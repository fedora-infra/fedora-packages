#!/bin/bash

pushd /usr/share/fedoracommunity/
python setup.py install
popd
export GIT_PYTHON_REFRESH=quiet
dumb-init httpd -DFOREGROUND
