#!/usr/bin/env python

import sys
import xapian
import cPickle

def search(query, start=0, limit=10):
    """ A method to perform a simple query on our xapian database """
    db = xapian.Database('xapian')
    enquire = xapian.Enquire(db)
    qp = xapian.QueryParser()
    qp.set_database(db)
    qp.set_default_op(xapian.Query.OP_ELITE_SET)
    qp.add_prefix('exact_name', 'XA')
    query = qp.parse_query(query)

    enquire.set_query(query)
    matches = enquire.get_mset(start, limit);

    count = matches.get_matches_estimated()
    rows = []
    for m in matches:
        print m.percent, m.rank, m.weight
        result = cPickle.loads(m.document.get_data())
        data, assocs, groups = result
        rows.append(data)
        print data['exact_name']

if __name__ == '__main__':
    search(' '.join(sys.argv[1:]))
