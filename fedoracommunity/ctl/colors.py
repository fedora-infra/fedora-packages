""" Color functions for moksha-ctl.

Looks for fabulous and fails gracefully if its not installed.
"""

fabu = None
try:
    import fabulous.color as fabu
except ImportError as e:
    pass


def _color(col, s):
    return getattr(fabu, col, lambda _s: _s)(s)


def cyan(s):
    return _color('cyan', s)


def red(s):
    return _color('red', s)


def green(s):
    return _color('green', s)


def yellow(s):
    return _color('yellow', s)


def magenta(s):
    return _color('magenta', s)
