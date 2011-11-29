""" Various moksha-ctl utils. Mostly context managers. """

import os


def install_distributions(distributions):
    """ Installs distributions with pip! """

    import pip.commands.install

    command = pip.commands.install.InstallCommand()
    opts, args = command.parser.parse_args()

    opts.use_mirrors = True
    opts.mirrors = [
        'b.pypi.python.org',
        'c.pypi.python.org',
        'd.pypi.python.org',
        'e.pypi.python.org',
    ]
    opts.build_dir = os.path.expanduser('~/.pip/build')
    try:
        os.mkdir(opts.build_dir)
    except OSError as e:
        pass

    requirement_set = command.run(opts, distributions)
    requirement_set.install([])


class DirectoryContext(object):
    """ Context manager for changing the path working directory """
    def __init__(self, directory):
        self.dirname = directory
        self.old_path = None

    def __enter__(self):
        if self.old_path:
            raise ValueError("Weird. old_path should be None")
        self.old_path = os.getcwd()
        os.chdir(self.dirname)

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.old_path)
        self.old_path = None
