#!/bin/bash

pushd /usr/share/fedoracommunity/
python setup.py install
popd
export GIT_PYTHON_REFRESH=quiet
echo "http://0.0.0.0/packages"
dumb-init httpd -DFOREGROUND
