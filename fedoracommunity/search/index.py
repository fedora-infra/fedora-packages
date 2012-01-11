"""
Creates our search index and its field structure,
and then populates it with packages from yum repositories
"""
import os
import sys
import shutil
import urllib2
import tempfile
import xappy

from os.path import join, dirname

from utils import filter_search_string
from fedora.client import PackageDB, ServerError
from rpmcache import RPMCache
from parsers import DesktopParser, SimpleSpecfileParser
from iconcache import IconCache


# how many time to retry a downed server
MAX_RETRY = 10

try:
    import json
except ImportError:
    import simplejson as json

class Indexer(object):
    def __init__(self, cache_path, yum_conf, tagger_url=None, pkgdb_url=None):
        self.cache_path = cache_path
        self.dbpath = join(cache_path, 'search')
        self.yum_cache_path = join(cache_path, 'yum-cache')
        self.icons_path = join(cache_path, 'icons')
        self.yum_conf = yum_conf
        self.create_index()
        self._owners_cache = None
        self.default_icon = 'package_128x128'
        self.tagger_url = tagger_url
        if pkgdb_url:
            self.pkgdb_client = PackageDB(base_url=pkgdb_url)
        else:
            self.pkgdb_client = PackageDB()

    def create_index(self):
        """ Create a new index, and set up its field structure """
        iconn = xappy.IndexerConnection(self.dbpath)

        iconn.add_field_action('exact_name', xappy.FieldActions.INDEX_FREETEXT)
        iconn.add_field_action('name', xappy.FieldActions.INDEX_FREETEXT,
                               language='en')

        iconn.add_field_action('summary', xappy.FieldActions.INDEX_FREETEXT,
                               language='en')

        iconn.add_field_action('description', xappy.FieldActions.INDEX_FREETEXT,
                               language='en')

        iconn.add_field_action('subpackages',xappy.FieldActions.INDEX_FREETEXT,
                               language='en')

        iconn.add_field_action('category_tags', xappy.FieldActions.INDEX_FREETEXT,
                               language='en')

        iconn.add_field_action('cmd', xappy.FieldActions.INDEX_FREETEXT)
        # FieldActions.TAG not currently supported in F15 xapian (1.2.7)
        #iconn.add_field_action('tags', xappy.FieldActions.TAG)
        iconn.add_field_action('tag', xappy.FieldActions.INDEX_FREETEXT)

        #iconn.add_field_action('requires', xappy.FieldActions.INDEX_EXACT)
        #iconn.add_field_action('provides', xappy.FieldActions.INDEX_EXACT)

        self.iconn = iconn

    def find_devel_owner(self, pkg_name, retry=0):
        if self._owners_cache == None:
            print "Caching the owners list from PackageDB"

            self._owners_cache = self.pkgdb_client.get_bugzilla_acls()

        try:
            mainowner = self._owners_cache['Fedora'][pkg_name]['owner']
            print 'Owner: %s' % mainowner
            return mainowner
        except KeyError:
            print 'Owner: None'
            return ''

    def index_yum_pkgs(self):
        """
        index_yum_pkgs

        Index the packages from yum into this format:

           {base_package_name: {'name': base_package_name,
                                'summary': base_package_summary,
                                'description': base_package_summary,
                                'devel_owner': owner,
                                'icon': icon_name,
                                'pkg': pkg,
                                'upstream_url': url,
                                'src_pkg': src_pkg,
                                'sub_pkgs': [{'name': sub_pkg_name,
                                              'summary': sub_pkg_summary,
                                              'description': sub_pkg_description,
                                              'icon': icon_name,
                                              'pkg': pkg},
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

        pkgs = yb.pkgSack.returnPackages()
        base_pkgs = {}
        seen_pkg_names = []

        # get the tagger data
        self.tagger_cache = None
        if self.tagger_url:
            print "Caching tagger data"
            response = urllib2.urlopen(self.tagger_url)
            html = response.read()
            tagger_data = json.loads(html)
            self.tagger_cache = {}
            for pkg_tag_info in tagger_data['packages']:
                for pkg_name in pkg_tag_info.keys():
                    self.tagger_cache[pkg_name] = pkg_tag_info[pkg_name]

        i = 0
        for pkg in pkgs:
            i += 1
            print "%d: pre-processing package '%s':" % (i, pkg['name'])

            # precache the icon themes for later extraction and matching
            if pkg.ui_from_repo != 'rawhide-source':
                self.icon_cache.check_pkg(pkg)

            if not pkg.base_package_name in base_pkgs:
                # we haven't seen this base package yet so add it
                base_pkgs[pkg.base_package_name] = {'name': pkg.base_package_name,
                                                    'summary': '',
                                                    'description':'',
                                                    'devel_owner':'',
                                                    'pkg': None,
                                                    'src_pkg': None,
                                                    'icon': self.default_icon,
                                                    'upstream_url': None,
                                                    'sub_pkgs': []}

            base_pkg = base_pkgs[pkg.base_package_name]

            if pkg.ui_from_repo == 'rawhide-source':
               base_pkg['src_pkg'] = pkg
               base_pkg['upstream_url'] = pkg.URL

               if not base_pkg['devel_owner']:
                   base_pkg['devel_owner'] = self.find_devel_owner(pkg.name)
               if not base_pkg['summary']:
                   base_pkg['summary'] = pkg.summary
               if not base_pkg['description']:
                   base_pkg['description'] = pkg.description
               continue

            # avoid duplicates
            if pkg.name in seen_pkg_names:
                continue

            seen_pkg_names.append(pkg.name)

            if pkg.base_package_name == pkg.name:
                # this is the main package
                base_pkg['summary'] = pkg.summary
                base_pkg['description'] = pkg.description
                base_pkg['pkg'] = pkg
                base_pkg['devel_owner'] = self.find_devel_owner(pkg.name)
            else:
                # this is a sub package
                subpkgs = base_pkg['sub_pkgs']
                subpkgs.append({'name': pkg.name,
                                'summary': pkg.summary,
                                'description': pkg.description,
                                'icon': self.default_icon,
                                'pkg': pkg})

        return base_pkgs

    def index_desktop_file(self, doc, desktop_file, pkg_dict, desktop_file_cache):
        doc.fields.append(xappy.Field('tag', 'desktop'))

        dp = DesktopParser(desktop_file)
        category = dp.get('Categories', '')

        for c in category.split(';'):
            if c:
                c = filter_search_string(c)
                doc.fields.append(xappy.Field('category_tags', c))
                # add exact match also
                doc.fields.append(xappy.Field('category_tags', "EX__%s__EX" % c))

        icon = dp.get('Icon', '')
        if icon:
            print "Icon %s" % icon
            generated_icon = self.icon_cache.generate_icon(icon, desktop_file_cache)
            if generated_icon != None:
                pkg_dict['icon'] = icon

    def index_files(self, doc, pkg_dict):
        yum_pkg = pkg_dict['pkg']
        if yum_pkg != None:
            desktop_file_cache = RPMCache(yum_pkg, self.yum_base, self.cache_path)
            desktop_file_cache.open()
            for filename in yum_pkg.filelist:
                if filename.endswith('.desktop'):
                    # index apps
                    print "        indexing desktop file %s" % os.path.basename(filename)
                    f = desktop_file_cache.open_file(filename, decompress_filter='*.desktop')
                    if f == None:
                        print "could not open desktop file"
                        continue

                    self.index_desktop_file(doc, f, pkg_dict, desktop_file_cache)
                    f.close()
                if filename.startswith('/usr/bin'):
                    # index executables
                    print ("        indexing exe file %s" % os.path.basename(filename))
                    exe_name = filter_search_string(os.path.basename(filename))
                    doc.fields.append(xappy.Field('cmd', "EX__%s__EX" % exe_name))

            desktop_file_cache.close()

    def index_spec(self, doc, pkg, src_rpm_cache):
        # don't use this but keep it here if we need to index spec files
        # again
        for filename in pkg['src_pkg'].filelist:
            if filename.endswith('.spec'):
                break;

        print "        Spec: %s" % filename
        f = src_rpm_cache.open_file(filename)
        if f:
            try:
                spec_parse = SimpleSpecfileParser(f)
                pkg['upstream_url'] = spec_parse.get('url')
            except ValueError as e:
                print e
                print "    Setting upstream_url to empty string for now"
                pkg['upstream_url'] = ''

    def index_tags(self, doc, pkg):
        if not self.tagger_cache:
            return

        name = pkg['name']
        tags = self.tagger_cache.get(name, [])
        for tag_info in tags:
            tag_name = tag_info['tag']
            total = tag_info['total']
            if total > 0:
                print "    adding '%s' tag (%d)" % (tag_name, total)
            for i in range(total):
                doc.fields.append(xappy.Field('tag', tag_name))

    def index_pkgs(self):
        yum_pkgs = self.index_yum_pkgs()
        i = 0

        for pkg in yum_pkgs.values():
            i += 1

            doc = xappy.UnprocessedDocument()
            filtered_name = filter_search_string(pkg['name'])
            filtered_summary = filter_search_string(pkg['summary'])
            filtered_description = filter_search_string(pkg['description'])

            if pkg['name'] != filtered_name:
                print("%d: indexing %s as %s" % (i, pkg['name'], filtered_name) )
            else:
                print("%d: indexing %s" % (i, pkg['name']))

            doc.fields.append(xappy.Field('exact_name', 'EX__' + filtered_name + '__EX', weight=10.0))

            name_parts = filtered_name.split('_')
            for i in range(20):
                if len(name_parts) > 1:
                    for part in name_parts:
                        doc.fields.append(xappy.Field('name', part, weight=1.0))
                doc.fields.append(xappy.Field('name', filtered_name, weight=10.0))
            doc.fields.append(xappy.Field('summary', filtered_summary, weight=1.0))
            doc.fields.append(xappy.Field('description', filtered_description, weight=0.2))

            self.index_files(doc, pkg)
            self.index_tags(doc, pkg)

            for sub_pkg in pkg['sub_pkgs']:
                i += 1
                filtered_sub_pkg_name = filter_search_string(sub_pkg['name'])
                if filtered_sub_pkg_name != sub_pkg['name']:
                    print("%d:    indexing subpkg %s as %s" % (i, sub_pkg['name'], filtered_sub_pkg_name))
                else:
                    print("%d:    indexing subpkg %s" % (i, sub_pkg['name']))

                doc.fields.append(xappy.Field('subpackages', filtered_sub_pkg_name, weight=1.0))
                doc.fields.append(xappy.Field('exact_name', 'EX__' + filtered_sub_pkg_name + '__EX', weight=10.0))

                self.index_files(doc, sub_pkg)
                self.index_tags(doc, sub_pkg)

                # remove anything we don't want to store
                del sub_pkg['pkg']

            # @@: Right now we're only indexing the first part of the
            # provides/requires, and not boolean comparison or version
            #for requires in pkg.requires:
            #    print requires[0]
            #    doc.fields.append(xappy.Field('requires', requires[0]))
            #for provides in pkg.provides:
            #    doc.fields.append(xappy.Field('provides', provides[0]))


            # remove anything we don't want to store and then store data in
            # json format
            del pkg['pkg']
            del pkg['src_pkg']

            processed_doc = self.iconn.process(doc, False)
            processed_doc._doc.set_data(json.dumps(pkg))
            # preempt xappy's processing of data
            processed_doc._data = None
            self.iconn.add(processed_doc)

        self.icon_cache.close()

        return i

def run(cache_path, yum_conf, tagger_url=None, pkgdb_url=None):
    indexer = Indexer(cache_path, yum_conf, tagger_url, pkgdb_url)

    print "Indexing packages from Yum..."
    count = indexer.index_pkgs()
    print "Indexed %d packages." % count

if __name__ == '__main__':
    run('index_cache', join(dirname(__file__), 'yum.conf'), 'http://community.dev.fedoraproject.org/tagger/dump')
