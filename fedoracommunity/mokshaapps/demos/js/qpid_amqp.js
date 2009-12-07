(function(){
var _module = null;

amqp.protocol.extend(amqp, {
    Connection: function(options) {
        version = options.version;

        this._conn = amqp.protocol.get_connection(version, options);
    },
    
    Session: function(options) {
        this.name = options['name'];
        this._sess = options['_conn'].create_session(this.name);
        this._conn = options['_conn'];
        this._last_channel = -1;
        var s = this._sess;
        this.Message = function() {this._sess.Message.apply(s, arguments)};
        
        this.Queue = function() {this._sess.Queue.apply(s, arguments)}
        this.Exchange = function() {this._sess.Exchange.apply(s, arguments)};
    },
    
    Queue: amqp.protocol.MetaClass({
        _defaults: {
            name: 'local_class',
            channel: -1,
            flow_mode: 0,
            flow_credits: 0xFFFFFFFF,
            _session: null
        },
        _init: function(options) {
            this.name = options['name'];
            this._session = options['_session'];
            this._flow_mode = options['flow_mode'];
            this._flow_credits = options['flow_credits'];
            
            var c = options['channel'];
            if (c < 0)
                c  = this._session.get_next_channel();
            this._channel = c;
            
            this._bound_remote_queues = {};
            this._dispatch_table = [];
            this._partial_transfer = {};
            
        }
    })
});


_module = amqp;

/* public methods */

amqp.protocol.extend(amqp.Connection.prototype, {
    create_session: function(name) {
        var options = null;
        if (typeof(name) == 'string') {
            options = {};
            options['name'] = name;
        } else {
            options = name;
        }
        
        options['_conn'] = this._conn;
        
        return new _module.Session(options); 
    },
    
    start: function() {
        this._conn.start();
    }
});

amqp.protocol.extend(amqp.Session.prototype,{
    create_local_queue: function(options) {
        options['_session'] = this;
        return new _module.Queue(options);
    },
    
    get_next_channel: function() {
        this._last_channel++;
        return this._last_channel;
    },
    
});

amqp.protocol.extend(amqp.Queue.prototype, {
    set_flow_mode: function(mode) {
        this._flow_mode = mode;
        this._session.Message('set_flow_mode', 
                              {destination: this.name,
                               flow_mode: mode});
    },
    
    add_flow_credits: function(credits) {
        if (typeof(credits) == 'undefined')
            credits = this._flow_credits;
        else
            this._flow_credits = credits;
            
        this._session.Message('flow', {destination: this.name,
                                       unit: 0,
                                       value: credits});
        this._session.Message('flow', {destination: this.name,
                                       unit: 1,
                                       value: credits});
    },
    
    subscribe: function(options) {
        this._session.Exchange('bind', {exchange: options.exchange,
                                        queue: options.remote_queue,
                                        binding_key: options.binding_key});

        if (!this._bound_remote_queues[options.remote_queue]) {
            this._session.Message('subscribe', {queue: options.remote_queue,
                                                destination: this.name,
                                                accept_mode: 1,
                                                acquire_mode: 0});
                                                
            this._bound_remote_queues[options.remote_queue] = true;
        }
        
        this._dispatch_table.push(options);
    },
    
    _dispatch: function(transfer) {
        var header = transfer['header'];
        var dp = header['delivery_properties'];
        var exchange = dp['exchange'];
        var routing_key = dp['routing_key'];
        
        for (var i in this._dispatch_table) {
            var opts = this._dispatch_table[i];
            if (opts['exchange'] != exchange)
                continue;
           
            var routing_key_split = routing_key.split('.');
            var binding_key_split = opts.binding_key.split('.');
            if (binding_key_split.length > routing_key_split.length)
                continue;
            
            var is_match = false;
            for(var j in binding_key_split) {
                is_match = true;
                var bkey = binding_key_split[j];
                if (bkey == '#')
                    continue; 
                    
                if (bkey != routing_key_split[j]) {
                    is_match = false;
                    break;
                }
            }
            
            if (is_match)
                opts['callback'](transfer);
        } 
    },
    
    start: function() {
        this.set_flow_mode(this._flow_mode);
        this.add_flow_credits(this._flow_credits);
        
        var _me = this;
        
        var handle_header = function(frame) {
            var header = frame.get('header');
            var is_last_segment = frame.get('is_last_segment');
            var channel = frame.get('channel');
            
            var transfer = _me._partial_transfer[channel];
            if (typeof(transfer) == 'undefined' || transfer == null)
                return false;
                
            for (var h in header)
                transfer['header'][h] = header[h]
            
            if (is_last_segment) {
                _me._partial_transfer[channel] = null;
                _me._dispatch(transfer);
            }
            
            return true;
        }
            
        var handle_body = function(frame) {
            var body = frame.get('body');
            var is_last_segment = frame.get('is_last_segment');
            var channel = frame.get('channel');
            
            var transfer = _me._partial_transfer[channel];
            if (typeof(transfer) == 'undefined' || transfer == null)
                return false;
                
            transfer['body'] += body;
            
            if (is_last_segment) {
                _me._partial_transfer[channel] = null;
                _me._dispatch(transfer);
            }
            
            return true;
        }
        
        var handle_transfer = function(frame) {    
            var msg = frame.get('msg');
            var is_last_segment = frame.get('is_last_segment');
            var channel = frame.get('channel');
            var dest = msg.get('destination');
            if (dest != _me.name)
                return false;

            if (is_last_segment)
                _me._dispatch({'header':{},
                                'body': ''
                                }); //empty message
            else
                _me._partial_transfer[channel] = {'header':{},
                                                   'body': ''}
            return true;
        };
        
        this._session._conn.command_subscribe('message',
                                              'transfer',
                                              null,
                                              handle_transfer,
                                              false);
                                              
        this._session._conn.header_subscribe('message',
                                             null,
                                             handle_header,
                                             false);
                                             
        this._session._conn.body_subscribe(null,
                                           handle_body,
                                           false);
 
    }
});
})();