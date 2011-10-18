#!/usr/bin/env python
"""
Creates our search index and its field structure,
and then populates it with packages from yum repositories
"""

import xappy
from utils import filter_search_string

try:
    import json
except ImportError:
    import simplejson as json

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
    # FieldActions.TAG not currently supported in F15 xapian (1.2.7)
    #iconn.add_field_action('tags', xappy.FieldActions.TAG)
    iconn.add_field_action('tag', xappy.FieldActions.INDEX_EXACT)

    #iconn.add_field_action('requires', xappy.FieldActions.INDEX_EXACT)
    #iconn.add_field_action('provides', xappy.FieldActions.INDEX_EXACT)

    iconn.close()

"""
index_yum_pkgs

Index the packages from yum into this format:

   {base_package_name: {'name': base_package_name,
                        'summary': base_package_summary,
                        'description': base_package_summary,
                        'pkg': pkg,
                        'sub_pkgs': [{'name': sub_pkg_name,
                                      'summary': sub_pkg_summary,
                                      'description': sub_pkg_description},
                                     ...]},
    ...
   }
"""
def index_yum_pkgs():
    import yum
    yb = yum.YumBase()
    yb.disablePlugins()
    yb.conf.cache = 1

    pkgs = yb.pkgSack.returnPackages()
    base_pkgs = {}
    seen_pkg_names = []

    for pkg in pkgs:
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
        else:
            # this is a sub package
            subpkgs = base_pkg['sub_pkgs']
            subpkgs.append({'name': pkg.name, 'summary': pkg.summary, 'description': pkg.description})

    return base_pkgs

def index_pkgs(iconn):
    yum_pkgs = index_yum_pkgs()
    i = 0

    for pkg in yum_pkgs.values():
        i += 1

        doc = xappy.UnprocessedDocument()
        filtered_name = filter_search_string (pkg['name'])
        filtered_summary = filter_search_string (pkg['summary'])
        filtered_description = filter_search_string (pkg['description'])
        doc.fields.append(xappy.Field('exact_name', 'EX__' + filtered_name + '__EX', weight=2.0))
        doc.fields.append(xappy.Field('name', filtered_name, weight=2.0))
        doc.fields.append(xappy.Field('summary', filtered_summary, weight=1.0))
        doc.fields.append(xappy.Field('description', filtered_description, weight=0.2))
        for sub_pkg in pkg['sub_pkgs']:
            filtered_sub_pkg_name = filter_search_string (sub_pkg['name'])
            doc.fields.append(xappy.Field('subpackages', filtered_sub_pkg_name, weight=1.0))

        # @@: Right now we're only indexing the first part of the
        # provides/requires, and not boolean comparison or version
        #for requires in pkg.requires:
        #    print requires[0]
        #    doc.fields.append(xappy.Field('requires', requires[0]))
        #for provides in pkg.provides:
        #    doc.fields.append(xappy.Field('provides', provides[0]))

        # Figure out if this package is a desktop application
        yum_pkg = pkg['pkg']
        if yum_pkg != None:
            for filename in yum_pkg.filelist:
                if filename.endswith('.desktop'):
                    print "Desktop app found: %s" % yum_pkg.name
                    doc.fields.append(xappy.Field('tag', 'desktop'))
                    break

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
