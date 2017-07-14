"""
Creates our search index and its field structure,
and then populates it with packages from yum repositories
"""

import copy
import os
import json
import gzip
import logging
import shutil
import tarfile
import threading

import appstream
import requests
import xappy

from os.path import join

from utils import filter_search_string

# It is on the roof.
import fedoracommunity.pool

local = threading.local()
local.http = requests.session()
log = logging.getLogger()

# how many time to retry a downed server
MAX_RETRY = 10


def download_file(url, dest):
    dirname = os.path.dirname(dest)
    if not os.path.isdir(dirname):
        log.info("Creating directory %s" % dirname)
        os.makedirs(dirname)

    log.info("Downloading %s to %s" % (url, dest))
    r = local.http.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if not chunk:
                continue
            f.write(chunk)

    # Extract the big one.
    if dest.endswith('.tar.gz'):
        log.info("Extracting %s in %s" % (dest, dirname))
        f = tarfile.open(dest)
        try:
            f.extractall(path=dirname)
        finally:
            f.close()

    return dest


class Indexer(object):
    def __init__(self, cache_path,
                 tagger_url=None,
                 pkgdb_url=None,
                 mdapi_url=None,
                 icons_url=None):

        self.cache_path = cache_path
        self.dbpath = join(cache_path, 'search')
        self.icons_path = join(cache_path, 'icons')
        self.default_icon = 'package_128x128.png'
        self.tagger_url = tagger_url or "https://apps.fedoraproject.org/tagger"
        # killit!
        self.pkgdb_url = pkgdb_url or "https://admin.fedoraproject.org/pkgdb"
        self.mdapi_url = mdapi_url or "https://apps.fedoraproject.org/mdapi"
        self.icons_url = icons_url or "https://alt.fedoraproject.org/pub/alt/screenshots"
        self._latest_release = None
        self._active_fedora_releases = None
        self.icon_cache = {}

        self.create_index()

    def create_index(self):
        """ Create a new index, and set up its field structure """
        indexer = xappy.IndexerConnection(self.dbpath)

        indexer.add_field_action('exact_name', xappy.FieldActions.INDEX_FREETEXT)
        indexer.add_field_action('name', xappy.FieldActions.INDEX_FREETEXT,
                               language='en', spell=True)

        indexer.add_field_action('summary', xappy.FieldActions.INDEX_FREETEXT,
                               language='en')

        indexer.add_field_action('description', xappy.FieldActions.INDEX_FREETEXT,
                               language='en')

        indexer.add_field_action('subpackages',xappy.FieldActions.INDEX_FREETEXT,
                               language='en', spell=True)

        indexer.add_field_action('category_tags', xappy.FieldActions.INDEX_FREETEXT,
                               language='en', spell=True)

        indexer.add_field_action('cmd', xappy.FieldActions.INDEX_FREETEXT, spell=True)
        # FieldActions.TAG not currently supported in F15 xapian (1.2.7)
        #indexer.add_field_action('tags', xappy.FieldActions.TAG)
        indexer.add_field_action('tag', xappy.FieldActions.INDEX_FREETEXT, spell=True)

        #indexer.add_field_action('requires', xappy.FieldActions.INDEX_EXACT)
        #indexer.add_field_action('provides', xappy.FieldActions.INDEX_EXACT)

        self.indexer = indexer

    @property
    def latest_release(self):
        # TODO - query PDC (or Bodhi) for this info
        if not self._latest_release:
            response = local.http.get(self.pkgdb_url + "/api/collections")
            if not bool(response):
                raise IOError("Unable to find latest release %r" % response)
            data = response.json()

            # Strip off rawhide
            data['collections'] = [
                c for c in data['collections'] if c['version'] != 'devel'
            ]

            # Find the latest
            by_version = lambda c: int(c['version'])
            data['collections'].sort(key=by_version, reverse=True)
            self._latest_release = int(data['collections'][0]['version'])
        return self._latest_release

    @property
    def active_fedora_releases(self):
        if not self._active_fedora_releases:
            # TODO - query PDC (or Bodhi) for this info
            response = local.http.get(self.pkgdb_url + "/api/collections")
            if not bool(response):
                raise IOError("Unable to find releases %r" % response)
            data = response.json()

            # Strip off rawhide
            data['collections'] = [
                c for c in data['collections']
            ]

            # Strip off rawhide, inactive releases, and epel
            data['collections'] = [
                c for c in data['collections'] if (
                    c['version'] != 'devel' and
                    c['status'] == 'Active' and
                    c['name'] == 'Fedora'
                )
            ]

            by_version = lambda c: int(c['version'])
            data['collections'].sort(key=by_version, reverse=True)
            self._active_fedora_releases = [
                int(item['version']) for item in data['collections']
            ]
        return self._active_fedora_releases

    def pull_icons(self):
        for release in reversed(self.active_fedora_releases):
            prefix = 'f%i' % release
            files = ['fedora-%i.xml.gz', 'fedora-%i-icons.tar.gz']
            for fname in files:
                fname = fname % release
                url = join(self.icons_url, prefix, fname)
                target = join(self.icons_path, 'tmp', str(release), fname)

                try:
                    stats = os.stat(target)
                except OSError:
                    # Presumably no such file locally.  get it.
                    download_file(url, target)
                    continue

                # Check the file to see if it is different
                response = local.http.head(url)
                remote_size = int(response.headers['content-length'])
                local_size = stats.st_size
                if remote_size == local_size:
                    log.debug("%r seems unchanged." % url)
                    continue

                # Otherwise, they differ.  So download.
                download_file(url, target)

    def cache_icons(self):
        for release in self.active_fedora_releases:
            fname = 'fedora-%i.xml.gz' % release
            target = join(self.icons_path, 'tmp', str(release), fname)

            metadata = appstream.Store()
            f = gzip.open(target, 'rb')
            try:
                metadata.parse(f.read())
            finally:
                f.close()

            for idx, component in metadata.components.items():
                # Other types are 'stock' and 'unknown'
                icons = component.icons.get('cached', [])

                # Pick the biggest one..
                icon = None
                for candidate in icons:
                    if not icon:
                        icon = candidate
                        continue
                    if int(icon['width']) < int(candidate['width']):
                        icon = candidate

                if not icon:
                    continue

                # Some old F21 and F22 metadata entries have this weirdness.
                prefix = '{width}x{height}'.format(**icon)
                if icon['value'].startswith(prefix + '/'):
                    icon['value'] = icon['value'].strip(prefix + '/')

                # Move the file out of the temp dir and into place
                s = join(self.icons_path, 'tmp', str(release),
                         '{width}x{height}', '{value}')
                d = join(self.icons_path, '{value}')
                source = s.format(**icon)
                destination = d.format(**icon)

                # Furthermore, none of the F21 icons are namespaced
                if release == 21:
                    source = source.replace(prefix + '/', '')

                try:
                    shutil.copy(source, destination)

                    # And hang the name in the dict for other code to find it
                    # ... but only if we succeeded at placing the icon file.
                    self.icon_cache[component.pkgname] = icon['value']
                except IOError as e:
                    log.warning("appstream metadata lied: %s %r" % (source, e))
                except OSError as e:
                    log.warning("fail %r->%r.  %r" % (source, destination, e))

        shutil.rmtree(join(self.icons_path, 'tmp'))

    def gather_pkgdb_packages(self):
        response = local.http.get(self.pkgdb_url + '/api/packages/')
        if not bool(response):
            raise IOError("Failed to talk to pkgdb: %r" % response)

        pages = response.json()['page_total']

        for i in range(pages):
            log.info("Requesting pkgdb page %i of %i" % (i + 1, pages))
            response = local.http.get(self.pkgdb_url + '/api/packages/',
                                      params=dict(page=i+1))
            if not bool(response):
                raise IOError("Failed to talk to pkgdb: %r" % response)
            for package in response.json()['packages']:
                yield package

    def latest_active(self, name, ignore=None):
        # TODO - Query the PDC component-branches API endpoint for this
        ignore = ignore or []
        url = self.pkgdb_url + "/api/package/" + name
        response = local.http.get(url)
        if not bool(response):
            raise KeyError("Failed to talk to pkgdb: %s %r" % (url, response))
        data = response.json()
        # Figure out the latest active, non-retired branch
        by_version = lambda p: p['collection']['version']
        data['packages'].sort(key=by_version, reverse=True)
        for info in data['packages']:
            if info['collection']['version'] in ignore:
                continue
            if info['status'] == 'Approved':
                return info

        raise KeyError("Couldn't find active pkgdb branch for %r" % name)

    def construct_package_dictionary(self, package):
        """ Return structured package dictionary from a pkgdb package.

        Result looks like this::

           {base_package_name: {'name': base_package_name,
                                'summary': base_package_summary,
                                'description': base_package_summary,
                                'devel_owner': owner,
                                'icon': icon_name,
                                'package': None,
                                'upstream_url': url,
                                'sub_pkgs': [{'name': sub_package_name,
                                              'summary': sub_package_summary,
                                              'description': sub_package_description,
                                              'icon': icon_name,
                                              'package': package},
                                             ...]},
        """
        package = copy.deepcopy(package)

        name = package['name']
        try:
            info = self.latest_active(name)
        except KeyError:
            log.warning("Failed to get pkgdb info for %r" % name)
            return

        package['summary'] = info['package']['summary'] or \
            '(no summary in pkgdb)'
        package['description'] = info['package']['description'] or \
            '(no description in pkgdb)'
        package['devel_owner'] = info['point_of_contact']
        package['status'] = info['package']['status']

        package['icon'] = self.icon_cache.get(name, self.default_icon)
        package['branch'] =  info['collection']['branchname']
        package['sub_pkgs'] = list(self.get_sub_packages(package))

        # This is a "parent" reference.  the base packages always have "none"
        # for it, but the sub packages have the name of their parent package in
        # it.
        package['package'] = None

        return package

    def get_sub_packages(self, package):
        name = package['name']
        branch = package['branch']
        icon = package['icon']

        if branch == 'master':
            branch = 'rawhide'

        url = "/".join([self.mdapi_url, branch, "pkg", name])
        response = local.http.get(url)

        if not bool(response):
            # TODO -- don't always do this.
            # if we get a 404, that's usually because the package is retired in
            # rawhide... but that's okay.  we just queried pkgdb, so we should
            # see if it is active in any other branches, and if it is, get the
            # sub-packages from there.
            raise StopIteration

        data = response.json()
        sub_package_names = sorted(set([
            p for p in data['co-packages'] if p != name
        ]))

        for sub_package_name in sub_package_names:
            url = "/".join([self.mdapi_url, branch, "pkg", sub_package_name])
            response = local.http.get(url)
            if not bool(response):
                log.warn("Failed to get sub info for %r, %r" % (sub_package_name, response))
                continue
            data = response.json()
            yield {
                'name': sub_package_name,
                'summary': data['summary'],
                'description': data['description'],
                'icon': icon,
                'package': name,
                'branch': branch,
            }

    def index_files_of_interest(self, doc, package_dict):
        name = package_dict['name']
        branch = package_dict['branch']

        if branch == 'master':
            branch = 'rawhide'

        url = "/".join([self.mdapi_url, branch, "files", name])
        response = local.http.get(url)
        if not bool(response):
            log.warn("Failed to get file list for %r, %r" % (name, response))
            return
        data = response.json()
        for entry in data['files']:
            filenames = entry['filenames'].split('/')
            for filename in filenames:
                if filename.startswith('/usr/bin'):
                    # index executables
                    log.info("        indexing exe file %s" % os.path.basename(filename))
                    exe_name = filter_search_string(os.path.basename(filename))
                    doc.fields.append(xappy.Field('cmd', "EX__%s__EX" % exe_name))

    def index_tags(self, doc, package):
        name = package['name']
        response = local.http.get(self.tagger_url + '/api/v1/' + name)
        if not bool(response):
            log.warn("Failed to get tagger info for %r, %r" % (name, response))
            return
        tags = response.json()['tags']
        for tag_info in tags:
            tag_name = tag_info['tag']
            total = tag_info['total']
            if total > 0:
                log.debug("    adding '%s' tag (%d)" % (
                    tag_name.encode('utf-8'), total))
            for i in range(total):
                doc.fields.append(xappy.Field('tag', tag_name))

    def index_packages(self):
        # This is a generator that yields dicts of package info that we index
        # TODO - replace this with gather_pdc_packages() and get the master list from there.
        #
        # This is *probably* the endpoint you want, but you might need to use another:
        #   https://pdc.fedoraproject.org/rest_api/v1/global-components/
        #
        # See some pull requests here for examples of how to query PDC:
        #   https://pagure.io/releng/pull-requests
        #
        # You can delete the gather_pkgdb_packages one.
        packages = self.gather_pkgdb_packages()

        # XXX - Only grab the first N for dev purposes
        #packages = [packages.next() for i in range(50)]

        def io_work(package):
            log.info("indexing %s" % (package['name']))
            local.http = requests.session()

            # Do all of the gathering...
            package = self.construct_package_dictionary(package)

            # If the package is retired in all branches, it is None here..
            if package is None:
                return None

            return package

        pool = fedoracommunity.pool.ThreadPool(20)
        packages = pool.map(io_work, packages)

        for package in packages:
            if package is None:
                continue
            # And then prepare everything for xapian
            log.info("Processing final details for %s" % package['name'])
            document = self._create_document(package)
            processed = self._process_document(package, document)
            self.indexer.add(processed)

        self.indexer.close()

    def _process_document(self, package, document):
        processed = self.indexer.process(document, False)
        processed._doc.set_data(json.dumps(package))
        # preempt xappy's processing of data
        processed._data = None
        return processed

    def _create_document(self, package):
        doc = xappy.UnprocessedDocument()
        filtered_name = filter_search_string(package['name'])
        filtered_summary = filter_search_string(package['summary'])
        filtered_description = filter_search_string(package['description'])

        doc.fields.append(xappy.Field('exact_name', 'EX__' + filtered_name + '__EX', weight=10.0))

        name_parts = filtered_name.split('_')
        for i in range(20):
            if len(name_parts) > 1:
                for part in name_parts:
                    doc.fields.append(xappy.Field('name', part, weight=1.0))
            doc.fields.append(xappy.Field('name', filtered_name, weight=10.0))

        for i in range(4):
            doc.fields.append(xappy.Field('summary', filtered_summary, weight=1.0))
        doc.fields.append(xappy.Field('description', filtered_description, weight=0.2))

        self.index_files_of_interest(doc, package)
        self.index_tags(doc, package)

        for sub_package in package['sub_pkgs']:
            filtered_sub_package_name = filter_search_string(sub_package['name'])
            log.info("       indexing subpackage %s" % sub_package['name'])

            doc.fields.append(xappy.Field('subpackages', filtered_sub_package_name, weight=1.0))
            doc.fields.append(xappy.Field('exact_name', 'EX__' + filtered_sub_package_name + '__EX', weight=10.0))

            self.index_files_of_interest(doc, sub_package)

            # fedora-tagger does not provide special tags for sub-packages...
            #self.index_tags(doc, sub_package)

            # Set special sub-package icon if appstream has one
            sub_package['icon'] = self.icon_cache.get(
                sub_package['name'], self.default_icon)

            # If the parent has a dull icon, give it ours!
            if sub_package['icon'] != self.default_icon \
                and package['icon'] == self.default_icon:
                package['icon'] = sub_package['icon']

            # remove anything we don't want to store
            del sub_package['package']

        # @@: Right now we're only indexing the first part of the
        # provides/requires, and not boolean comparison or version
        #for requires in package.requires:
        #    print requires[0]
        #    doc.fields.append(xappy.Field('requires', requires[0]))
        #for provides in package.provides:
        #    doc.fields.append(xappy.Field('provides', provides[0]))


        # remove anything we don't want to store and then store data in
        # json format
        del package['package']

        return doc


# TODO - pkgdb url here can go
def run(cache_path, tagger_url=None, pkgdb_url=None, mdapi_url=None, icons_url=None):
    indexer = Indexer(cache_path, tagger_url, pkgdb_url, mdapi_url, icons_url)

    indexer.pull_icons()
    indexer.cache_icons()

    log.info("Indexing packages.")
    indexer.index_packages()
    log.info("Indexed a ton of packages.")
