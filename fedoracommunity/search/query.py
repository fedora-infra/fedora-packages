#!/usr/bin/env python

import sys
import xapian
import json

def search(query, start=0, limit=10):
    """ A method to perform a simple query on our xapian database """
    db = xapian.Database('xapian')
    enquire = xapian.Enquire(db)
    qp = xapian.QueryParser()
    qp.set_database(db)
    qp.set_default_op(xapian.Query.OP_ELITE_SET)
    query = qp.parse_query(query)

    enquire.set_query(query)
    matches = enquire.get_mset(start, limit);

    count = matches.get_matches_estimated()
    rows = []
    for m in matches:
        print m.percent, m.rank, m.weight
        result = json.loads(m.document.get_data())
        rows.append(result)
        print result['name']

if __name__ == '__main__':
    search_terms = ' '.join(sys.argv[1:])
    for term in sys.argv[1:]:
        search_terms += " EX__%s__EX" % term

    search(search_terms)
