# Link in a module in the global Python site-packages the virtualenv that we are currently in
# Author: Luke Macken <lmacken@redhat.com>

import os
import sys

from glob import glob
from distutils.sysconfig import get_python_lib

def symlink_global_module_into_virtualenv(modulename, env):
    for path in (get_python_lib(), get_python_lib(1)):
        for modpath in glob(os.path.join(path, modulename) + '*'):
            dest = os.path.join(env, path.replace('/usr/', ''), os.path.basename(modpath))
            if os.path.exists(dest):
                assert os.path.islink(dest)
            else:
                print "%s => %s" % (modpath, dest)
                os.symlink(modpath, dest)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s <virtualenv> <modulename>" % sys.argv[0]
        sys.exit(2)

    env = os.environ.get('VIRTUAL_ENV')
    if env:
        print "You must deactivate your virtualenv first"
        sys.exit(1)

    prog, env, module = sys.argv

    symlink_global_module_into_virtualenv(module, env)
