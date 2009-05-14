def parse_build(build):
    """
    >>> nvr = parse_build('python-sqlalchemy-0.4.8-1.fc10')
    >>> nvr['name']
    'python-sqlalchemy'
    >>> nvr['version']
    '0.4.8'
    >>> nvr['release']
    '1.fc10'
    """
    chunks = build.split('-')
    return {
            'name': '-'.join(chunks[:-2]),
            'version': '-'.join(chunks[-2:-1]),
            'release': chunks[-1],
            'nvr': build,
           }
