#!/usr/bin/env python
"""
Creates our search index and its field structure,
and then populates it with packages from yum repositories
"""

import xappy

def create_index(dbpath):
    """ Create a new index, and set up its field structure """
    iconn = xappy.IndexerConnection(dbpath)

    #iconn.add_field_action('package', xappy.FieldActions.INDEX_EXACT)

    iconn.add_field_action('name', xappy.FieldActions.STORE_CONTENT)
    iconn.add_field_action('name', xappy.FieldActions.INDEX_FREETEXT,
                           language='en', weight=2)

    iconn.add_field_action('summary', xappy.FieldActions.STORE_CONTENT)
    iconn.add_field_action('summary', xappy.FieldActions.INDEX_FREETEXT,
                           language='en')

    iconn.add_field_action('description', xappy.FieldActions.INDEX_FREETEXT,
                           language='en')

    # FieldActions.TAG not currently supported in F15 xapian (1.2.7)
    #iconn.add_field_action('tags', xappy.FieldActions.TAG)
    iconn.add_field_action('tag', xappy.FieldActions.INDEX_EXACT)

    #iconn.add_field_action('requires', xappy.FieldActions.INDEX_EXACT)
    #iconn.add_field_action('provides', xappy.FieldActions.INDEX_EXACT)

    iconn.close()

def index_yum_pkgs(iconn):
    import yum
    yb = yum.YumBase()
    yb.disablePlugins()
    yb.conf.cache = 1
    #yb.pkgSack.excludeArchs(['x86_64', 'noarch']) # skip dupes across arches
    packages = set()
    pkgs = sorted(yb.pkgSack.returnPackages())
    i = 0
    for pkg in pkgs:
        # Skip dupes for varous arches
        if pkg.name in packages:
            continue
        packages.add(pkg.name)
        i += 1

        doc = xappy.UnprocessedDocument()
        doc.fields.append(xappy.Field('name', pkg.name))
        #doc.fields.append(xappy.Field('package', pkg.name))
        doc.fields.append(xappy.Field('summary', pkg.summary))
        doc.fields.append(xappy.Field('description', pkg.description))

        # @@: Right now we're only indexing the first part of the
        # provides/requires, and not boolean comparison or version
        #for requires in pkg.requires:
        #    print requires[0]
        #    doc.fields.append(xappy.Field('requires', requires[0]))
        #for provides in pkg.provides:
        #    doc.fields.append(xappy.Field('provides', provides[0]))

        # Figure out if this package is a desktop application
        for filename in pkg.filelist:
            if filename.endswith('.desktop'):
                print "Desktop app found: %s" % pkg.name
                doc.fields.append(xappy.Field('tag', 'desktop'))
                break

        iconn.add(doc)

    return i

def open_index(dbpath):
    """ Open an existing index """
    return xappy.IndexerConnection(dbpath)

def main():
    dbpath = 'xapian'
    create_index(dbpath)
    iconn = open_index(dbpath)
    print "Indexing packages from Yum..."
    count = index_yum_pkgs(iconn)
    print "Indexed %d packages." % count

if __name__ == '__main__':
    main()
