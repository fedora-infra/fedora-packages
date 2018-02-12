import json
import os
import pytest
import xapian

from fedoracommunity.search import index


pkg_guake = {'branch': 'f27',
             'status': True,
             'name': 'guake',
             'summary': 'Drop-down terminal for GNOME',
             'description': 'Guake is a drop-down terminal for Gnome Desktop '
                            'Environment,\nso you just need to press a key to '
                            'invoke him,\nand press again to hide.',
             'devel_owner': 'pingou',
             'icon': 'package_128x128.png',
             'package': None,
             'upstream_url': 'http://guake-project.org/',
             'sub_pkgs': []}


def search(query):
    """ Helper function to query a xapian db """
    db = xapian.Database('/tmp/xapian/search')
    enquire = xapian.Enquire(db)
    qp = xapian.QueryParser()
    qp.set_database(db)
    flags = xapian.QueryParser.FLAG_DEFAULT | \
        xapian.QueryParser.FLAG_PARTIAL | \
        xapian.QueryParser.FLAG_WILDCARD
    query = qp.parse_query(query, flags)

    enquire.set_query(query)
    matches = enquire.get_mset(0, 10)

    results = []
    for m in matches:
        results.append(json.loads(m.document.get_data()))

    return results


@pytest.fixture(scope='module')
def indexer():
    """ Helper fixture that create an indexer for
    the xapian db
    """
    indexer = index.Indexer('/tmp/xapian/')
    return indexer


def test_Indexer_create_index(delete_xapian_db):
    """ Test the _create_index method
    We create a xapian db that is used after by the other
    test
    """
    assert os.path.isdir('/tmp/xapian/search') is False
    index.Indexer('/tmp/xapian/')
    assert os.path.isdir('/tmp/xapian/search') is True


@pytest.mark.vcr()
def test_Indexer_get_active_fedora_release(indexer):
    """ Test the _get_active_fedora_release """
    active_releases = indexer._get_active_fedora_releases()
    assert active_releases == [27, 26]


@pytest.mark.vcr()
def test_Indexer_latest_active(indexer):
    """ Test the latest_active method """
    branch_info = indexer.latest_active('guake')
    assert branch_info == {'active': True,
                           'critical_path': False,
                           'global_component': 'guake',
                           'id': 328539,
                           'name': 'f27',
                           'slas': [
                               {'eol': '2018-11-24', 'id': 656966, 'sla': 'bug_fixes'},
                               {'eol': '2018-11-24', 'id': 656965, 'sla': 'security_fixes'}],
                           'type': 'rpm'}


@pytest.mark.vcr()
def test_Indexer_construct_package_dictionary(indexer):
    """ Test the construct_package_dictionary method """
    pkg = {'name': 'guake'}
    pkg_dict = indexer.construct_package_dictionary(pkg)
    assert pkg_dict == pkg_guake


@pytest.mark.vcr()
def test_Indexer_create_document(indexer):
    """ Test the indexer _create_document method
    use the search function to make sure the index worked
    and we return the correct results
    """
    pkgs = [{'name': 'vim'}, {'name': 'origin'}, {'name': 'bodhi'},
            {'name': 'firefox'}, {'name': 'hexchat'}, {'name': 'vim-taglist'},
            {'name': 'vim-jedi'}]
    packages = []
    for pkg in pkgs:
        packages.append(indexer.construct_package_dictionary(pkg))
    for package in packages:
        indexer._create_document(package)
    indexer.db.close()

    # Validate the indexing by doing some query
    # Search the name
    results = search('vim')
    assert len(results) == 3
    assert results[0]['name'] == 'vim'

    # Search the name (exact name return only vim)
    results = search('EX__vim__EX')
    assert len(results) == 1
    assert results[0]['name'] == 'vim'

    # Search the summary
    results = search('Openshift Origin')
    assert len(results) == 1
    assert results[0]['name'] == 'origin'

    # Search the description
    results = search('graphical IRC')
    assert len(results) == 1
    assert results[0]['name'] == 'hexchat'

    # gedit was not indexed so no result is expected
    results = search('gedit')
    assert len(results) == 0

    # search sub packages
    results = search('bodhi-client')
    assert len(results) == 1
    assert results[0]['name'] == 'bodhi'
    assert results[0]['sub_pkgs'][0]['name'] == 'bodhi-client'

    # search point of contact (poc has to be exact match)
    results = search('EX__phracek__EX')
    assert len(results) == 2
    assert results[0]['name'] == 'vim-jedi'
    assert results[1]['name'] == 'vim-taglist'
