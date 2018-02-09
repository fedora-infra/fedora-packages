import pytest
import os
import shutil
import xapian


@pytest.fixture(scope='module')
def delete_xapian_db():
    if os.path.isdir('/tmp/xapian/search'):
        shutil.rmtree('/tmp/xapian/search')


@pytest.fixture(scope='module')
def create_xapian_db():
    """ Fixture that creates an empty xapian db """

    db = xapian.WritableDatabase('/tmp/xapian/search', xapian.DB_CREATE_OR_OPEN)
    db.close()
