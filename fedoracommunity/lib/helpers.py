def parse_build(build):
    """
    >>> nvr = parse_build('python-sqlalchemy-0.4.8-1.fc10.noarch')
    >>> nvr['name']
    'python-sqlalchemy'
    >>> nvr['version']
    '0.4.8'
    >>> nvr['release']
    '1.fc10'
    >>> nvr['arch']
    'noarch'
    """
    chunks = build.split('-')
    return {
            'name': '-'.join(chunks[:-2]),
            'version': '-'.join(chunks[-2:-1]),
            'release': '.'.join(chunks[-1].split('.')[:-1]),
            'arch': chunks[-1].split('.')[-1],
            }
