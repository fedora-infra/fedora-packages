from UserDict import DictMixin

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

class HRElapsedTime():
    def __init__(self):
        self.start = None
        self.end = None
        self.longdate = True

    @staticmethod        
    def time_from_string(timestr):
        parse_format = '%Y-%m-%d %H:%M:%S'
        
        timep = datetime.strptime(timestr.split('.')[0], parse_format)
        
            
        return timep
    
    def set_start_timestr(self, timestr):
        self.start = self.time_from_string(timestr)
        
    def set_start_time(self, time):
        self.start = time
        
    def set_end_timestr(self, timestr):
        self.end = self.time_from_string(timestr)
        
    def set_end_time(self, time):
        self.end = time
        
    def set_end_time_to_now(self):
        self.end = datetime.now()
        
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
            dstr = 'over ' + str(weeks) + ' week'
            if weeks > 1:
               dstr += 's'
            dstr += ' ago'
        elif delta.days < 365:
            months = int(delta.days/31)
            dstr = 'over ' + str(months) + ' month'
            if months > 1:
                dstr += 's'
            dstr += ' ago'
        else:
            years = int(delta.days/365)
            dstr = 'over ' + str(years) + ' year'
            if years > 1:
                dstr += 's'
            dstr += ' ago'
        
        
        return dstr
            
    def get_hr_time(self, time):
        if self.longdate:
            return datetime.strftime(time, "%e %b %Y")
        else:
            return datetime.strftime(time, "%l:%M %P")
        
    def get_hr_start_time(self):
        return self.get_hr_time(self.start)
        
    def get_hr_end_time(self):
        return self.get_hr_time(self.end)