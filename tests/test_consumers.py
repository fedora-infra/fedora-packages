import fedmsg.config
import json
import mock
import pytest
import xapian

from fedoracommunity.consumers import CacheInvalidator

msg = {
  "topic": "org.fedoraproject.prod.mdapi.repo.update",
  "msg": {
    "packages": ["guake"]}
  }

pkg_guake = {'name': 'guake',
             'summary': 'Drop-down terminal for GNOME',
             'description': 'Guake is a drop-down terminal for Gnome Desktop Environment',
             'devel_owner': 'pingou',
             'icon': 'guake',
             'package': None,
             'upstream_url': 'http://guake.org/',
             'sub_pkgs': []}


class MockHub(mock.MagicMock):
    """ Class that mock a fedmsg hub """
    config = fedmsg.config.load_config()
    config['fedoracommunity.fedmsg.consumer.enabled'] = True


def test_CacheInvalidator_new_package(create_xapian_db, mocker):
    """ Test that the update_xapian method
    creates a new xapian document when we receive
    an update from a new package.
    """
    mocker.patch('fedoracommunity.consumers.find_config_file',
                 return_value='/usr/share/fedoracommunity/tests/config.py')
    mocker.patch('fedoracommunity.search.index.Indexer.pull_icons')
    mocker.patch('fedoracommunity.search.index.Indexer.cache_icons')
    mocker.patch('fedoracommunity.search.index.Indexer.index_files_of_interest')
    mocker.patch(
        'fedoracommunity.search.index.Indexer.construct_package_dictionary',
        return_value=pkg_guake)

    consumer = CacheInvalidator(MockHub())
    consumer.update_xapian(msg)
    db = xapian.Database('/tmp/xapian/search')
    last_doc = db.get_lastdocid()
    data = json.loads(db.get_document(last_doc).get_data())
    assert data['name'] == 'guake'
    assert data['devel_owner'] == 'pingou'
    assert db.get_doccount() == 1


def test_CacheInvalidator_update_package(mocker):
    """ Test that the update_xapian method updates
    the xapian document when we recieve an update from
    fedmsg """

    pkg_guake_update = {'name': 'guake',
                        'summary': 'Drop-down terminal for GNOME',
                        'description': 'Guake is a drop-down terminal for Gnome Desktop Environment',
                        'devel_owner': 'cverna',
                        'icon': 'guake',
                        'package': None,
                        'upstream_url': 'http://guake.org/',
                        'sub_pkgs': []}

    mocker.patch('fedoracommunity.consumers.find_config_file',
                 return_value='/usr/share/fedoracommunity/tests/config.py')
    mocker.patch('fedoracommunity.search.index.Indexer.pull_icons')
    mocker.patch('fedoracommunity.search.index.Indexer.cache_icons')
    mocker.patch('fedoracommunity.search.index.Indexer.index_files_of_interest')
    mocker.patch(
        'fedoracommunity.search.index.Indexer.construct_package_dictionary',
        return_value=pkg_guake_update)

    consumer = CacheInvalidator(MockHub())
    consumer.update_xapian(msg)
    db = xapian.Database('/tmp/xapian/search')
    last_doc = db.get_lastdocid()
    data = json.loads(db.get_document(last_doc).get_data())
    assert data['name'] == 'guake'
    # POC was successfully updated
    assert data['devel_owner'] == 'cverna'
    # We still have only one document in the database
    assert db.get_doccount() == 1


@pytest.fixture(params=[
    {"topic": "org.fedoraproject.prod.mdapi.wrong.topic",
     "msg": {"packages": ["guake"]}},
    {"topic": "org.fedoraproject.prod.mdapi.repo.update",
     "msg": {"wrong": ["guake"]}},
    {"topic": "org.fedoraproject.prod.mdapi.repo.update",
     "msg": {"wrong": [""]}},
    ])
def test_wrong_fedmsg(request):
    return request.param


def test_CacheInvalidator_wrong_fedmsg(mocker, test_wrong_fedmsg):
    """ Test that the update_xapian method
    returns whith a wrong fedmsg message
    Case 1 : Wrong topic
    Case 2 : Wrong msg format
    Case 3 : No package name in the msg
    """

    mocker.patch('fedoracommunity.consumers.find_config_file',
                 return_value='/usr/share/fedoracommunity/tests/config.py')
    mocker.patch('fedoracommunity.search.index.Indexer.pull_icons')
    mocker.patch('fedoracommunity.search.index.Indexer.cache_icons')
    mocker.patch('fedoracommunity.search.index.Indexer.index_files_of_interest')
    mocker.patch(
        'fedoracommunity.search.index.Indexer.construct_package_dictionary',
        return_value=pkg_guake)

    consumer = CacheInvalidator(MockHub())
    consumer.update_xapian(test_wrong_fedmsg)

    db = xapian.Database('/tmp/xapian/search')
    last_doc = db.get_lastdocid()
    data = json.loads(db.get_document(last_doc).get_data())
    # POC was not changed
    assert data['devel_owner'] == 'cverna'
    # We still have only one document in the database
    assert db.get_doccount() == 1
