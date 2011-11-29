""" Loading moksha-ctl config from file (and the defaults!) """

import os
import sys
import textwrap
import ConfigParser

EXAMPLE_CTL_CONF = """
# An example ~/.moksha/ctl.conf could look like this
[fcomm]
venv = fcomm
fcomm-src-dir = /home/user/devel/fedoracommunity
moksha-src-dir = /home/user/devel/moksha
"""

def load_config(fname="~/.moksha/ctl.conf"):
    """ Load a config file into a dictionary and return it """

    # Defaults
    config_d = {
        'venv': 'fcomm',
        'apps-dir': 'moksha/apps',
        'fcomm-src-dir': os.getcwd(),
        'moksha-src-dir': os.getcwd() + '/../moksha'
    }

    config = ConfigParser.ConfigParser()

    fname = os.path.expanduser(fname)
    if not os.path.exists(fname):
        # If moksha is already checked out alongside of us, then automatically
        # generate the config.
        mokshadir = os.path.abspath(os.path.join('..', 'moksha'))
        if os.path.isdir(mokshadir):
            mokshacfgdir = os.path.dirname(fname)
            if not os.path.isdir(mokshacfgdir):
                os.makedirs(mokshacfgdir)
            cfg = file(fname, 'w')
            cfg.write(textwrap.dedent("""\
                [fcomm]
                venv = fcomm
                fcomm-src-dir = %s
                moksha-src-dir = %s
            """ % (os.getcwd(), mokshadir)))
            cfg.close()
        else:
            print "No such file '%s'" % fname
            print EXAMPLE_CTL_CONF
            sys.exit(1)

    with open(fname) as f:
        config.readfp(f)

    if not config.has_section('fcomm'):
        print "'%s' has no [fcomm] section" % fname
        print EXAMPLE_CTL_CONF
        sys.exit(1)

    # Extract all defined fields
    for key in ['moksha-src-dir', 'fcomm-src-dir', 'venv', 'apps-dir']:
        if config.has_option('fcomm', key):
            config_d[key] = config.get('fcomm', key)

    return config_d
