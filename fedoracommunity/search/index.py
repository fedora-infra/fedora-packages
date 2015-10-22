"""
Creates our search index and its field structure,
and then populates it with packages from yum repositories
"""

import copy
import os
import logging
import requests
import urllib2
import xappy

from os.path import join, dirname

from utils import filter_search_string
from parsers import DesktopParser, SimpleSpecfileParser
#from iconcache import IconCache

http = requests.session()
log = logging.getLogger()

# how many time to retry a downed server
MAX_RETRY = 10

try:
    import json
except ImportError:
    import simplejson as json

class Indexer(object):
    def __init__(self, cache_path, yum_conf, tagger_url=None, pkgdb_url=None, mdapi_url=None):
        self.cache_path = cache_path
        self.dbpath = join(cache_path, 'search')
        self.yum_cache_path = join(cache_path, 'yum-cache')
        self.icons_path = join(cache_path, 'icons')
        self.yum_conf = yum_conf
        self.create_index()
        self._owners_cache = None
        self.default_icon = 'package_128x128'
        self.tagger_url = tagger_url
        self.pkgdb_url = pkgdb_url or "https://admin.fedoraproject.org/pkgdb"
        self.mdapi_url = mdapi_url or "http://209.132.184.236"  # dev instance

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

    def find_devel_owner(self, package_name, retry=0):
        if self._owners_cache == None:
            print "Caching the owners list from pkgdb"

            url = self.pkgdb_url + "/api/bugzilla?format=json"
            response = http.get(url)
            self._owners_cache = response.json()['bugzillaAcls']

        try:
            mainowner = self._owners_cache['Fedora'][package_name]['owner']
            print 'Owner: %s' % mainowner
            return mainowner
        except KeyError:
            print 'Owner: None'
            return ''

    def gather_pkgdb_packages(self):
        response = http.get(self.pkgdb_url + '/api/packages/')
        if not bool(response):
            raise IOError("Failed to talk to pkgdb: %r" % response)

        pages = response.json()['page_total']

        for i in range(pages):
            log.info("Requesting pkgdb page %i of %i" % (i + 1, pages))
            response = http.get(self.pkgdb_url + '/api/packages/')
            if not bool(response):
                raise IOError("Failed to talk to pkgdb: %r" % response)
            for package in response.json()['packages']:
                yield package

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
                                'src_package': src_package,
                                'sub_pkgs': [{'name': sub_package_name,
                                              'summary': sub_package_summary,
                                              'description': sub_package_description,
                                              'icon': icon_name,
                                              'package': package},
                                             ...]},
        """
        package = copy.deepcopy(package)

        name = package['name']

        ###
        # Get some more detailed pkgdb info for this package (in rawhide)
        ###
        url = self.pkgdb_url + "/api/package/" + name
        params = dict(branches='master')
        pkgdb_info = http.get(url, params=params).json()
        pkgdb_info = pkgdb_info['packages'][0]

        package['summary'] = pkgdb_info['package']['summary'] or \
            '(no summary in pkgdb)'
        package['description'] = pkgdb_info['package']['description'] or \
            '(no description in pkgdb)'
        package['devel_owner'] = pkgdb_info['point_of_contact']
        package['status'] = pkgdb_info['package']['status']

        ###
        # Get some further detailed information from koji.
        ###
        package['sub_pkgs'] = list(self.get_sub_packages(name))

        # This is a "parent" reference.  the base packages always have "none"
        # for it, but the sub packages have the name of their parent package in
        # it.
        package['package'] = None

        # TODO -- get this icon for real
        package['icon'] = self.default_icon

        # Is this important?  I think maybe not..
        # TODO - try deleting it and see if everything still works..
        package['src_package'] = 'is this important?'

        return package

    def get_sub_packages(self, name):

        response = http.get(self.mdapi_url + "/pkg/" + name)

        if not bool(response):
            # TODO -- don't always do this.
            # if we get a 404, that's usually because the package is retired in
            # rawhide... but that's okay.  we just queried pkgdb, so we should
            # see if it is active in any other branches, and if it is, get the
            # sub-packages from there.
            raise StopIteration

        data = response.json()
        sub_package_names = [p for p in data['co-packages'] if p != name]

        for sub_package_name in sub_package_names:
            response = http.get(self.mdapi_url + "/pkg/" + sub_package_name)
            if not bool(response):
                log.warn("Failed to get sub info for %r" % sub_package_name)
                continue
            data = response.json()
            yield {
                'name': sub_package_name,
                'summary': data['summary'],
                'description': data['description'],
                'icon': 'wat3',  # inherit this from the parent
                'package': name,
            }

    def index_yum_packages(self):
        """
        index_yum_packages

        Index the packages from yum into this format:

           {base_package_name: {'name': base_package_name,
                                'summary': base_package_summary,
                                'description': base_package_summary,
                                'devel_owner': owner,
                                'icon': icon_name,
                                'package': package,
                                'upstream_url': url,
                                'src_package': src_package,
                                'sub_pkgs': [{'name': sub_package_name,
                                              'summary': sub_package_summary,
                                              'description': sub_package_description,
                                              'icon': icon_name,
                                              'package': package},
                                             ...]},
            ...
           }
        """
        import yum
        yb = yum.YumBase()
        self.yum_base = yb

        if not os.path.exists(self.yum_cache_path):
            os.mkdir(self.yum_cache_path)

        if not os.path.exists(self.icons_path):
            os.mkdir(self.icons_path)

        yb.doConfigSetup(self.yum_conf, root=os.getcwd(), init_plugins=False)
        for r in yb.repos.findRepos('*'):
            if r.id in ['rawhide-x86_64', 'rawhide-source']:
                r.enable()
            else:
                r.disable()

        yb._getRepos(doSetup = True)
        yb._getSacks(['x86_64', 'noarch', 'src'])
        yb.doRepoSetup()
        yb.doSackFilelistPopulate()

        # Doesn't work right now due to a bug in yum.
        # https://bugzilla.redhat.com/show_bug.cgi?id=750593
        #yb.disablePlugins()

        yb.conf.cache = 1

        self.icon_cache = IconCache(yb, ['gnome-icon-theme', 'oxygen-icon-theme'], self.icons_path, self.cache_path)

        packages = yb.packageSack.returnPackages()
        base_packages = {}
        seen_package_names = []

        # get the tagger data
        self.tagger_cache = None
        if self.tagger_url:
            print "Caching tagger data"
            response = urllib2.urlopen(self.tagger_url)
            html = response.read()
            tagger_data = json.loads(html)
            self.tagger_cache = {}
            for package_tag_info in tagger_data['packages']:
                for package_name in package_tag_info.keys():
                    self.tagger_cache[package_name] = package_tag_info[package_name]

        package_count = 0
        for package in packages:
            # precache the icon themes for later extraction and matching
            if package.ui_from_repo != 'rawhide-source':
                self.icon_cache.check_package(package)

            if not package.base_package_name in base_packages:
                # we haven't seen this base package yet so add it
                base_packages[package.base_package_name] = {'name': package.base_package_name,
                                                    'summary': '',
                                                    'description':'',
                                                    'devel_owner':'',
                                                    'package': None,
                                                    'src_package': None,
                                                    'icon': self.default_icon,
                                                    'upstream_url': None,
                                                    'sub_pkgs': []}

            base_package = base_packages[package.base_package_name]

            if package.ui_from_repo == 'rawhide-source':
               package_count += 1
               print "%d: pre-processing package '%s':" % (package_count, package['name'])

               base_package['src_package'] = package
               base_package['upstream_url'] = package.URL

               if not base_package['devel_owner']:
                   base_package['devel_owner'] = self.find_devel_owner(package.name)
               if not base_package['summary']:
                   base_package['summary'] = package.summary
               if not base_package['description']:
                   base_package['description'] = package.description
               continue

            # avoid duplicates
            if package.name in seen_package_names:
                continue

            seen_package_names.append(package.name)

            if package.base_package_name == package.name:
                # this is the main package
                if not base_package['src_package']:
                    package_count += 1
                    print "%d: pre-processing package '%s':" % (package_count, package['name'])

                base_package['summary'] = package.summary
                base_package['description'] = package.description
                base_package['package'] = package
                base_package['devel_owner'] = self.find_devel_owner(package.name)
            else:
                # this is a sub package
                package_count += 1
                print "%d: pre-processing package '%s':" % (package_count, package['name'])

                subpackages = base_package['sub_pkgs']
                subpackages.append({'name': package.name,
                                'summary': package.summary,
                                'description': package.description,
                                'icon': self.default_icon,
                                'package': package})

        return base_packages

    #def index_desktop_file(self, doc, desktop_file, package_dict, desktop_file_cache):
    #    doc.fields.append(xappy.Field('tag', 'desktop'))

    #    dp = DesktopParser(desktop_file)
    #    category = dp.get('Categories', '')

    #    for c in category.split(';'):
    #        if c:
    #            c = filter_search_string(c)
    #            doc.fields.append(xappy.Field('category_tags', c))
    #            # add exact match also
    #            doc.fields.append(xappy.Field('category_tags', "EX__%s__EX" % c))

    #    icon = dp.get('Icon', '')
    #    if icon:
    #        print "Icon %s" % icon
    #        generated_icon = self.icon_cache.generate_icon(icon, desktop_file_cache)
    #        if generated_icon != None:
    #            package_dict['icon'] = icon

    def index_files_of_interest(self, doc, package_dict):
        name = package_dict['name']
        response = http.get(self.mdapi_url + "/files/" + name)
        if not bool(response):
            log.warn("Failed to get file list for %r" % name)
            return
        data = response.json()
        for entry in data:
            filenames = entry['filenames'].split('/')
            for filename in filenames:
                if filename.endswith('.desktop'):
                    log.warn("TODO - indexing the content of desktop files is disabled for now")
                    continue
                    # When we get back here, we should give up on parsing the .desktop file like this,
                    # and we should instead use the appstream metadata that hughsie worked on
                    # See:
                    # - https://alt.fedoraproject.org/pub/alt/screenshots/f23/$a
                    # - fedora-23-icons.tar.gz there has the icons
                    # - fedora-23-xml.gz has the metadata
                    # - github.com/hughsie/python-appstream has a parser for the xml if we need it.

                    ## index apps
                    #log.info("        indexing desktop file %s" % os.path.basename(filename))
                    #f = desktop_file_cache.open_file(filename, decompress_filter='*.desktop')
                    #if f == None:
                    #    log.warn("could not open desktop file")
                    #    continue
                    #self.index_desktop_file(doc, f, package_dict, desktop_file_cache)
                    #f.close()
                if filename.startswith('/usr/bin'):
                    # index executables
                    log.info("        indexing exe file %s" % os.path.basename(filename))
                    exe_name = filter_search_string(os.path.basename(filename))
                    doc.fields.append(xappy.Field('cmd', "EX__%s__EX" % exe_name))

    def index_spec(self, doc, package, src_rpm_cache):
        # don't use this but keep it here if we need to index spec files
        # again
        for filename in package['src_package'].filelist:
            if filename.endswith('.spec'):
                break;

        print "        Spec: %s" % filename
        f = src_rpm_cache.open_file(filename)
        if f:
            try:
                spec_parse = SimpleSpecfileParser(f)
                package['upstream_url'] = spec_parse.get('url')
            except ValueError as e:
                print e
                print "    Setting upstream_url to empty string for now"
                package['upstream_url'] = ''

    def index_tags(self, doc, package):
        if not self.tagger_cache:
            return

        name = package['name']
        tags = self.tagger_cache.get(name, [])
        for tag_info in tags:
            tag_name = tag_info['tag']
            total = tag_info['total']
            if total > 0:
                print "    adding '%s' tag (%d)" % (tag_name.encode('utf-8'), total)
            for i in range(total):
                doc.fields.append(xappy.Field('tag', tag_name))

    def index_packages(self):
        # This is a generator that yields dicts of package info that we index
        packages = self.gather_pkgdb_packages()

        # XXX - Only grab the first N for dev purposes
        packages = [packages.next() for i in range(5)]

        packages = (self.construct_package_dictionary(p) for p in packages)

        for i, package in enumerate(packages):
            print("%d: indexing %s" % (i, package['name']))
            document = self._create_document(package)
            processed = self._process_document(package, document)
            self.indexer.add(processed)

        self.indexer.close()
        return i + 1

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
        log.warn("TODO -- add indexing tags back in...")
        #self.index_tags(doc, package)

        for sub_package in package['sub_pkgs']:
            filtered_sub_package_name = filter_search_string(sub_package['name'])
            print("       indexing subpackage %s" % sub_package['name'])

            doc.fields.append(xappy.Field('subpackages', filtered_sub_package_name, weight=1.0))
            doc.fields.append(xappy.Field('exact_name', 'EX__' + filtered_sub_package_name + '__EX', weight=10.0))

            self.index_files_of_interest(doc, sub_package)
            log.warn("TODO -- add indexing tags back in...")
            #self.index_tags(doc, sub_package)

            if sub_package['icon'] != self.default_icon and package['icon'] == self.default_icon:
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
        del package['src_package']

        return doc


def run(cache_path, yum_conf, tagger_url=None, pkgdb_url=None, mdapi_url=None):
    indexer = Indexer(cache_path, yum_conf, tagger_url, pkgdb_url, mdapi_url)

    print "Indexing packages."
    count = indexer.index_packages()
    print "Indexed %d packages." % count

if __name__ == '__main__':
    run('index_cache', join(dirname(__file__), 'yum.conf'), 'http://apps.fedoraproject.org/tagger/dump')
