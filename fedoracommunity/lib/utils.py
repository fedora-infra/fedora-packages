# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from UserDict import DictMixin
from tg import url, request

import paste

architectures = ('i386', 'x86_64', 'ppc', 'ppc64', 'noarch')

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

def fullurl(path):
    h = url(path)
    h = paste.request.resolve_relative_url(h, request.environ)

    return h

# git setuptools plugin
from subprocess import Popen, PIPE
def find_git_files(dir):
    try:
        p = Popen(["git-ls-files", dir], stdout=PIPE)
        files = p.stdout.readlines()
    except:
        return []

    results = []
    for f in files:
        results.append(f.strip())

    print "finding git files in dir %s" % dir
    return results

def _print_map(map, depth):
    tabstop = ''
    for i in xrange(depth):
        tabstop += '\t'
    print tabstop + '{'
    for k in map.keys():
        v = map[k]
        print tabstop + '\t' + str(k) + '=',
        if isinstance(v, dict):
            print ''
            _print_map(v, depth + 1)
        elif isinstance(v, list) or isinstance(v, tuple):
            print ''
            _print_array(v, depth + 1)
        else:
            print v

    print tabstop + '}'


def _print_array(array, depth):
    tabstop = ''
    for i in xrange(depth):
        tabstop += '\t'
    print tabstop + '['
    for a in array:
        if isinstance(a, dict):
            _print_map(a, depth + 1)
        elif isinstance(a, list) or isinstance(a, tuple):
            _print_array(a, depth + 1)
        else:
            print tabstop + '\t' + str(a)
    print tabstop + ']'

pretty_print_map = lambda m : _print_map(m, 0)
pretty_print_array = lambda a : _print_array(a, 0)

class odict(DictMixin):

    def __init__(self):
        self._keys = []
        self._data = {}

    def __setitem__(self, key, value):
        if key not in self._data:
            self._keys.append(key)

        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]
        self._keys.remove(key)

    def __iter__(self):
        for key in self._keys:
            yield key

    def keys(self):
        return list(self._keys)

    def copy(self):
        copyDict = odict()
        copyDict._data = self._data.copy()
        copyDict._keys = self._keys[:]
        return copyDict

    def __repr__(self):
        result = []
        for key in self._keys:
            result.append('(%s, %s)' % (repr(key), repr(self._data[key])))
        return ''.join(['OrderedDict', '([', ', '.join(result), '])'])

from datetime import datetime
import time

class HRElapsedTime(object):
    def __init__(self):
        self.start = None
        self.end = None
        self.output_format = '%l:%M %P'
        self.parse_format = '%Y-%m-%d %H:%M:%S'

    def set_parse_format(self, format):
        self.parse_format = format

    def set_output_format(self, format):
        self.output_format = format

    @staticmethod
    def time_from_string(timestr, parse_format = '%Y-%m-%d %H:%M:%S'):
        timep = datetime(*time.strptime(timestr.split('.')[0], parse_format)[0:5])

        return timep

    def set_start_timestr(self, timestr):
        self.start = self.time_from_string(timestr, self.parse_format)

    def set_start_time(self, time):
        self.start = time

    def set_end_timestr(self, timestr):
        self.end = self.time_from_string(timestr, self.parse_format)

    def set_end_time(self, time):
        self.end = time

    def set_end_time_to_now(self):
        self.end = datetime.utcnow()

    def get_hr_elapsed_time(self):

        delta = self.end - self.start
        if delta.days < 1 and self.start.day == self.end.day:
            dstr = 'Today'
            self.longdate = False
        elif delta.days < 2 and (self.end.day - self.start.day) == 1:
            dstr = 'Yesterday'
            self.longdate = False
        elif delta.days < 7:
            dstr = str(delta.days) + ' days ago'
        elif delta.days < 31:
            weeks = int(delta.days/7)
            dstr = str(weeks) + ' week'
            if weeks > 1:
               dstr += 's'
            dstr += ' ago'
        elif delta.days < 365:
            months = int(delta.days/31)
            dstr = str(months) + ' month'
            if months > 1:
                dstr += 's'
            dstr += ' ago'
        else:
            years = int(delta.days/365)
            dstr = str(years) + ' year'
            if years > 1:
                dstr += 's'
            dstr += ' ago'

        return dstr

    def get_hr_time(self, time):
        return datetime.strftime(time, self.output_format)

    def get_hr_start_time(self):
        return self.get_hr_time(self.start)

    def get_hr_end_time(self):
        return self.get_hr_time(self.end)

import collections

if getattr(collections, 'OrderedDict', None):
    OrderedDict = collections.OrderedDict
else:
    import ordereddict
    OrderedDict = ordereddict.OrderedDict


# -*- coding: utf-8 -*-
"""
    pygments.lexers.package
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for package formats.

    :copyright: 2006-2008 by Georg Brandl, Tim Hatch ,
                Stou Sandalski, Paulo Moura, Clara Dimene,
                Andreas Amann ,
                Steve 'Ashcrow' Milner
    :license: BSD, see LICENSE for more details.
"""

