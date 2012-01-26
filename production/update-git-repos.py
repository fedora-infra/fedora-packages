#!/usr/bin/env python
# A script to keep our git repos up to date

import os, time, shutil, subprocess
from koji import ClientSession
from fedora.client.pkgdb import PackageDB

REPO_DIR = '/var/cache/fedoracommunity/git.fedoraproject.org'
TIMESTAMP = '/var/cache/fedoracommunity/git.fedoraproject.org/.timestamp'

# Get a list of active git branches
pkgdb = PackageDB()
collections = pkgdb.get_collection_list(eol=False)
active = [c[0].gitbranchname for c in collections]

# Grab a list of all koji builds since our last run
# if there is no saved timestamp, do a full run
packages = []
if not os.path.exists(TIMESTAMP):
    packages = os.listdir(REPO_DIR)
else:
    timestamp = file(TIMESTAMP).read().strip()
    koji = ClientSession('http://koji.fedoraproject.org/kojihub')
    builds = koji.listBuilds(queryOpts={'createdAfter': float(timestamp)})
    packages = set([build['name'] for build in builds])
    packages = [pkg for pkg in packages
                if os.path.isdir(os.path.join(REPO_DIR, pkg))]

for repo in packages:
    print("[ %s ]" % repo)
    for branch in os.listdir(os.path.join(REPO_DIR, repo)):
        if branch in active:
            subprocess.call('git pull', shell=True,
                    cwd=os.path.join(REPO_DIR, repo, branch))
        else:
            print("Deleting EOL branch %s" % branch)
            shutil.rmtree(os.path.join(REPO_DIR, repo, branch))

# save a timestamp of our last run
timestamp = file(TIMESTAMP, 'w')
timestamp.write(str(time.time()))
timestamp.close()
