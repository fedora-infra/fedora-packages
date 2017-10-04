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
import re

import requests
import xappy
import pdc_client

from os.path import join

from utils import filter_search_string

import gi

gi.require_version('AppStreamGlib', '1.0')

from gi.repository import AppStreamGlib

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
                 bodhi_url=None,
                 mdapi_url=None,
                 icons_url=None,
                 pdc_url=None,
                 pagure_url=None):

        self.cache_path = cache_path
        self.dbpath = join(cache_path, 'search')
        self.icons_path = join(cache_path, 'icons')
        self.default_icon = 'package_128x128.png'
        self.tagger_url = tagger_url or "https://apps.fedoraproject.org/tagger"
        self.bodhi_url = bodhi_url or "https://bodhi.fedoraproject.org"
        self.mdapi_url = mdapi_url or "https://apps.fedoraproject.org/mdapi"
        self.icons_url = icons_url or "https://alt.fedoraproject.org/pub/alt/screenshots"
        self.pdc_url = pdc_url or "https://pdc.fedoraproject.org/rest_api/v1"
        self.pagure_url = pagure_url or "https://src.fedoraproject.org/api/0"
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

        indexer.add_field_action('subpackages', xappy.FieldActions.INDEX_FREETEXT,
                                 language='en', spell=True)

        indexer.add_field_action('category_tags', xappy.FieldActions.INDEX_FREETEXT,
                                 language='en', spell=True)

        indexer.add_field_action('cmd', xappy.FieldActions.INDEX_FREETEXT, spell=True)
        # FieldActions.TAG not currently supported in F15 xapian (1.2.7)
        # indexer.add_field_action('tags', xappy.FieldActions.TAG)
        indexer.add_field_action('tag', xappy.FieldActions.INDEX_FREETEXT, spell=True)

        # indexer.add_field_action('requires', xappy.FieldActions.INDEX_EXACT)
        # indexer.add_field_action('provides', xappy.FieldActions.INDEX_EXACT)

        self.indexer = indexer

    @property
    def latest_release(self):
        # TODO - query PDC (or Bodhi) for this info
        if not self._latest_release:
            releases_all = self.get_all_releases_from_bodhi()

            # Find the latest
            by_version = lambda c: int(c['version'])
            releases_all.sort(key=by_version, reverse=True)
            self._latest_release = int(releases_all[0]['version'])
        return self._latest_release

    @property
    def active_fedora_releases(self):
        if not self._active_fedora_releases:
            releases_all = self.get_all_releases_from_bodhi()

            # Strip off inactive releases, and epel
            releases_all = [
                c for c in releases_all if (
                    c['state'] == 'current' and
                    c['id_prefix'] == 'FEDORA'
                )
            ]

            by_version = lambda c: int(c['version'])
            releases_all.sort(key=by_version, reverse=True)
            self._active_fedora_releases = [
                int(item['version']) for item in releases_all
            ]
        return self._active_fedora_releases

    def get_all_releases_from_bodhi(self):
        response = local.http.get(self.bodhi_url + "/releases").json()
        if not bool(response):
            raise IOError("Unable to find latest release %r" % response)

        releases_all = None
        for i in range(1, response['pages']+1):
            if releases_all is None:
                releases_all = response['releases']
                continue
            else:
                temp = local.http.get(self.bodhi_url + "/releases?page="+str(i)).json()
                temp = temp['releases']
                releases_all.extend(temp)
        if releases_all is None:
            raise TypeError

        return releases_all

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

            metadata = AppStreamGlib.Store()

            with gzip.open(target, 'rb') as f:
                metadata.from_xml(f.read(), '')

            for app in metadata.get_apps():
                # Other types are 'stock' and 'unknown'
                icons = app.get_icons()
                pkgname = app.get_pkgnames()[0]

                # Pick the biggest one..
                icon = None
                for candidate in icons:
                    if not icon:
                        if candidate.get_kind().value_nick == 'cached':
                            icon = candidate
                        continue
                    if int(icon.get_width()) < int(candidate.get_width()):
                        icon = candidate

                if not icon:
                    continue

                # Move the file out of the temp dir and into place
                s = join(self.icons_path, 'tmp', str(release),
                         '{width}x{height}', '{value}')
                d = join(self.icons_path, '{value}')
                source = s.format(width=icon.get_width(), height=icon.get_height(),
                                  value=icon.get_name())
                destination = d.format(value=icon.get_name())

                try:
                    shutil.copy(source, destination)

                    # And hang the name in the dict for other code to find it
                    # ... but only if we succeeded at placing the icon file.
                    self.icon_cache[pkgname] = icon.get_name()
                except IOError as e:
                    log.warning("appstream metadata lied: %s %r" % (source, e))
                except OSError as e:
                    log.warning("fail %r->%r.  %r" % (source, destination, e))

        shutil.rmtree(join(self.icons_path, 'tmp'))

    def gather_pdc_packages(self, pkg_name=None):
        pdc = pdc_client.PDCClient(self.pdc_url, develop=True, page_size=100)

        kwargs = dict()
        if pkg_name is not None:
            kwargs['name'] = pkg_name

        for component in pdc.get_paged(pdc['global-components']._, **kwargs):
            yield component

    def latest_active(self, name, ignore=None):

        # First, check to see if it is retired.
        # PDCClient pulls connection information from /etc/pdc.d/
        # develop=True means: don't authenticate.
        ignore = ignore or []
        pdc = pdc_client.PDCClient(self.pdc_url, develop=True)
        kwargs = dict(global_component=name, active=True, type='rpm')
        latest_version = None
        branch_info = None
        for branch in pdc.get_paged(pdc['component-branches']._, **kwargs):
            if re.match(r'f\d+', branch['name']):
                version = int(branch['name'].strip('f'))
                if version in ignore:
                    continue
                if latest_version:
                    latest_version = max(latest_version, version)
                    if latest_version == version:
                        branch_info = branch
                else:
                    latest_version = version
                    branch_info = branch

        if latest_version is None:
            # Check if we are a subpackage,
            # if so run latest_active with the main package name
            kwargs = {'name': name}
            for comp in pdc.get_paged(pdc['rpms']._, **kwargs):
                branch_info = self.latest_active(comp.get('srpm_name'))
                return branch_info

            raise ValueError('There is no active branch tied to a Fedora release')
        return branch_info

    def construct_package_dictionary(self, package):
        """ Return structured package dictionary from a pkg package.

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

        try:
            name = package['name']
            info = self.latest_active(name)
        except KeyError:
            log.warning("Failed to get pdc info for %r" % name)
            return

        # Getting summary and description
        try:
            mdapi_pkg_url = '/'.join([self.mdapi_url, info['name'],
                                     'srcpkg', info['global_component']])
            meta_data = local.http.get(mdapi_pkg_url).json()
            package['summary'] = meta_data['summary']
            package['description'] = meta_data['description']
        except:
            log.exception("Failed to get summary and description for %r at %s." % (
                info['global_component'], mdapi_pkg_url))
            package['summary'] = 'no summary in mdapi'
            package['description'] = 'no description in mdapi'

        # Getting the upstream url for the package
        upstream_url_gen = self.gather_pdc_packages(info['global_component'])
        for obj in upstream_url_gen:
            if obj['upstream']:
                package['upstream_url'] = obj['upstream']

        try:
            # Getting the owner name
            pagure_pkg_url = '/'.join([self.pagure_url, 'rpms', info['global_component']])
            owner_data = local.http.get(pagure_pkg_url).json()
            package['devel_owner'] = owner_data['access_users']['owner'][0]
        except:
            log.exception("Failed to get owner name for %r at %s." % (
                info['global_component'], pagure_pkg_url))
            package['devel_owner'] = 'no owner info in pagure'

        package['status'] = info['active']
        package['icon'] = self.icon_cache.get(name, self.default_icon)
        package['branch'] = info['name']
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

        url = "/".join([self.mdapi_url, branch, "srcpkg", name])
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
                log.warn("Failed to get sub info for %r, %r" %
                         (sub_package_name, response))
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

        packages = self.gather_pdc_packages()

        # XXX - Only grab the first N for dev purposes
        # packages = [packages.next() for i in range(50)]

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

        doc.fields.append(xappy.Field('exact_name',
                          'EX__' + filtered_name + '__EX', weight=10.0))

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

            doc.fields.append(xappy.Field('subpackages',
                                          filtered_sub_package_name, weight=1.0))
            doc.fields.append(xappy.Field('exact_name',
                                          'EX__' + filtered_sub_package_name + '__EX',
                                          weight=10.0))

            self.index_files_of_interest(doc, sub_package)

            # fedora-tagger does not provide special tags for sub-packages...
            # self.index_tags(doc, sub_package)

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
        # for requires in package.requires:
        #    print requires[0]
        #    doc.fields.append(xappy.Field('requires', requires[0]))
        # for provides in package.provides:
        #    doc.fields.append(xappy.Field('provides', provides[0]))

        # remove anything we don't want to store and then store data in
        # json format
        del package['package']

        return doc


def run(cache_path, tagger_url=None, bodhi_url=None,
        mdapi_url=None, icons_url=None, pdc_url=None, pagure_url=None):
    indexer = Indexer(cache_path, tagger_url, bodhi_url, mdapi_url,
                      icons_url, pdc_url, pagure_url)

    indexer.pull_icons()
    indexer.cache_icons()

    log.info("Indexing packages.")
    indexer.index_packages()
    log.info("Indexed a ton of packages.")
