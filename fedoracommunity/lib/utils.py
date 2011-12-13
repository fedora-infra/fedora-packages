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
from tg import url
from pylons import request
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
    ## {{{ http://code.activestate.com/recipes/576693/ (r9)
    # Backport of OrderedDict() class that runs on Python 2.4, 2.5, 2.6, 2.7 and pypy.
    # Passes Python2.7's test suite and incorporates all the latest updates.

    try:
        from thread import get_ident as _get_ident
    except ImportError:
        from dummy_thread import get_ident as _get_ident

    try:
        from _abcoll import KeysView, ValuesView, ItemsView
    except ImportError:
        pass


    class OrderedDict(dict):
        'Dictionary that remembers insertion order'
        # An inherited dict maps keys to values.
        # The inherited dict provides __getitem__, __len__, __contains__, and get.
        # The remaining methods are order-aware.
        # Big-O running times for all methods are the same as for regular dictionaries.

        # The internal self.__map dictionary maps keys to links in a doubly linked list.
        # The circular doubly linked list starts and ends with a sentinel element.
        # The sentinel element never gets deleted (this simplifies the algorithm).
        # Each link is stored as a list of length three:  [PREV, NEXT, KEY].

        def __init__(self, *args, **kwds):
            '''Initialize an ordered dictionary.  Signature is the same as for
            regular dictionaries, but keyword arguments are not recommended
            because their insertion order is arbitrary.

            '''
            if len(args) > 1:
                raise TypeError('expected at most 1 arguments, got %d' % len(args))
            try:
                self.__root
            except AttributeError:
                self.__root = root = []                     # sentinel node
                root[:] = [root, root, None]
                self.__map = {}
            self.__update(*args, **kwds)

        def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
            'od.__setitem__(i, y) <==> od[i]=y'
            # Setting a new item creates a new link which goes at the end of the linked
            # list, and the inherited dictionary is updated with the new key/value pair.
            if key not in self:
                root = self.__root
                last = root[0]
                last[1] = root[0] = self.__map[key] = [last, root, key]
            dict_setitem(self, key, value)

        def __delitem__(self, key, dict_delitem=dict.__delitem__):
            'od.__delitem__(y) <==> del od[y]'
            # Deleting an existing item uses self.__map to find the link which is
            # then removed by updating the links in the predecessor and successor nodes.
            dict_delitem(self, key)
            link_prev, link_next, key = self.__map.pop(key)
            link_prev[1] = link_next
            link_next[0] = link_prev

        def __iter__(self):
            'od.__iter__() <==> iter(od)'
            root = self.__root
            curr = root[1]
            while curr is not root:
                yield curr[2]
                curr = curr[1]

        def __reversed__(self):
            'od.__reversed__() <==> reversed(od)'
            root = self.__root
            curr = root[0]
            while curr is not root:
                yield curr[2]
                curr = curr[0]

        def clear(self):
            'od.clear() -> None.  Remove all items from od.'
            try:
                for node in self.__map.itervalues():
                    del node[:]
                root = self.__root
                root[:] = [root, root, None]
                self.__map.clear()
            except AttributeError:
                pass
            dict.clear(self)

        def popitem(self, last=True):
            '''od.popitem() -> (k, v), return and remove a (key, value) pair.
            Pairs are returned in LIFO order if last is true or FIFO order if false.

            '''
            if not self:
                raise KeyError('dictionary is empty')
            root = self.__root
            if last:
                link = root[0]
                link_prev = link[0]
                link_prev[1] = root
                root[0] = link_prev
            else:
                link = root[1]
                link_next = link[1]
                root[1] = link_next
                link_next[0] = root
            key = link[2]
            del self.__map[key]
            value = dict.pop(self, key)
            return key, value

        # -- the following methods do not depend on the internal structure --

        def keys(self):
            'od.keys() -> list of keys in od'
            return list(self)

        def values(self):
            'od.values() -> list of values in od'
            return [self[key] for key in self]

        def items(self):
            'od.items() -> list of (key, value) pairs in od'
            return [(key, self[key]) for key in self]

        def iterkeys(self):
            'od.iterkeys() -> an iterator over the keys in od'
            return iter(self)

        def itervalues(self):
            'od.itervalues -> an iterator over the values in od'
            for k in self:
                yield self[k]

        def iteritems(self):
            'od.iteritems -> an iterator over the (key, value) items in od'
            for k in self:
                yield (k, self[k])

        def update(*args, **kwds):
            '''od.update(E, **F) -> None.  Update od from dict/iterable E and F.

            If E is a dict instance, does:           for k in E: od[k] = E[k]
            If E has a .keys() method, does:         for k in E.keys(): od[k] = E[k]
            Or if E is an iterable of items, does:   for k, v in E: od[k] = v
            In either case, this is followed by:     for k, v in F.items(): od[k] = v

            '''
            if len(args) > 2:
                raise TypeError('update() takes at most 2 positional '
                                'arguments (%d given)' % (len(args),))
            elif not args:
                raise TypeError('update() takes at least 1 argument (0 given)')
            self = args[0]
            # Make progressively weaker assumptions about "other"
            other = ()
            if len(args) == 2:
                other = args[1]
            if isinstance(other, dict):
                for key in other:
                    self[key] = other[key]
            elif hasattr(other, 'keys'):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
            for key, value in kwds.items():
                self[key] = value

        __update = update  # let subclasses override update without breaking __init__

        __marker = object()

        def pop(self, key, default=__marker):
            '''od.pop(k[,d]) -> v, remove specified key and return the corresponding value.
            If key is not found, d is returned if given, otherwise KeyError is raised.

            '''
            if key in self:
                result = self[key]
                del self[key]
                return result
            if default is self.__marker:
                raise KeyError(key)
            return default

        def setdefault(self, key, default=None):
            'od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od'
            if key in self:
                return self[key]
            self[key] = default
            return default

        def __repr__(self, _repr_running={}):
            'od.__repr__() <==> repr(od)'
            call_key = id(self), _get_ident()
            if call_key in _repr_running:
                return '...'
            _repr_running[call_key] = 1
            try:
                if not self:
                    return '%s()' % (self.__class__.__name__,)
                return '%s(%r)' % (self.__class__.__name__, self.items())
            finally:
                del _repr_running[call_key]

        def __reduce__(self):
            'Return state information for pickling'
            items = [[k, self[k]] for k in self]
            inst_dict = vars(self).copy()
            for k in vars(OrderedDict()):
                inst_dict.pop(k, None)
            if inst_dict:
                return (self.__class__, (items,), inst_dict)
            return self.__class__, (items,)

        def copy(self):
            'od.copy() -> a shallow copy of od'
            return self.__class__(self)

        @classmethod
        def fromkeys(cls, iterable, value=None):
            '''OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
            and values equal to v (which defaults to None).

            '''
            d = cls()
            for key in iterable:
                d[key] = value
            return d

        def __eq__(self, other):
            '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
            while comparison to a regular mapping is order-insensitive.

            '''
            if isinstance(other, OrderedDict):
                return len(self)==len(other) and self.items() == other.items()
            return dict.__eq__(self, other)

        def __ne__(self, other):
            return not self == other

        # -- the following methods are only used in Python 2.7 --

        def viewkeys(self):
            "od.viewkeys() -> a set-like object providing a view on od's keys"
            return KeysView(self)

        def viewvalues(self):
            "od.viewvalues() -> an object providing a view on od's values"
            return ValuesView(self)

        def viewitems(self):
            "od.viewitems() -> a set-like object providing a view on od's items"
            return ItemsView(self)
    ## end of http://code.activestate.com/recipes/576693/ }}}
