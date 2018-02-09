import os
import pytest

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


@pytest.fixture(scope='module')
def indexer():
    indexer = index.Indexer('/tmp/xapian/')
    return indexer


def test_Indexer_create_index(delete_xapian_db):
    assert os.path.isdir('/tmp/xapian/search') is False
    index.Indexer('/tmp/xapian/')
    assert os.path.isdir('/tmp/xapian/search') is True


@pytest.mark.vcr()
def test_Indexer_get_active_fedora_release(indexer):
    active_releases = indexer._get_active_fedora_releases()
    assert active_releases == [27, 26]


@pytest.mark.vcr()
def test_Indexer_latest_active(indexer):

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
    pkg = {'name': 'guake'}
    pkg_dict = indexer.construct_package_dictionary(pkg)
    assert pkg_dict == pkg_guake
