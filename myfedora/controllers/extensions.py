from myfedora.lib.base import Controller
from tg import expose
import pylons
import shlex
import os
import pkg_resources

class Chunk(object):
    def __init__(self):
        self.consumes = []
        self.info = ""
        self.code = ""
        
    def parse_consumes_field(self):
        start = self.info.find('consumes') + 8
        start = self.info.find('[',start)
        end = self.info.find(']', start)
        
        consumes = self.info[start + 1 : end]
    
        self.consumes = shlex.split(consumes)
      

class ExtensionsController(Controller):
    """
    ExtensionsController provide the base controller for serving 
    myfedora javascript extensions.  This works by searching for
    all extensions of a given type and creating a javascript array
    pointing to their run functions.
    
    All extensions should contain at least a run function which will be passed
    the data fields specified by the extension point.  They should also return
    the HTML they wish to be embedded at the extension point. e.g.:
    
    function run(data) {
      // data will always contain a uid field and the HTML you return
      // will be wrapped in a div with that id
      return "<div>Hello</div>";
    };
    
    Extensions also need a header which describes the extension as such:
    
    info : {'consumes':['build_message'],
            'author': 'John (J5) Palmieri <johnp@redhat.com>',
            'version': '0.1',
            'name': 'Hello World Message'
           }
    """
    
    def __init__(self, debug=False):
        self.__debug = debug # if debug is False condense javascript to optimize
        self.__extension_cache = {}
        
        # FIXME: use pkg_resources to find the extensions directories 
        self.load_extensions('myfedora', 'plugins/extensions')
    
    def chunk_code(self, js, filename):
        start = js.find('{')
        end = 0
        chunks = []
        length = len(js)
        
        while (start != -1):
            count = 1
            i = start + 1
            pull_info = False
            pull_info_start = 0
            pull_info_end = 0
            
            while(count != 0 and i < length):
                if js[i] == '{':
                    count += 1
                elif js[i] == '}':
                    count -= 1
                elif count==1 and js[i]=='i' and js.find('info',i) == i:
                    if pull_info_start != 0:
                        print "ERROR: Unexpected Info Field : extension file %s has more than on info field per extension (ignoring file)" % filename
                        return None
                    
                    # put us on info duty
                    pull_info = True
                    
                if pull_info:
                    if pull_info_start == 0:
                        if count > 1:
                            pull_info_start = i
                    else:
                        if count == 1:
                            pull_info_end = i
                            pull_info = False
                    
                i += 1
            
            end = i
            
            c = Chunk()
            c.code = js[start:end]
            c.info = js[pull_info_start:pull_info_end + 1]
            
            c.parse_consumes_field()
            chunks.append(c)
            
            if i >= length:
                print "ERROR: Unexpected EOF: extension file %s has mismatched braces (ignoring file)" % filename
                return None
                
            start = js.find('{', end)
        
        return chunks
    
    def load_extension(self, file):
        print "Loading JavaScript extension %s" % file
        f = open(file,'r')
        js = f.read()
        
        chunks = self.chunk_code(js, file)
        if not chunks:
            if chunks != None:
                print "ERROR: No Content : extension file %s doesn't have any valid extensions (ignoring file)" % filename
                
            return
        
        for c in chunks:
            for exttype in c.consumes:
                code = self.__extension_cache.get(exttype, [])
                #TODO: run through optimizer which strips whitespace
                code.append(c.code)
                self.__extension_cache[exttype] = code
        
    def load_extensions(self, module, dir):
        real_dir = pkg_resources.resource_filename(module, dir)
        for root, dirs, files in os.walk(real_dir):
            for name in files:
                if name.endswith('js'):
                    path = os.path.join(root, name)
                    self.load_extension(path)
                    
        # compile lists in the cache down to a string so we don't have to 
        # process it on each request
        for key, value in self.__extension_cache.iteritems():
            s = '[' + ','.join(value) + ']'
            self.__extension_cache[key] = s
                
    @expose()
    def default(self, exttype=None, _=None):
        # _ is a jsonp thing
        
        if not exttype:
            return ''
        
        extensions_data = self.__extension_cache.get(exttype, "")
        extensions_str = ','.join(extensions_data)
        
        script = 'var mf_loaded_extensions ='
        script += extensions_data
        script += ';'
        # now run the deferred extensions queued up while the scripts
        # were being downloaded
        
        script += 'myfedora.extensions._extension_cache["' + exttype +'"] = mf_loaded_extensions;'
        script += 'var deferred=myfedora.extensions._extension_deferred["' + exttype +'"];'
        script += 'var d=deferred.shift();'
        script += 'while(d){' 
        script +=   'myfedora.extensions.run_extensions(mf_loaded_extensions, d);'
        script +=   'd = deferred.shift();'
        script += '}'
        
        return script
        
