#!/usr/bin/env python

import sys
import xappy

def open_index(dbpath):
    return xappy.SearchConnection(dbpath)

def search(query, start=0, limit=10):
    """ A method to perform a simple query on our xapian database """
    dbpath = 'xapian'
    sconn = open_index(dbpath)
    print "Searching %d documents for \"%s\"" % (
        sconn.get_doccount(), query)

    q = sconn.query_parse(query, default_op=sconn.OP_AND)
    print str(q)
    print

    results = sconn.query(q, start, limit)
    if results.estimate_is_exact:
        print "Found %d results" % results.matches_estimated
    else:
        print "Found approximately %d results" % results.matches_estimated

    for result in results:
        print result
        print

if __name__ == '__main__':
    search(' '.join(sys.argv[1:]))
