/*

console = new amqp.qmf.Console({brokerConnected: function(broker){},
                                brokerDisconnected: function(broker){}, 
                                newPackage: function(name){},
                                newClass: function(kind, classKey){},
                                newAgent: function(agent){},
                                delAgent: function(agent){},
                                objectProps: function(broker, object){},
                                objectStats: function(broker, object){},
                                event: function(broker, event){},
                                heartbeat: function(agent, timestamp){},
                                brokerInfo: function(broker){},
                                methodResponse: function(broker, seq, response){},
                                manageConnections: true,
                                rcvObjects: false,
                                rcvHeartbeats: false});
session = amqp.qmf.Session(console);
broker = session.add_broker('http://localhost:9000');
queues = sess.getObjects(_class="queue", _package="org.apache.qpid.broker");


*/

(function(){
var _module = null;


})();