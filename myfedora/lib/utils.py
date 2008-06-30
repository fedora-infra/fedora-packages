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
