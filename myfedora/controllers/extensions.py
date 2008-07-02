from myfedora.lib.base import Controller
from tg import expose
import pylons

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
    
    info = {'consumes':['build_message'],
            'author': 'John (J5) Palmieri <johnp@redhat.com>',
            'version': '0.1',
            'name': 'Hello World Message'
           }
    """
    
    def __init__(self, debug=False):
        self.__debug = debug # if debug is False condense javascript to optimize
        self.__extension_cache = {}
        
        #lets put a dummy in for now to test
        self.__extension_cache['build_message'] = """
        [{ 
           info: {consumes:['build_message'],
                 author: 'John (J5) Palmieri <johnp@redhat.com>',
                 version: '0.1',
                 name: 'Hello World Message'
           },
         
           run: function (data) {
            
             msg = this.HelloWorld(data.task_id);
            
             jQuery("#" + data.uid).css('background-color', 'blue');
             return(msg); 
           },
         
           HelloWorld: function (name) {
             return("Hello " + name);
           }
         },
         { 
           info: {consumes:['build_message'],
                 author: 'John (J5) Palmieri <johnp@redhat.com>',
                 version: '0.1',
                 name: 'Goodbye World Message'
           },
         
           run: function (data) {
            
             msg = this.GoodbyeWorld(data.task_id);
            
             jQuery("#" + data.uid).css('background-color', 'red');
             return(msg); 
           },
         
           GoodbyeWorld: function (name) {
             return("Goodbye " + name);
           }
         }
        ]
        """
    
    @expose()
    def default(self, exttype):
        return self.__extension_cache.get(exttype, "");
        