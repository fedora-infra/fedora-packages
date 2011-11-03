#!/usr/bin/env python
"""
Creates our search index and its field structure,
and then populates it with packages from yum repositories
"""
import os
import sys
import shutil
import tempfile
import xappy
import re

from utils import filter_search_string
from fedora.client import ProxyClient, PackageDB

# how many time to retry a downed server
MAX_RETRY = 10

_pkgdb_client = ProxyClient('https://admin.fedoraproject.org/pkgdb',
                            session_as_cookie=False,
                            insecure=False)


try:
    import json
except ImportError:
    import simplejson as json

cache_dir = "cache"

class DesktopParser(object):
    key_value_re = re.compile('([A-Za-z0-9-]*)[ ]*=[ ]*(.*)')
    def __init__(self, file_name):
        object.__init__(self)
        self._entries = {}
        self.parse(file_name)

    def get(self, entry_key, default=''):
        return self._entries.get(entry_key, default)

    def parse(self, file_name):
        dfile = open(file_name, 'r')
        for line in dfile:
            if line.startswith('#') or line.startswith(' ') or line.startswith('['):
                continue
            m = self.key_value_re.match(line)
            if m:
                key = m.group(1)
                value = m.group(2)
                self._entries[key] = value

        dfile.close()

def create_index(dbpath):
    """ Create a new index, and set up its field structure """
    iconn = xappy.IndexerConnection(dbpath)

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
    iconn.add_field_action('tag', xappy.FieldActions.INDEX_EXACT)

    #iconn.add_field_action('requires', xappy.FieldActions.INDEX_EXACT)
    #iconn.add_field_action('provides', xappy.FieldActions.INDEX_EXACT)

    iconn.close()

def find_devel_owner(pkg_name, retry=0):
    print "not cached yet"
    return "not cached yet"
    pkginfo = _pkgdb_client.send_request('/acls/name',
                                         req_params = {'packageName': pkg_name,
                                                       'collectionName': 'Fedora',
                                                       'collectionVersion': 'devel'})

    pkginfo = pkginfo[1]
    try:
        for pkg in pkginfo['packageListings']:
            if pkg['collection']['branchname'] == 'devel':
                print 'owner %s' % pkg['owner']
                return pkg['owner']
    except KeyError:
        print('no owner')
        return ''
    except ServerError:
        if retry <= MAX_RETRY:
            return find_devel_owner(pkg_name, retry + 1)

        print('owner: server error')
        return None

    print ''

"""
index_yum_pkgs

Index the packages from yum into this format:

   {base_package_name: {'name': base_package_name,
                        'summary': base_package_summary,
                        'description': base_package_summary,
                        'pkg': pkg,
                        'sub_pkgs': [{'name': sub_pkg_name,
                                      'summary': sub_pkg_summary,
                                      'description': sub_pkg_description,
                                      'pkg': pkg},
                                     ...]},
    ...
   }
"""
def index_yum_pkgs():
    import yum
    yb = yum.YumBase()

    # Doesn't work right now due to a bug in yum.
    # https://bugzilla.redhat.com/show_bug.cgi?id=750593
    #yb.disablePlugins()

    # Temporary work around
    yb.preconf.disabled_plugins = '*'

    yb.conf.cache = 1

    pkgs = yb.pkgSack.returnPackages()
    base_pkgs = {}
    seen_pkg_names = []

    i = 0
    for pkg in pkgs:
        i += 1
        print "%d: pre-processing package '%s':" % (i, pkg['name']), 
        if not pkg.base_package_name in base_pkgs:
            # we haven't seen this base package yet so add it
            base_pkgs[pkg.base_package_name] = {'name': pkg.base_package_name,
                                                'summary': '',
                                                'description':'',
                                                'pkg': None,
                                                'sub_pkgs': []}

        base_pkg = base_pkgs[pkg.base_package_name]
        # avoid duplicates
        if pkg.name in seen_pkg_names:
            continue

        seen_pkg_names.append(pkg.name)

        if pkg.base_package_name == pkg.name:
            # this is the main package
            base_pkg['summary'] = pkg.summary
            base_pkg['description'] = pkg.description
            base_pkg['pkg'] = pkg
            base_pkg['devel_owner'] = find_devel_owner(pkg.name)
        else:
            # this is a sub package
            subpkgs = base_pkg['sub_pkgs']
            subpkgs.append({'name': pkg.name, 'summary': pkg.summary, 'description': pkg.description, 'pkg': pkg})

    return base_pkgs

def cache_rpm_contents():
    full_cache_dir = os.path.join(os.getcwd(), cache_dir)
    tmp_dir = tempfile.mkdtemp()