import re
from pygments.lexer import Lexer, RegexLexer, include, bygroups, using, this, \
                           do_insertions
from pygments.token import Error, Punctuation, Literal, \
     Text, Comment, Operator, Keyword, Name, String, Number, Generic

line_re  = re.compile('.*?\n')

class RpmSpecLexer(RegexLexer):
    """
    Lexer for RPM specs based of the bash lexer.

    *New in Pygments X.Y.*
    """

    name = 'RPM'
    aliases = ['spec']
    filenames = ['*.spec']

    flags = re.IGNORECASE

    tokens = {
        'root': [
            include('basic'),
            (r'\$\(\(', Keyword, 'math'),
            (r'\$\(', Keyword, 'paren'),
            (r'\${#?', Keyword, 'curly'),
            (r'`', String.Backtick, 'backticks'),
            include('data'),
        ],
        'basic': [
            # TODO: Verify we are using the colors right

            (r'\b(Name:|Version:|Release:|Summary:|Group:|License:|URL:|'
             r'Source[0-9]*:|BuildRoot:|BuildArch:|BuildRequires:|Requires:|'
             r'Provides:)\s*\b', Name.Builtin),
            # things like %install
            (r'(\%[a-zA-Z0-9]{1}[a-zA-Z0-9]*\n)', Keyword.Reserved),
            (r'(\%\{_[a-zA-Z0-9]*\})', Keyword), # FIXME: Kind of works ...
            # things like %attr(...)
            (r'(\%[a-zA-Z0-9]*)(\(.*\))',
             bygroups(Keyword.Declaration, Name.Function)),
            # Macros
            (r'(\%\{!\?[a-zA-Z0-9_]*:)(.*)(\})',
             bygroups(Keyword, String, Keyword)),
            # Variables like %{my_item}
            (r'(\%{[a-zA-Z0-9]{1}[a-zA-Z0-9_\-]*})', Name.Variable),
            # things like %doc
            (r'(\%[a-zA-Z0-9]*)(.*)', bygroups(Keyword.Reserved, String.Doc)),

            # Changelog related
            (r'(\* )([a-zA-Z]{3} [a-zA-Z]{3} [0-9 ]* [0-9]* )(.* )(<)(.*)(> )(.*)(-)(.*)',
             bygroups(Punctuation, Literal.Date, String.Doc, Punctuation,
                      Name.Builtin, Punctuation, Number, Punctuation, Number)),
            # Changelog entry
            (r'(^\-)(.*)',
             bygroups(Punctuation, String.Doc)),

            # ---
            (r'\b(alias|bg|bind|break|builtin|caller|cd|command|compgen|'
             r'complete|declare|dirs|disown|echo|enable|eval|exec|exit|'
             r'export|false|fc|fg|getopts|hash|help|history|jobs|kill|let|'
             r'local|logout|popd|printf|pushd|pwd|read|readonly|set|shift|'
             r'shopt|source|suspend|test|time|times|trap|true|type|typeset|'
             r'if|fi|else|while|do|done|for|then|return|function|case|'
             r'select|continue|until|esac|elif|ulimit|umask|unalias|unset|'
             r'wait|rm|mkdir|sh|find|install|xargs|bash)\s*\b', Name.Builtin),
            (r'#.*\n', Comment),
            (r'\\[\w\W]', String.Escape),
            (r'(\b\w+)(\s*)(=)', bygroups(Name.Variable, Text, Operator)),
            (r'[\[\]{}()=]+', Operator),
            (r'<<\s*(\'?)\\?(\w+)[\w\W]+?\2', String),
            (r'&&|\|\|', Operator),
        ],
        'data': [
            (r'\$?"(\\\\|\\[0-7]+|\\.|[^"])*"', String.Double),
            (r"\$?'(\\\\|\\[0-7]+|\\.|[^'])*'", String.Single),
            (r';', Text),
            (r'\s+', Text),
            (r'[^=\s\n\[\]{}()$"\'`\\<]+', Text),
            (r'\d+(?= |\Z)', Number),
            (r'\$#?(\w+|.)', Name.Variable),
            (r'<', Text),
        ],
        'curly': [
            (r'}', Keyword, '#pop'),
            (r':-', Keyword),
            (r'[a-zA-Z0-9_]+', Name.Variable),
            (r'[^}:"\'`$]+', Punctuation),
            (r':', Punctuation),
            include('root'),
        ],
        'paren': [
            (r'\)', Keyword, '#pop'),
            include('root'),
        ],
        'math': [
            (r'\)\)', Keyword, '#pop'),
            (r'[-+*/%^|&]|\*\*|\|\|', Operator),
            (r'\d+', Number),
            include('root'),
        ],
        'backticks': [
            (r'`', String.Backtick, '#pop'),
            include('root'),
        ],
    }

    def analyse_text(text):
        """
        TODO: Implement me
        """
        return 1.0
