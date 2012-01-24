#!/usr/bin/env python
# A script to keep our git repos up to date

import os, shutil, subprocess
from fedora.client.pkgdb import PackageDB

REPO_DIR = '/var/cache/fedoracommunity/git.fedoraproject.org'

# Get a list of active git branches
pkgdb = PackageDB()
collections = pkgdb.get_collection_list(eol=False)
active = [c[0].gitbranchname for c in collections]

for repo in os.listdir(REPO_DIR):
    print("[ %s ]" % repo)
    for branch in os.listdir(os.path.join(REPO_DIR, repo)):
        if branch in active:
            subprocess.call('git pull', shell=True,
                    cwd=os.path.join(REPO_DIR, repo, branch))
        else:
            print("Deleting EOL branch %s" % branch)
            shutil.rmtree(os.path.join(REPO_DIR, repo, branch))