class RPMCache(object):
    def __init__(self, rpm_envra, cache_dir=cache_dir):
        if ':' in rpm_envra:
            rpm_envra = rpm_envra.split(':')[1]

        self.rpm_file_name = "%s.rpm" % rpm_envra
        self.rpm_envra = rpm_envra
        self.cache_dir = os.path.join(os.getcwd(), cache_dir)
        self.retry = 0

        # create cache dir if it does not exist
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

        self.tmp_dir = None

    def open(self):
        self.tmp_dir = tempfile.mkdtemp()
        self._download_rpm()
        self._extract_rpm()

    def _download_rpm(self):
        self.rpm_path = os.path.join(self.cache_dir, self.rpm_file_name)
        os.system('yumdownloader --destdir %s %s' % (self.cache_dir, self.rpm_envra))

    def _extract_rpm(self):
        push_dir = os.getcwd()
        os.chdir(self.tmp_dir)
        os.system('rpm2cpio %s | cpio -idm --no-absolute-filenames --quiet' % self.rpm_path)
        os.chdir(push_dir)

    def retry(self):
        if self.retry <= MAX_RETRY:
            self.retry += 1
            try:
                os.remove(self.rpm_path)                
            except OSError:
                pass
            self._download_rpm()
            self._extract_rpm()
            return True
        return False

    def close(self):
        shutil.rmtree(self.tmp_dir)

def index_desktop_file(doc, rpm_cache, filename):
    doc.fields.append(xappy.Field('tag', 'desktop'))
    
    def parse_desktop_file(file_path):
        dp = DesktopParser(file_path)
        category = dp.get('Categories', '')

        for c in category.split(';'):
            if c:
                c = filter_search_string(c)
                doc.fields.append(xappy.Field('category_tags', c))
                # add exact match also
                doc.fields.append(xappy.Field('category_tags', "EX__%s__EX" % c))

    desktop_file = rpm_cache.tmp_dir + filename

    def try_parse(desktop_file):
        if os.path.exists(desktop_file):
            parse_desktop_file(desktop_file)
        else:
            if rpm_cache.retry():
                print "Could not find '%s' trying to redownload" % tmp_file
                try_parse(desktop_file)
            else:
                print "Maximum retrys exceeded. Skipping desktop file parsing."

def index_files(doc, yum_pkg):
    if yum_pkg != None:
        desktop_file_cache = RPMCache(yum_pkg['ui_envra'])
        desktop_file_cache.open()
        for filename in yum_pkg.filelist:
            if filename.endswith('.desktop'):
                # index apps
                "        indexing desktop file %s" % os.path.basename(filename)
                index_desktop_file(doc, desktop_file_cache, filename)
            if filename.startswith('/usr/bin'):
                # index executables
                print ("        indexing exe file %s" % os.path.basename(filename))
                exe_name = filter_search_string(os.path.basename(filename))
                doc.fields.append(xappy.Field('cmd', "EX__%s__EX" % exe_name))

        desktop_file_cache.close()

def index_pkgs(iconn):
    yum_pkgs = index_yum_pkgs()
    i = 0

    for pkg in yum_pkgs.values():
        i += 1

        doc = xappy.UnprocessedDocument()
        filtered_name = filter_search_string (pkg['name'])
        filtered_summary = filter_search_string (pkg['summary'])
        filtered_description = filter_search_string (pkg['description'])

        if pkg['name'] != filtered_name:
            print("indexing %s as %s" % (pkg['name'], filtered_name) )
        else:
            print("indexing %s" % pkg['name'])

        doc.fields.append(xappy.Field('exact_name', 'EX__' + filtered_name + '__EX', weight=10.0))
        doc.fields.append(xappy.Field('name', filtered_name, weight=10.0))
        doc.fields.append(xappy.Field('summary', filtered_summary, weight=1.0))
        doc.fields.append(xappy.Field('description', filtered_description, weight=0.2))

        index_files(doc, pkg['pkg'])

        for sub_pkg in pkg['sub_pkgs']:
            filtered_sub_pkg_name = filter_search_string (sub_pkg['name'])
            if filtered_sub_pkg_name != sub_pkg['name']:
                print("    indexing subpkg %s as %s" % (sub_pkg['name'], filtered_sub_pkg_name))
            else:
                print("    indexing subpkg %s" % sub_pkg['name'])

            doc.fields.append(xappy.Field('subpackages', filtered_sub_pkg_name, weight=1.0))
            index_files(doc, sub_pkg['pkg'])

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

        processed_doc = iconn.process(doc, False)
        processed_doc._doc.set_data(json.dumps(pkg))
        # preempt xappy's processing of data
        processed_doc._data = None
        iconn.add(processed_doc)

    return i

def open_index(dbpath):
    """ Open an existing index """
    return xappy.IndexerConnection(dbpath)

def main():
    dbpath = 'xapian'
    create_index(dbpath)
    iconn = open_index(dbpath)
    print "Indexing packages from Yum..."
    count = index_pkgs(iconn)
    print "Indexed %d packages." % count

if __name__ == '__main__':
    main()
