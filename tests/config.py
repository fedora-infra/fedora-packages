#
# Fedora Packages - unit test configuration
#
[DEFAULT]
fedoracommunity.connector.xapian.package-search.db = /tmp/xapian/search

cache.connectors.backend=dogpile.cache.memcached
cache.connectors.expiration_time=30
cache.connectors.arguments.url=127.0.0.1:11211
cache.connectors.arguments.distributed_lock=False

[app:main]
use = egg:fedoracommunity
