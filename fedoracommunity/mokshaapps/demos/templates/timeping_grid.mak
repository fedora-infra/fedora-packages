    <div class="list header-list">
        Here lies the timeping demo.  Our AMQP server puts out a ping every
        5 seconds with a message containing a timestamp.  This is only a demo
        so we can test our AMQP servers and tweak how they are used.  This API
        is not final and should only be used as a guide to show what is possible.
        A final API for live updates using the Fedora messaging infrastructure
        is forthcomming.
        
        <table id="${id}">
            <thead>
                <tr>
                    <th>Routing Key</th>
                    <th>Message</th>
                </tr>
            </thead>

            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            @{routing_key}
                        </td>
                        <td>
                            @{payload}
                        </td>
                    </tr>
                </tbody>
        </table>
    </div>
    
    <script type="text/javascript">
       $(document).ready(function(){
        document.domain = document.domain;
        Orbited.settings.port = ${orbited_port};
        settings = {};
        settings.amqp_broker_port = 5672;
        settings.amqp_broker_host = 'admin.stg.fedoraproject.org';
        settings.remote_queue = 'org.fedoraproject';
        
        amqp_conn = new amqp.Connection({host:settings.amqp_broker_host,
                                        port:settings.amqp_broker_port,
                                        username: 'guest',
                                        password: 'guest',
                                        
                                       });
    
        amqp_conn.start();
        
        session = amqp_conn.create_session('${id}');
        var remote_queue =  settings.remote_queue + session.name;
        session.Queue('declare', {queue: remote_queue});
        
        var queue = session.create_local_queue({name: 'local_queue'});
        
        var output_cb = function(msg) {
            $('#${id}').mokshagrid('insert_row', 
                                   0, 
                                    {routing_key: msg.header.delivery_properties.routing_key,
                                     payload: msg.body}
                                   
                                  );
        }
     
        queue.subscribe({exchange: 'amq.topic',
                         remote_queue:remote_queue,
                         binding_key: 'org.fedoraproject.timeping',
                         callback: output_cb});
        
        queue.start();

      });
    </script>
