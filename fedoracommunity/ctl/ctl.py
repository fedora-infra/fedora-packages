""" Functions for fcomm-ctl """
import decorator
import os
import sys

# Local imports
import config
import colors as c
import utils


# load the fedoracommunity config
ctl_config = config.load_config()

# Add moksha's src dir to the path so we can import it
sys.path.insert(0, ctl_config['moksha-src-dir'])

# Import moksha from its source directory
import moksha.ctl.core.ctl as moksha_ctl

# Override moksha config with fedoracommunity config
moksha_ctl.ctl_config.update(ctl_config)

PRETTY_PREFIX = "[ " + c.magenta("fcomm-ctl") + " ] "


@decorator.decorator
def _with_virtualenv(func, *args, **kwargs):
    import virtualenvcontext
    with virtualenvcontext.VirtualenvContext(ctl_config['venv']):
        return func(*args, **kwargs)


@decorator.decorator
def _in_srcdir(func, *args, **kwargs):
    with utils.DirectoryContext(ctl_config['fcomm-src-dir']):
        return func(*args, **kwargs)

@decorator.decorator
def _with_moksha_faked(func, *args, **kwargs):
    ret = True

    # Do what moksha do, but don't change directory
    moksha_ctl.ctl_config['moksha-src-dir'] = ctl_config['fcomm-src-dir']

    # Call the function by name
    ret = getattr(moksha_ctl, func.__name__)(*args, **kwargs)

    moksha_ctl.ctl_config['moksha-src-dir'] = ctl_config['moksha-src-dir']

    # Go on with our fcomm business
    return func(*args, **kwargs) and ret

@decorator.decorator
def _with_moksha_first(func, *args, **kwargs):
    ret = True

    with utils.DirectoryContext(ctl_config['moksha-src-dir']):
        # Call the function by name
        ret = getattr(moksha_ctl, func.__name__)(*args, **kwargs)

    # Go on with our fcomm business
    return func(*args, **kwargs) and ret

@decorator.decorator
def _reporter(func, *args, **kwargs):
    PRETTY_PREFIX = "[" + c.magenta("fcomm-ctl") + "] "
    descriptor = ":".join([func.__name__] + [a for a in args if a])
    print PRETTY_PREFIX, "Running:", descriptor
    output = None
    try:
        output = func(*args, **kwargs)
        if not output:
            raise Exception
        print PRETTY_PREFIX, "[ " + c.green('OK') + " ]", descriptor
    except Exception:
        print PRETTY_PREFIX, "[ " + c.red('FAIL') + " ]", descriptor
    return output


@_reporter
@_with_moksha_first
def bootstrap():
    """ Should only be run once. First-time moksha setup. """
    ret = True
    if os.path.exists('/etc/redhat-release'):
        reqs = [
            'python-kitchen', 'python-fedora', 'python-bugzilla', 'koji',
            'xapian-bindings-python',
        ]
        ret = ret and not os.system(
            'sudo yum install -q -y ' + ' '.join(reqs))

    print PRETTY_PREFIX, "Scratch that."
    print "Really, run './fcomm-ctl.py rebuild' to continue."
    return ret


@_reporter
@_with_moksha_first
def rebuild():
    """ Completely destroy and rebuild the virtualenv. """
    return install_hacks() and link_external_libs() and develop() and download_db_snapshot()


@_reporter
def download_db_snapshot():
    """ Download a snapshot of our xapian database """
    os.system('wget -N http://johnp.fedorapeople.org/downloads/xapian/xapian-LATEST.tar.xz')
    os.system('tar xvf xapian-LATEST.tar.xz')
    return True


@_reporter
@_with_moksha_first
@_with_virtualenv
def install_hacks():
    """ Install dependencies with weird workarounds. """
    # Checkout and install the latest xappy
    if not os.path.isdir('xappy'):
        os.system('svn checkout http://xappy.googlecode.com/svn/trunk/ xappy')
    with utils.DirectoryContext('xappy'):
        os.system('%s setup.py install' % sys.executable)
    return True


@_reporter
def link_external_libs():
    """ Link rpm modules in from the system site-packages. """
    location = 'python{major}.{minor}/site-packages'.format(
        major=sys.version_info.major, minor=sys.version_info.minor)
    template = 'ln -s /usr/{location}/{lib} {workon}/{venv}/{location}/'
    for lib in ['koji', 'rpm', 'rpmUtils', 'fedora', 'kitchen', 'pycurl', 'yum', 'urlgrabber',
                'sqlitecachec', '_sqlitecache', 'bugzilla', 'xapian']:
        for libdir in ('lib64', 'lib'):
            for ext in ('.py', '.so', ''):
                mod = '/usr/%s/%s/%s%s' % (libdir, location, lib, ext)
                if os.path.exists(mod):
                    template = 'ln -s /usr/{libdir}/{location}/{lib}{ext} {workon}/{venv}/{libdir}/{location}/'
                    cmd = template.format(
                        libdir=libdir, ext=ext,
                        location=location, venv=ctl_config['venv'], lib=lib,
                        workon=os.getenv("WORKON_HOME"))
                    print cmd
                    out = os.system(cmd)
    # TODO -- test for success
    return True


@_reporter
@_with_moksha_first
@_with_virtualenv
@_in_srcdir
def develop():
    """ `python setup.py develop` """
    ret = True
    ret = ret and not os.system('%s setup.py develop' % sys.executable)
    ret = ret and not os.system('%s setup.py install' % sys.executable)
    if not os.path.isdir('logs'):
        os.makedirs('logs')
    return ret


@_reporter
@_with_moksha_faked
def start(service='paster'):
    """ Start paster. """
    return True


@_reporter
@_with_moksha_faked
def stop(service='paster'):
    """ Stop paster, orbited, and moksha-hub. """
    return True


@_with_moksha_faked
def logs():
    """ Watch colorized logs of paster, orbited, and moksha-hub """
    return True
