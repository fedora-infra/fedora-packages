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

class odict(dict):
    
    def __init__(self):
        dict.__init__(self)
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
