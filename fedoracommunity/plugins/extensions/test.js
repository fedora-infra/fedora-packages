        {{  
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
         }
         
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
