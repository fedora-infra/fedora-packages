// This file is part of Fedora Community.
// Copyright (C) 2008-2009  Red Hat, Inc.
// 
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
// 
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
