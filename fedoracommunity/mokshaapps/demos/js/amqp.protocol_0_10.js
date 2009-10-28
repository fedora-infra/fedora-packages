
/*********************************************************
 * Generated AMQP lowlevel protocol bindings
 *
 * We put this under the namespace
 * amqp.protocol_<vermajor>_<version_minor> to
 * seperate out the generated bindings from the high level
 * bindings.
 *
 * Also note we use a notation that is easier for generated
 * output but not as readable as hand written code.  Every
 * section outputs a complete javascript block.
 *********************************************************/

(function(){
var None = null;
var _module = null;

amqp.protocol_0_10= {
    version: {major: 0,
              minor: 10,
              toString: function(){return "0.10"},
             },
    default_port: 5672,
    type:{},
    typecode:{},
    cls:{},
    clscode:{},
    get_type: function(typecode) {
        return this.typecode[typecode];
    },
    get_header: function() {
        var protocol_header = 'AMQP';
        var major = this.version.major;
        var minor = this.version.minor;
        protocol_header += String.fromCharCode(1, 1, major, minor);
        return protocol_header;
    },
    guess_type: function(value) {
        if (typeof(value) == 'number') {
            var sn = value.toString(10);
            var absv = Math.abs(value);
            if (vn.indexOf('.') == -1) {
                if (absv < (1 << 7))
                    return new this.type.int8(value);
                else if (absv < (1 << 15))
                    return new this.type.int16(value);
                else if (absv < (1 << 31))
                    return new this.type.int32(value);
                else if (absv < (1 << 63))
                    return new this.type.int64(value);
            } else {
                // send as a double
                return new this.type.double(value);
            }
        } else if (typeof(value) == 'string') {
            var l = value.length;
            if (l < (1 << 8))
                return new this.type.str8(value);
            else if (l < (1 << 16))
                return new this.type.str16(value);
        } else if (typeof(value) == 'object' && value.encode) {
            return value;
        } else {
            throw "Can not guess the value of '" + value + "' not yet handled in guess_type";
        }
    },
    Connection: amqp.protocol.MetaClass({
        _defaults: {
            host: 'localhost',
            port: 9000,
            username: '',
            password: '',
            send_hook: function() {},
            recive_hook: function() {},
            _module: null
        },

        statecode: {
            CLOSED: 0,
            CONNECTING: 1,
            HANDSHAKE_STAGE_1: 2,
            CONNECTED: 3,
            NEGOTIATED: 4
        },

        _init: function(options) {
            this._options = options;
            this._module = options._module;
            this._prenegotiation_msg_queue = [];

            options._module = null;

            var TCPSocket = Orbited.TCPSocket;
            this._orbited_conn = new TCPSocket();
            this.state = this.statecode.CLOSED;
            this._dispatch_table = {};

            var _me = this;

            this._orbited_conn.onopen = function() {
                console.log('connection opened!');

                // Handshake
                _me.state = _me.statecode.HANDSHAKE_STAGE_1;
                protocol_header = _me.get_header();

                _me._raw_send(protocol_header);
            };

            var process_data = function(data) {
                var sc = _me.statecode;
                var assembly = null;

                if (data instanceof amqp.protocol.Assembly)
                    assembly = data;
                else
                    assembly = new amqp.protocol.Assembly({data: data});

                assembly.mark_start(); // debug metadata

                switch(_me.state) {
                    case sc.HANDSHAKE_STAGE_1:
                        _me.state = sc.CONNECTED;
                        var frame = new _me._module.Frame({assembly: assembly,
                                                           contains_header: true});
                        frame.decode();

                        if (_me._options.recive_hook)
                            _me._options.recive_hook(data, frame);

                        var track = frame.get('track');
                        var type = frame.get('segment_type');

                        if (track != 0)
                            throw "Expecting a control frame but recived a command during stage 1 of the handshake";
                        if (type != 0)
                            throw "Recived the wrong control code during stage 1 of the handshake";

                        var start_control = frame.get('msg');
                        var srv_properties = start_control.get('server_properties');
                        var mechanisms = start_control.get('mechanisms');
                        var locals = start_control.get('locals');

                        // send start-ok response
                        // FIXME: Support other auth mechanisms
                        var start_ok_msg = new amqp.protocol.Message({
                            template: _me._module.cls.connection.prototype.msg.start_ok,
                            parsed_data: {
                                client_properties: {
                                    product: 'qpid kamaloka javascript client',
                                    platform: navigator.userAgent,
                                },
                                mechanism: 'ANONYMOUS',
                                locale: 'en_US',
                                response: ''
                            }

                        });

                        _me.control_subscribe('connection',
                                              'tune',
                                              0,
                                              _me.handle_tune_cmd);

                        _me.send(start_ok_msg, true);

                        break;

                    case sc.CONNECTED:
                    case sc.NEGOTIATED:
                        // dispatch from here
                        var frame = new _me._module.Frame({assembly: assembly,
                                                          contains_header: false});
                        frame.decode();

                        if (_me._options.recive_hook)
                            _me._options.recive_hook(data, frame);
                        
                        var track = frame.get('track');
                        var type = frame.get('segment_type');
                        var cls = frame.get('class_code');
                        var control = frame.get('control_code');
                        var channel = frame.get('channel');
                        var id = 0;
                                                
                        if (type == 0 || type == 1) {
                            id = type + '.' + cls + '.' + control;                           
                        } else if (type == 2) {
                            id = type + '.' + cls + '.0';    
                        } else if (type == 3) {
                            id = type + '.0.0';    
                        } else {
                            console.log('Frame type ' + type + ' unknown!!!');
                            return;
                        }
                        
                        var callbacks = _me._dispatch_table[id];
                        if (callbacks) {
                            var discard_pile = [];
                            for (var i=0; i<callbacks.length; i++) {
                                var cb = callbacks[i][0];
                                var discard = callbacks[i][1];
                                var ch = callbacks[i][2];
                                if (typeof(ch) != undefined && ch != null)
                                    if (ch != channel) // we are looking for a specific channel
                                        continue; 
                                        
                                if (discard)
                                    discard_pile.push(i);
                                    
                                if (cb) {
                                    var handled = cb.call(_me, frame);
                                    if (handled)
                                        break;
                                }
                            }

                            for (var i=discard_pile.length-1; i>=0; i--)
                                callbacks.splice(discard_pile[i], 1);
                        }

                        break;

                    default:
                        throw "State code 0x" + _me.state.toString(16) + " is not implemented by amqp.Connecton";

                }

                // check for more frames
                if (!assembly.eof())
                    process_data(assembly);

            };

            this._orbited_conn.onread = process_data;

            this._orbited_conn.onclose = function(code) {
                console.log('Connection Closed [' + code + ']');
            };
        },

        message_subscribe: function (cls_code, msg_code, msg_type, channel, callback, discard) {
            var id = msg_type + '.' + cls_code + '.' + msg_code;
            var callback_list = this._dispatch_table[id];

            if (!callback_list)
                callback_list = []

            callback_list.push([callback, discard, channel]);

            this._dispatch_table[id] = callback_list;
        },
        control_subscribe: function (cls_name, msg_name, channel, callback, discard) {
            var cls = this._module.cls[cls_name];
            var cls_code = cls.prototype.code;
            var msg = cls.prototype.msg[msg_name];
            var msg_code = msg.code;
            
            this.message_subscribe(cls_code, msg_code, 0,  channel, callback, discard);
        },
        command_subscribe: function (cls_name, msg_name, channel, callback, discard) {
            var cls = this._module.cls[cls_name];
            var cls_code = cls.prototype.code;
            var msg = cls.prototype.msg[msg_name];
            var msg_code = msg.code;
            
            this.message_subscribe(cls_code, msg_code, 1, channel, callback, discard);
        },
        header_subscribe: function (cls_name, channel, callback, discard) {
            var cls = this._module.cls[cls_name];
            var cls_code = cls.prototype.code;
      
            this.message_subscribe(cls_code, 0, 2,  channel, callback, discard);
        },
        body_subscribe: function (channel, callback, discard) {
            this.message_subscribe(0, 0, 3,  channel, callback, discard);
        },
        
        get_state: function() {
            return this.state;
        },

        get_type: function (typecode) {
            return this._module.get_type(typecode);
        },

        get_header: function () {
            return this._module.get_header();
        },

        guess_type: function (value) {
            return this._module.guess_type(value);
        },

        _raw_send: function (msg) {
            this._orbited_conn.send(msg);
        },

        send: function (message, is_negotiating) {
            // queue messages if we are still negotiating
            if (!is_negotiating && !(this.state == this.statecode.NEGOTIATED)) {
                this._prenegotiation_msg_queue.push(message);
                return;
            }

            message.encode();

            // FIXME: break up if size is too big
            var size = message.get_size();
            var payload = message.get_data(size);
            var msg_type = message.get_type();
            var cls_code = message.code;
            var segment_type = msg_type;
            var channel = 0;
            var track = msg_type;


            // FIXME: get module version from the header info
            //        and work with segments and multiple frames
            var frame = new this._module.Frame({
                parsed_data: {
                    frame_format_version: 0,
                    is_first_segment: true,
                    is_last_segment: true,
                    is_first_frame: true,
                    is_last_frame: true,
                    segment_type: segment_type, // control
                    track: track,
                    channel: channel,
                    control_code: msg_type,
                    class_code: cls_code,
                    msg: message
                },
                payload: payload
            });

            frame.encode();
            var data = frame.get_data();
            this._raw_send(data);
            if (this._options.send_hook)
                this._options.send_hook(data, frame);
        },

        start: function() {
            this.state = this.statecode.CONNECTING;
            this._orbited_conn.open(this._options.host, this._options.port, isBinary=true);
        },

        handle_tune_cmd: function (frame) {
            var msg = frame.get('msg');
            var channel_max = msg.get('channel_max');
            var max_frame_size = msg.get('max_frame_size');
            var heartbeat_min = msg.get('heartbeat_min');
            var heartbeat_max = msg.get('heartbeat_max');

            var tune_ok_msg = new amqp.protocol.Message({
                template: this._module.cls.connection.prototype.msg.tune_ok,
                parsed_data: {
                    channel_max: 2,
                }
            });

            this.send(tune_ok_msg, true);

            this.control_subscribe('connection', 'open_ok', 0, this.handle_open_ok_cmd, true);
            var open_msg = this.construct_message('connection', 'open', {virtual_host:''});
            this.send(open_msg, true);
        },

        handle_open_ok_cmd: function (frame) {
            var msg = frame.get('msg');
            this.state = this.statecode.NEGOTIATED;
            for (var i = 0; i < this._prenegotiation_msg_queue.length; i++)
                this.send(this._prenegotiation_msg_queue[i]);
        },

        create_session: function(uuid) {
            var sess = new _module.Session({uuid: uuid,
                                            connection: this});

            return sess;
        },

        construct_message: function(cls_name, message_name, params) {
            var msg = new amqp.protocol.Message({
                template: _module.cls[cls_name].prototype.msg[message_name],
                parsed_data: params
            });

            return msg;
        }
    }),
    Frame: amqp.protocol.MetaClass({
        _defaults: {
            assembly: null,
            parsed_data: {},
            contains_header: false,
            payload: ''
        },

        _init: function(options) {
            this._options = options;
            if (!this._options.assembly)
                this._options.assembly = new amqp.protocol.Assembly()
            this._module = amqp.protocol_0_10;
        },

        decode: function() {
            var o = this._options;
            var assembly = o.assembly;

            // Parse the header
            if (this._options.contains_header)
                this.set('header', amqp.protocol.decode_header(assembly));

            // now the Frame
            this.set('frame_format_version', assembly.read_bit(2));
            assembly.read_bit(2);
            this.set('is_first_segment', assembly.read_bit(1));
            this.set('is_last_segment', assembly.read_bit(1));
            this.set('is_first_frame', assembly.read_bit(1));
            this.set('is_last_frame', assembly.read_bit(1));
            this.set('segment_type', new this._module.type.uint8().decode(assembly));
            this.set('frame_size', new this._module.type.uint16().decode(assembly));
            assembly.read_byte(1);
            assembly.read_bit(4);
            this.set('track', assembly.read_bit(4));
            this.set('channel', new this._module.type.uint16().decode(assembly));
            assembly.read_byte(4);
            var payload_size = this.get('frame_size') - 12; // frame size - header size

            var st = o.parsed_data['segment_type'];
            if (st == 0 || st == 1)   // control/command #TODO: check against the segment-type domain enum
                this.decode_cls();
            else if(st == 2)          // header
                this.decode_header(payload_size);
            else if(st == 3)         // body
                this.decode_body(payload_size);
            else
                throw "Invalid segment type encountered"
        },

        decode_cls: function() {
            var a = this._options.assembly;
            var cls_code = this.set('class_code', new this._module.type.uint8().decode(a));
            var control_code = this.set('control_code', new this._module.type.uint8().decode(a));

            var cls = this._module.clscode[cls_code];
            // FIXME: error handling

            var msg = new cls({assembly: a});
            this.set('msg', msg);

            var results = msg.decode(control_code);
            for (var k in results)
                this.set(k, results[k]);
        },

        decode_header: function(payload_size) {
            var a = this._options.assembly;
            var header = {};

            do {
                var struct_size = new this._module.type.uint32().decode(a);
                var cls_code = this.set('class_code', new this._module.type.uint8().decode(a));
                var header_code = this.set('control_code', new this._module.type.uint8().decode(a));

                var cls = this._module.clscode[cls_code];
                // FIXME: error handling

                var st = new cls.prototype.structcode[header_code]();
                var values = st.decode(a);
                var key = st.name;
                header[key] = values;
                payload_size = payload_size - (struct_size + 4);
            } while (payload_size > 0);
            
            this.set('header', header);
        },

        decode_body: function(size) {
            var a = this._options.assembly;
            var data = a.read_byte(size);
            this.set('body', data);
        },

        encode: function() {
            var o = this._options;
            var assembly = o.assembly;

            // Add the header
            if(o.contains_header)
                assembly.write(this._module.get_header());

            // now the Frame
            var ffv = this.get('frame_format_version');
            var next_byte = ffv << 6;

            //next two bits are reserved while we add the rest of the bits
            if(this.get('is_first_segment'))
                next_byte += 1 << 3;
            if(this.get('is_last_segment'))
                next_byte += 1 << 2;
            if(this.get('is_first_frame'))
                next_byte += 1 << 1;
            if(this.get('is_last_frame'))
                next_byte += 1;

            assembly.write(String.fromCharCode(next_byte));
            var st = amqp.protocol.int_to_bytestr(this.get('segment_type'), 1);
            assembly.write(st);

            // set the frame size which is the size of the header +
            // size field (2) + padding byte (1) + track field (1) +
            // channel field (2) + padding bytes(4) + size of payload
            var frame_size = assembly.get_size(false) + 10 + o.payload.length;
            var fs = amqp.protocol.int_to_bytestr(frame_size, 2);
            assembly.write(fs);
            assembly.write(String.fromCharCode(0));
            var t = amqp.protocol.int_to_bytestr(this.get('track'), 1);
            assembly.write(t);
            var ch = amqp.protocol.int_to_bytestr(this.get('channel'), 2);
            assembly.write(ch);
            assembly.write(String.fromCharCode(0,0,0,0));
            assembly.write(o.payload);
        },

        get: function(key) {
            return this._options.parsed_data[key];
        },

        set: function(key, value) {
            this._options.parsed_data[key] = value;
            return value;
        },

        get_assembly: function() {
            return this._options.assembly;
        },

        get_data: function() {
            return this._options.assembly.get_data();
        }
    }),

    Session: amqp.protocol.MetaClass({
        _defaults: {
            uuid: null,
            connection: null
        },
        _init: function(options) {
            this.name = options.uuid;
            this._conn = options.connection;
            this._defered = [];
            this._ready = false;

            var _me = this;

            // setup the session handshake sequence
            // FIXME: Handle already existing connections
            this._conn.control_subscribe('session',
                                         'attached',
                                         0,
                                         function(frame) {
                                             var msg = frame.get('msg');
                                             var flush = _me._conn.construct_message('session',
                                                                                      'flush',
                                                                                      {expected: false,
                                                                                       confirmed: false,
                                                                                       completed: true});

                                             _me._conn.send(flush);
                                         },
                                         true
                                        );

            this._conn.control_subscribe('session',
                                         'completed',
                                         0,
                                         function(frame) {
                                             var msg = frame.get('msg');
                                             var known_completed = _me._conn.construct_message('session',
                                                                                      'known_completed',
                                                                                      {});

                                             _me._conn.send(known_completed);
                                             var request_timeout = _me._conn.construct_message('session',
                                                                                      'request_timeout',
                                                                                      {timeout: 400});

                                             _me._conn.send(request_timeout);
                                         },
                                         true
                                        );

            this._conn.control_subscribe('session',
                                         'timeout',
                                         0,
                                         function(frame) {
                                             var msg = frame.get('msg');
                                             var command_point = _me._conn.construct_message('session',
                                                                                      'command_point',
                                                                                      {command_id: 0,
                                                                                       command_offset:0});

                                             _me._conn.send(command_point);

                                             for(var i=0; i<_me._defered.length; i++)
                                                 _me._conn.send(_me._defered[i]);
                                         },
                                         true
                                        );

            var attach = this._conn.construct_message('session',
                                                     'attach',
                                                     {name: this.name});
            this._conn.send(attach);

        },

        send: function(msg) {
            if (this._ready)
                this._conn.send(msg);
            else
                this._defered.push(msg);
        },

        Queue: function(command_name, params) {
            var queue_msg = this._conn.construct_message('queue',
                                                         command_name,
                                                         params);
            this.send(queue_msg);
        },
        create_queue: function() {

        },
        Exchange: function(command_name, params) {
            var ex_msg = this._conn.construct_message('exchange',
                                                  command_name,
                                                  params);
            this.send(ex_msg);
        },
        Message: function(command_name, params) {
            var message_msg = this._conn.construct_message('message',
                                                           command_name,
                                                         params);
            this.send(message_msg);
        },

    })
};

_module = amqp.protocol_0_10;

// octet of unspecified encoding
amqp.protocol_0_10.type['BIN8'] = 0x00;
amqp.protocol_0_10.type['bin8'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bin8'].prototype = {
    'code': 0x00,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 1)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 1, value);
    }
};
amqp.protocol_0_10.typecode[0x00] = amqp.protocol_0_10.type['bin8'];
 
// 8-bit signed integral value (-128 - 127)
amqp.protocol_0_10.type['INT8'] = 0x01;
amqp.protocol_0_10.type['int8'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['int8'].prototype = {
    'code': 0x01,
    'decode': function(assembly) {return amqp.protocol.decode_int.call(_module, assembly, 1)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_int.call(_module, assembly, code, 1, value);
    }
};
amqp.protocol_0_10.typecode[0x01] = amqp.protocol_0_10.type['int8'];
 
// 8-bit unsigned integral value (0 - 255)
amqp.protocol_0_10.type['UINT8'] = 0x02;
amqp.protocol_0_10.type['uint8'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['uint8'].prototype = {
    'code': 0x02,
    'decode': function(assembly) {return amqp.protocol.decode_uint.call(_module, assembly, 1)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_uint.call(_module, assembly, code, 1, value);
    }
};
amqp.protocol_0_10.typecode[0x02] = amqp.protocol_0_10.type['uint8'];
 
// an iso-8859-15 character
amqp.protocol_0_10.type['CHAR'] = 0x04;
amqp.protocol_0_10.type['char'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['char'].prototype = {
    'code': 0x04,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 1)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 1, value);
    }
};
amqp.protocol_0_10.typecode[0x04] = amqp.protocol_0_10.type['char'];
 
// boolean value (zero represents false, nonzero represents true)
amqp.protocol_0_10.type['BOOLEAN'] = 0x08;
amqp.protocol_0_10.type['boolean'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['boolean'].prototype = {
    'code': 0x08,
    'decode': function(assembly) {return amqp.protocol.decode_bool.call(_module, assembly, 1)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bool.call(_module, assembly, code, 1, value);
    }
};
amqp.protocol_0_10.typecode[0x08] = amqp.protocol_0_10.type['boolean'];
 
// two octets of unspecified binary encoding
amqp.protocol_0_10.type['BIN16'] = 0x10;
amqp.protocol_0_10.type['bin16'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bin16'].prototype = {
    'code': 0x10,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 2)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 2, value);
    }
};
amqp.protocol_0_10.typecode[0x10] = amqp.protocol_0_10.type['bin16'];
 
// 16-bit signed integral value
amqp.protocol_0_10.type['INT16'] = 0x11;
amqp.protocol_0_10.type['int16'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['int16'].prototype = {
    'code': 0x11,
    'decode': function(assembly) {return amqp.protocol.decode_int.call(_module, assembly, 2)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_int.call(_module, assembly, code, 2, value);
    }
};
amqp.protocol_0_10.typecode[0x11] = amqp.protocol_0_10.type['int16'];
 
// 16-bit unsigned integer
amqp.protocol_0_10.type['UINT16'] = 0x12;
amqp.protocol_0_10.type['uint16'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['uint16'].prototype = {
    'code': 0x12,
    'decode': function(assembly) {return amqp.protocol.decode_uint.call(_module, assembly, 2)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_uint.call(_module, assembly, code, 2, value);
    }
};
amqp.protocol_0_10.typecode[0x12] = amqp.protocol_0_10.type['uint16'];
 
// four octets of unspecified binary encoding
amqp.protocol_0_10.type['BIN32'] = 0x20;
amqp.protocol_0_10.type['bin32'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bin32'].prototype = {
    'code': 0x20,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[0x20] = amqp.protocol_0_10.type['bin32'];
 
// 32-bit signed integral value
amqp.protocol_0_10.type['INT32'] = 0x21;
amqp.protocol_0_10.type['int32'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['int32'].prototype = {
    'code': 0x21,
    'decode': function(assembly) {return amqp.protocol.decode_int.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_int.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[0x21] = amqp.protocol_0_10.type['int32'];
 
// 32-bit unsigned integral value
amqp.protocol_0_10.type['UINT32'] = 0x22;
amqp.protocol_0_10.type['uint32'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['uint32'].prototype = {
    'code': 0x22,
    'decode': function(assembly) {return amqp.protocol.decode_uint.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_uint.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[0x22] = amqp.protocol_0_10.type['uint32'];
 
// single precision IEEE 754 32-bit floating point
amqp.protocol_0_10.type['FLOAT'] = 0x23;
amqp.protocol_0_10.type['float'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['float'].prototype = {
    'code': 0x23,
    'decode': function(assembly) {return amqp.protocol.decode_float.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_float.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[0x23] = amqp.protocol_0_10.type['float'];
 
// single unicode character in UTF-32 encoding
amqp.protocol_0_10.type['CHAR_UTF32'] = 0x27;
amqp.protocol_0_10.type['char_utf32'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['char_utf32'].prototype = {
    'code': 0x27,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[0x27] = amqp.protocol_0_10.type['char_utf32'];
 
// serial number defined in RFC-1982
amqp.protocol_0_10.type['SEQUENCE_NO'] = None;
amqp.protocol_0_10.type['sequence_no'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['sequence_no'].prototype = {
    'code': None,
    'decode': function(assembly) {return amqp.protocol.decode_uint.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_uint.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[None] = amqp.protocol_0_10.type['sequence_no'];
 
// eight octets of unspecified binary encoding
amqp.protocol_0_10.type['BIN64'] = 0x30;
amqp.protocol_0_10.type['bin64'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bin64'].prototype = {
    'code': 0x30,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 8)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 8, value);
    }
};
amqp.protocol_0_10.typecode[0x30] = amqp.protocol_0_10.type['bin64'];
 
// 64-bit signed integral value
amqp.protocol_0_10.type['INT64'] = 0x31;
amqp.protocol_0_10.type['int64'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['int64'].prototype = {
    'code': 0x31,
    'decode': function(assembly) {return amqp.protocol.decode_int.call(_module, assembly, 8)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_int.call(_module, assembly, code, 8, value);
    }
};
amqp.protocol_0_10.typecode[0x31] = amqp.protocol_0_10.type['int64'];
 
// 64-bit unsigned integral value
amqp.protocol_0_10.type['UINT64'] = 0x32;
amqp.protocol_0_10.type['uint64'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['uint64'].prototype = {
    'code': 0x32,
    'decode': function(assembly) {return amqp.protocol.decode_uint.call(_module, assembly, 8)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_uint.call(_module, assembly, code, 8, value);
    }
};
amqp.protocol_0_10.typecode[0x32] = amqp.protocol_0_10.type['uint64'];
 
// double precision IEEE 754 floating point
amqp.protocol_0_10.type['DOUBLE'] = 0x33;
amqp.protocol_0_10.type['double'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['double'].prototype = {
    'code': 0x33,
    'decode': function(assembly) {return amqp.protocol.decode_float.call(_module, assembly, 8)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_float.call(_module, assembly, code, 8, value);
    }
};
amqp.protocol_0_10.typecode[0x33] = amqp.protocol_0_10.type['double'];
 
// datetime in 64 bit POSIX time_t format
amqp.protocol_0_10.type['DATETIME'] = 0x38;
amqp.protocol_0_10.type['datetime'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['datetime'].prototype = {
    'code': 0x38,
    'decode': function(assembly) {return amqp.protocol.decode_datetime.call(_module, assembly, 8)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_datetime.call(_module, assembly, code, 8, value);
    }
};
amqp.protocol_0_10.typecode[0x38] = amqp.protocol_0_10.type['datetime'];
 
// sixteen octets of unspecified binary encoding
amqp.protocol_0_10.type['BIN128'] = 0x40;
amqp.protocol_0_10.type['bin128'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bin128'].prototype = {
    'code': 0x40,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 16)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 16, value);
    }
};
amqp.protocol_0_10.typecode[0x40] = amqp.protocol_0_10.type['bin128'];
 
// UUID (RFC-4122 section 4.1.2) - 16 octets
amqp.protocol_0_10.type['UUID'] = 0x48;
amqp.protocol_0_10.type['uuid'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['uuid'].prototype = {
    'code': 0x48,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 16)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 16, value);
    }
};
amqp.protocol_0_10.typecode[0x48] = amqp.protocol_0_10.type['uuid'];
 
// thirty two octets of unspecified binary encoding
amqp.protocol_0_10.type['BIN256'] = 0x50;
amqp.protocol_0_10.type['bin256'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bin256'].prototype = {
    'code': 0x50,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 32)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 32, value);
    }
};
amqp.protocol_0_10.typecode[0x50] = amqp.protocol_0_10.type['bin256'];
 
// sixty four octets of unspecified binary encoding
amqp.protocol_0_10.type['BIN512'] = 0x60;
amqp.protocol_0_10.type['bin512'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bin512'].prototype = {
    'code': 0x60,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 64)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 64, value);
    }
};
amqp.protocol_0_10.typecode[0x60] = amqp.protocol_0_10.type['bin512'];
 
// one hundred and twenty eight octets of unspecified binary encoding
amqp.protocol_0_10.type['BIN1024'] = 0x70;
amqp.protocol_0_10.type['bin1024'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bin1024'].prototype = {
    'code': 0x70,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 128)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 128, value);
    }
};
amqp.protocol_0_10.typecode[0x70] = amqp.protocol_0_10.type['bin1024'];
 
// up to 255 octets of opaque binary data
amqp.protocol_0_10.type['VBIN8'] = 0x80;
amqp.protocol_0_10.type['vbin8'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['vbin8'].prototype = {
    'code': 0x80,
    'decode': function(assembly) {return amqp.protocol.decode_str.call(_module, assembly, 1)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_str.call(_module, assembly, code, 1, value);
    }
};
amqp.protocol_0_10.typecode[0x80] = amqp.protocol_0_10.type['vbin8'];
 
// up to 255 iso-8859-15 characters
amqp.protocol_0_10.type['STR8_LATIN'] = 0x84;
amqp.protocol_0_10.type['str8_latin'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['str8_latin'].prototype = {
    'code': 0x84,
    'decode': function(assembly) {return amqp.protocol.decode_str.call(_module, assembly, 1)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_str.call(_module, assembly, code, 1, value);
    }
};
amqp.protocol_0_10.typecode[0x84] = amqp.protocol_0_10.type['str8_latin'];
 
// up to 255 octets worth of UTF-8 unicode
amqp.protocol_0_10.type['STR8'] = 0x85;
amqp.protocol_0_10.type['str8'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['str8'].prototype = {
    'code': 0x85,
    'decode': function(assembly) {return amqp.protocol.decode_str.call(_module, assembly, 1)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_str.call(_module, assembly, code, 1, value);
    }
};
amqp.protocol_0_10.typecode[0x85] = amqp.protocol_0_10.type['str8'];
 
// up to 255 octets worth of UTF-16 unicode
amqp.protocol_0_10.type['STR8_UTF16'] = 0x86;
amqp.protocol_0_10.type['str8_utf16'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['str8_utf16'].prototype = {
    'code': 0x86,
    'decode': function(assembly) {return amqp.protocol.decode_str.call(_module, assembly, 1)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_str.call(_module, assembly, code, 1, value);
    }
};
amqp.protocol_0_10.typecode[0x86] = amqp.protocol_0_10.type['str8_utf16'];
 
// up to 65535 octets of opaque binary data
amqp.protocol_0_10.type['VBIN16'] = 0x90;
amqp.protocol_0_10.type['vbin16'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['vbin16'].prototype = {
    'code': 0x90,
    'decode': function(assembly) {return amqp.protocol.decode_str.call(_module, assembly, 2)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_str.call(_module, assembly, code, 2, value);
    }
};
amqp.protocol_0_10.typecode[0x90] = amqp.protocol_0_10.type['vbin16'];
 
// up to 65535 iso-8859-15 characters
amqp.protocol_0_10.type['STR16_LATIN'] = 0x94;
amqp.protocol_0_10.type['str16_latin'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['str16_latin'].prototype = {
    'code': 0x94,
    'decode': function(assembly) {return amqp.protocol.decode_str.call(_module, assembly, 2)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_str.call(_module, assembly, code, 2, value);
    }
};
amqp.protocol_0_10.typecode[0x94] = amqp.protocol_0_10.type['str16_latin'];
 
// up to 65535 octets worth of UTF-8 unicode
amqp.protocol_0_10.type['STR16'] = 0x95;
amqp.protocol_0_10.type['str16'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['str16'].prototype = {
    'code': 0x95,
    'decode': function(assembly) {return amqp.protocol.decode_str.call(_module, assembly, 2)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_str.call(_module, assembly, code, 2, value);
    }
};
amqp.protocol_0_10.typecode[0x95] = amqp.protocol_0_10.type['str16'];
 
// up to 65535 octets worth of UTF-16 unicode
amqp.protocol_0_10.type['STR16_UTF16'] = 0x96;
amqp.protocol_0_10.type['str16_utf16'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['str16_utf16'].prototype = {
    'code': 0x96,
    'decode': function(assembly) {return amqp.protocol.decode_str.call(_module, assembly, 2)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_str.call(_module, assembly, code, 2, value);
    }
};
amqp.protocol_0_10.typecode[0x96] = amqp.protocol_0_10.type['str16_utf16'];
 
// byte ranges within a 64-bit payload
amqp.protocol_0_10.type['BYTE_RANGES'] = None;
amqp.protocol_0_10.type['byte_ranges'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['byte_ranges'].prototype = {
    'code': None,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 2)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 2, value);
    }
};
amqp.protocol_0_10.typecode[None] = amqp.protocol_0_10.type['byte_ranges'];
 
// ranged set representation
amqp.protocol_0_10.type['SEQUENCE_SET'] = None;
amqp.protocol_0_10.type['sequence_set'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['sequence_set'].prototype = {
    'code': None,
    'decode': function(assembly) {return amqp.protocol.decode_seq_set.call(_module, assembly, 2)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_seq_set.call(_module, assembly, code, 2, value);
    }
};
amqp.protocol_0_10.typecode[None] = amqp.protocol_0_10.type['sequence_set'];
 
// up to 4294967295 octets of opaque binary data
amqp.protocol_0_10.type['VBIN32'] = 0xa0;
amqp.protocol_0_10.type['vbin32'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['vbin32'].prototype = {
    'code': 0xa0,
    'decode': function(assembly) {return amqp.protocol.decode_str.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_str.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[0xa0] = amqp.protocol_0_10.type['vbin32'];
 
// a mapping of keys to typed values
amqp.protocol_0_10.type['MAP'] = 0xa8;
amqp.protocol_0_10.type['map'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['map'].prototype = {
    'code': 0xa8,
    'decode': function(assembly) {return amqp.protocol.decode_map.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_map.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[0xa8] = amqp.protocol_0_10.type['map'];
 
// a series of consecutive type-value pairs
amqp.protocol_0_10.type['LIST'] = 0xa9;
amqp.protocol_0_10.type['list'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['list'].prototype = {
    'code': 0xa9,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[0xa9] = amqp.protocol_0_10.type['list'];
 
// a defined length collection of values of a single type
amqp.protocol_0_10.type['ARRAY'] = 0xaa;
amqp.protocol_0_10.type['array'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['array'].prototype = {
    'code': 0xaa,
    'decode': function(assembly) {return amqp.protocol.decode_array.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_array.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[0xaa] = amqp.protocol_0_10.type['array'];
 
// a coded struct with a 32-bit size
amqp.protocol_0_10.type['STRUCT32'] = 0xab;
amqp.protocol_0_10.type['struct32'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['struct32'].prototype = {
    'code': 0xab,
    'decode': function(assembly) {return amqp.protocol.decode_str.call(_module, assembly, 4)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_str.call(_module, assembly, code, 4, value);
    }
};
amqp.protocol_0_10.typecode[0xab] = amqp.protocol_0_10.type['struct32'];
 
// five octets of unspecified binary encoding
amqp.protocol_0_10.type['BIN40'] = 0xc0;
amqp.protocol_0_10.type['bin40'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bin40'].prototype = {
    'code': 0xc0,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 5)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 5, value);
    }
};
amqp.protocol_0_10.typecode[0xc0] = amqp.protocol_0_10.type['bin40'];
 
// 32-bit decimal value (e.g. for use in financial values)
amqp.protocol_0_10.type['DEC32'] = 0xc8;
amqp.protocol_0_10.type['dec32'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['dec32'].prototype = {
    'code': 0xc8,
    'decode': function(assembly) {return amqp.protocol.decode_dec.call(_module, assembly, 5)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_dec.call(_module, assembly, code, 5, value);
    }
};
amqp.protocol_0_10.typecode[0xc8] = amqp.protocol_0_10.type['dec32'];
 
// nine octets of unspecified binary encoding
amqp.protocol_0_10.type['BIN72'] = 0xd0;
amqp.protocol_0_10.type['bin72'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bin72'].prototype = {
    'code': 0xd0,
    'decode': function(assembly) {return amqp.protocol.decode_bin.call(_module, assembly, 9)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bin.call(_module, assembly, code, 9, value);
    }
};
amqp.protocol_0_10.typecode[0xd0] = amqp.protocol_0_10.type['bin72'];
 
// 64-bit decimal value (e.g. for use in financial values)
amqp.protocol_0_10.type['DEC64'] = 0xd8;
amqp.protocol_0_10.type['dec64'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['dec64'].prototype = {
    'code': 0xd8,
    'decode': function(assembly) {return amqp.protocol.decode_dec.call(_module, assembly, 9)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_dec.call(_module, assembly, code, 9, value);
    }
};
amqp.protocol_0_10.typecode[0xd8] = amqp.protocol_0_10.type['dec64'];
 
// the void type
amqp.protocol_0_10.type['VOID'] = 0xf0;
amqp.protocol_0_10.type['void'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['void'].prototype = {
    'code': 0xf0,
    'decode': function(assembly) {return amqp.protocol.decode_void.call(_module, assembly, 0)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_void.call(_module, assembly, code, 0, value);
    }
};
amqp.protocol_0_10.typecode[0xf0] = amqp.protocol_0_10.type['void'];
 
// presence indicator
amqp.protocol_0_10.type['BIT'] = 0xf1;
amqp.protocol_0_10.type['bit'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
amqp.protocol_0_10.type['bit'].prototype = {
    'code': 0xf1,
    'decode': function(assembly) {return amqp.protocol.decode_bit.call(_module, assembly, 0)},
    'encode': function(assembly, value) {
        if (value == null || typeof(value) == 'undefined')
            value = this._value;

        var code = null;
        if (this._encode_type)
            code = this.code;

        amqp.protocol.encode_bit.call(_module, assembly, code, 0, value);
    }
};
amqp.protocol_0_10.typecode[0xf1] = amqp.protocol_0_10.type['bit'];
 
// The minimum size (in bytes) which can be     agreed upon as the maximum frame size.
amqp.protocol_0_10['MIN_MAX_FRAME_SIZE'] = 4096;
 
// work with connections
var cls_connection = {
    _defaults: {
        parsed_data: {},
        assembly: null
    },
    msg: {},
    msgcode: {},
    struct: {},
    structcode: {},
    code: 0x1,
    name: 'connection',
    _init: function(options) {
        this._options = options;
        if (typeof(this._options.parsed_data) == 'undefined')
            this._options.parsed_data = {}
    },
    get_name: function() {
        return this.name;
    },
    get_message_name: function() {
        var cc = this.message_code;
        return this.msgcode[cc].name;
    },
    get: function (key) {
        return this._options.parsed_data[key];
    },

    set: function (key, value) {
        this._options.parsed_data[key] = value;
    },

    decode: function(code) {
        this.message_code = code;
        var results = this.msgcode[code].decode(this._options.assembly);
        for (key in results) {
            this.set(key, results[key]);
        }
    },

    encode: function(code) {
        this.msgcode[code].encode(assembly, this._options.parsed_data);
    },
};
 
cls_connection.msg['start'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x1,
    cls: cls_connection,
    name: 'start',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0x1] = cls_connection.msg['start'];

// server properties
cls_connection.msg['start'].fields.push(['server_properties', _module.type.map, false, 1]);


// available security mechanisms
cls_connection.msg['start'].fields.push(['mechanisms', _module.type.array, true, 2]);


// available message locales
cls_connection.msg['start'].fields.push(['locales', _module.type.array, true, 4]);


cls_connection.msg['start_ok'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x2,
    cls: cls_connection,
    name: 'start_ok',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0x2] = cls_connection.msg['start_ok'];

// client properties
cls_connection.msg['start_ok'].fields.push(['client_properties', _module.type.map, false, 1]);


// selected security mechanism
cls_connection.msg['start_ok'].fields.push(['mechanism', _module.type.str8, true, 2]);


// security response data
cls_connection.msg['start_ok'].fields.push(['response', _module.type.vbin32, true, 4]);


// selected message locale
cls_connection.msg['start_ok'].fields.push(['locale', _module.type.str8, true, 8]);


cls_connection.msg['secure'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x3,
    cls: cls_connection,
    name: 'secure',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0x3] = cls_connection.msg['secure'];

// security challenge data
cls_connection.msg['secure'].fields.push(['challenge', _module.type.vbin32, true, 1]);


cls_connection.msg['secure_ok'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x4,
    cls: cls_connection,
    name: 'secure_ok',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0x4] = cls_connection.msg['secure_ok'];

// security response data
cls_connection.msg['secure_ok'].fields.push(['response', _module.type.vbin32, true, 1]);


cls_connection.msg['tune'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x5,
    cls: cls_connection,
    name: 'tune',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0x5] = cls_connection.msg['tune'];

// proposed maximum channels
cls_connection.msg['tune'].fields.push(['channel_max', _module.type.uint16, false, 1]);


// proposed maximum frame size
cls_connection.msg['tune'].fields.push(['max_frame_size', _module.type.uint16, false, 2]);


// the minimum supported heartbeat delay
cls_connection.msg['tune'].fields.push(['heartbeat_min', _module.type.uint16, false, 4]);


// the maximum supported heartbeat delay
cls_connection.msg['tune'].fields.push(['heartbeat_max', _module.type.uint16, false, 8]);


cls_connection.msg['tune_ok'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x6,
    cls: cls_connection,
    name: 'tune_ok',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0x6] = cls_connection.msg['tune_ok'];

// negotiated maximum channels
cls_connection.msg['tune_ok'].fields.push(['channel_max', _module.type.uint16, true, 1]);


// negotiated maximum frame size
cls_connection.msg['tune_ok'].fields.push(['max_frame_size', _module.type.uint16, false, 2]);


// negotiated heartbeat delay
cls_connection.msg['tune_ok'].fields.push(['heartbeat', _module.type.uint16, false, 4]);


cls_connection.msg['open'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x7,
    cls: cls_connection,
    name: 'open',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0x7] = cls_connection.msg['open'];

// virtual host name
cls_connection.msg['open'].fields.push(['virtual_host', _module.type.str8, true, 1]);


// required capabilities
cls_connection.msg['open'].fields.push(['capabilities', _module.type.array, false, 2]);


// insist on connecting to server
cls_connection.msg['open'].fields.push(['insist', _module.type.bit, false, 4]);


cls_connection.msg['open_ok'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x8,
    cls: cls_connection,
    name: 'open_ok',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0x8] = cls_connection.msg['open_ok'];

// alternate hosts which may be used in         the case of failure
cls_connection.msg['open_ok'].fields.push(['known_hosts', _module.type.array, false, 1]);


cls_connection.msg['redirect'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x9,
    cls: cls_connection,
    name: 'redirect',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0x9] = cls_connection.msg['redirect'];

// server to connect to
cls_connection.msg['redirect'].fields.push(['host', _module.type.str16, true, 1]);


// alternate hosts to try in case of         failure
cls_connection.msg['redirect'].fields.push(['known_hosts', _module.type.array, false, 2]);


cls_connection.msg['heartbeat'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0xa,
    cls: cls_connection,
    name: 'heartbeat',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0xa] = cls_connection.msg['heartbeat'];

cls_connection.msg['close'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0xb,
    cls: cls_connection,
    name: 'close',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0xb] = cls_connection.msg['close'];

// the numeric reply code
cls_connection.msg['close'].fields.push(['reply_code', _module.type.uint16, true, 1]);


// the localized reply text
cls_connection.msg['close'].fields.push(['reply_text', _module.type.str8, false, 2]);


cls_connection.msg['close_ok'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0xc,
    cls: cls_connection,
    name: 'close_ok',
    cls_name: 'connection',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_connection.msgcode[0xc] = cls_connection.msg['close_ok'];

amqp.protocol_0_10.cls['connection'] = amqp.protocol.MetaClass(cls_connection);
amqp.protocol_0_10.clscode[0x1] = amqp.protocol_0_10.cls['connection'];

// session controls
var cls_session = {
    _defaults: {
        parsed_data: {},
        assembly: null
    },
    msg: {},
    msgcode: {},
    struct: {},
    structcode: {},
    code: 0x2,
    name: 'session',
    _init: function(options) {
        this._options = options;
        if (typeof(this._options.parsed_data) == 'undefined')
            this._options.parsed_data = {}
    },
    get_name: function() {
        return this.name;
    },
    get_message_name: function() {
        var cc = this.message_code;
        return this.msgcode[cc].name;
    },
    get: function (key) {
        return this._options.parsed_data[key];
    },

    set: function (key, value) {
        this._options.parsed_data[key] = value;
    },

    decode: function(code) {
        this.message_code = code;
        var results = this.msgcode[code].decode(this._options.assembly);
        for (key in results) {
            this.set(key, results[key]);
        }
    },

    encode: function(code) {
        this.msgcode[code].encode(assembly, this._options.parsed_data);
    },
};
 
cls_session.struct['HEADER'] = 0;
cls_session.struct['header'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_session.struct['header'].prototype = {
    name: 'header',
    code: 0,
    pack_size: 1,
    size: 1,
    cls: amqp.protocol_0_10.cls.session,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_session.structcode[0] = cls_session.struct['header'];
 
// request notification of completion
cls_session.struct['header'].prototype.fields.push(['sync', _module.type.bit, false, 1]);


cls_session.struct['COMMAND_FRAGMENT'] = 0;
cls_session.struct['command_fragment'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_session.struct['command_fragment'].prototype = {
    name: 'command_fragment',
    code: 0,
    pack_size: 0,
    size: 0,
    cls: amqp.protocol_0_10.cls.session,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_session.structcode[0] = cls_session.struct['command_fragment'];
 
// None
cls_session.struct['command_fragment'].prototype.fields.push(['command_id', _module.type.sequence_no, true, 1]);


// None
cls_session.struct['command_fragment'].prototype.fields.push(['byte_ranges', _module.type.byte_ranges, true, 2]);


cls_session.msg['attach'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x1,
    cls: cls_session,
    name: 'attach',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0x1] = cls_session.msg['attach'];

// the session name
cls_session.msg['attach'].fields.push(['name', _module.type.vbin16, true, 1]);


// force attachment to a busy session
cls_session.msg['attach'].fields.push(['force', _module.type.bit, false, 2]);


cls_session.msg['attached'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x2,
    cls: cls_session,
    name: 'attached',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0x2] = cls_session.msg['attached'];

// the session name
cls_session.msg['attached'].fields.push(['name', _module.type.vbin16, true, 1]);


cls_session.msg['detach'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x3,
    cls: cls_session,
    name: 'detach',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0x3] = cls_session.msg['detach'];

// the session name
cls_session.msg['detach'].fields.push(['name', _module.type.vbin16, true, 1]);


cls_session.msg['detached'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x4,
    cls: cls_session,
    name: 'detached',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0x4] = cls_session.msg['detached'];

// the session name
cls_session.msg['detached'].fields.push(['name', _module.type.vbin16, true, 1]);


// the reason for detach
cls_session.msg['detached'].fields.push(['code', _module.type.uint8, true, 2]);


cls_session.msg['request_timeout'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x5,
    cls: cls_session,
    name: 'request_timeout',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0x5] = cls_session.msg['request_timeout'];

// the requested timeout
cls_session.msg['request_timeout'].fields.push(['timeout', _module.type.uint32, false, 1]);


cls_session.msg['timeout'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x6,
    cls: cls_session,
    name: 'timeout',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0x6] = cls_session.msg['timeout'];

// the execution timeout
cls_session.msg['timeout'].fields.push(['timeout', _module.type.uint32, false, 1]);


cls_session.msg['command_point'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x7,
    cls: cls_session,
    name: 'command_point',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0x7] = cls_session.msg['command_point'];

// the command-id of the next command
cls_session.msg['command_point'].fields.push(['command_id', _module.type.sequence_no, true, 1]);


// the byte offset within the command
cls_session.msg['command_point'].fields.push(['command_offset', _module.type.uint64, true, 2]);


cls_session.msg['expected'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x8,
    cls: cls_session,
    name: 'expected',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0x8] = cls_session.msg['expected'];

// expected commands
cls_session.msg['expected'].fields.push(['commands', _module.type.sequence_set, true, 1]);


// expected fragments
cls_session.msg['expected'].fields.push(['fragments', _module.type.array, false, 2]);


cls_session.msg['confirmed'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0x9,
    cls: cls_session,
    name: 'confirmed',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0x9] = cls_session.msg['confirmed'];

// entirely confirmed commands
cls_session.msg['confirmed'].fields.push(['commands', _module.type.sequence_set, false, 1]);


// partially confirmed commands
cls_session.msg['confirmed'].fields.push(['fragments', _module.type.array, false, 2]);


cls_session.msg['completed'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0xa,
    cls: cls_session,
    name: 'completed',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0xa] = cls_session.msg['completed'];

// completed commands
cls_session.msg['completed'].fields.push(['commands', _module.type.sequence_set, false, 1]);


// None
cls_session.msg['completed'].fields.push(['timely_reply', _module.type.bit, false, 2]);


cls_session.msg['known_completed'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0xb,
    cls: cls_session,
    name: 'known_completed',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0xb] = cls_session.msg['known_completed'];

// commands known to be complete
cls_session.msg['known_completed'].fields.push(['commands', _module.type.sequence_set, false, 1]);


cls_session.msg['flush'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0xc,
    cls: cls_session,
    name: 'flush',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0xc] = cls_session.msg['flush'];

// request notification of expected commands
cls_session.msg['flush'].fields.push(['expected', _module.type.bit, false, 1]);


// request notification of confirmed commands
cls_session.msg['flush'].fields.push(['confirmed', _module.type.bit, false, 2]);


// request notification of completed commands
cls_session.msg['flush'].fields.push(['completed', _module.type.bit, false, 4]);


cls_session.msg['gap'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    type: 0,
    code: 0xd,
    cls: cls_session,
    name: 'gap',
    cls_name: 'session',
    decode: function(assembly) {
        var result = {};
        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var required = this.fields[i][2];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            } else if (required) {
                throw "Parameter " + name + " is required for message" + this.cls_name + "." + this.name;
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_session.msgcode[0xd] = cls_session.msg['gap'];

// None
cls_session.msg['gap'].fields.push(['commands', _module.type.sequence_set, false, 1]);


amqp.protocol_0_10.cls['session'] = amqp.protocol.MetaClass(cls_session);
amqp.protocol_0_10.clscode[0x2] = amqp.protocol_0_10.cls['session'];

// execution commands
var cls_execution = {
    _defaults: {
        parsed_data: {},
        assembly: null
    },
    msg: {},
    msgcode: {},
    struct: {},
    structcode: {},
    code: 0x3,
    name: 'execution',
    _init: function(options) {
        this._options = options;
        if (typeof(this._options.parsed_data) == 'undefined')
            this._options.parsed_data = {}
    },
    get_name: function() {
        return this.name;
    },
    get_message_name: function() {
        var cc = this.message_code;
        return this.msgcode[cc].name;
    },
    get: function (key) {
        return this._options.parsed_data[key];
    },

    set: function (key, value) {
        this._options.parsed_data[key] = value;
    },

    decode: function(code) {
        this.message_code = code;
        var results = this.msgcode[code].decode(this._options.assembly);
        for (key in results) {
            this.set(key, results[key]);
        }
    },

    encode: function(code) {
        this.msgcode[code].encode(assembly, this._options.parsed_data);
    },
};
 
cls_execution.msg['sync'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x1,
    cls: cls_execution,
    name: 'sync',
    cls_name: 'execution',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_execution.msgcode[0x1] = cls_execution.msg['sync'];

cls_execution.msg['result'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x2,
    cls: cls_execution,
    name: 'result',
    cls_name: 'execution',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_execution.msgcode[0x2] = cls_execution.msg['result'];

// None
cls_execution.msg['result'].fields.push(['command_id', _module.type.sequence_no, true, 1]);


// None
cls_execution.msg['result'].fields.push(['value', _module.type.struct32, false, 2]);


cls_execution.msg['exception'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x3,
    cls: cls_execution,
    name: 'exception',
    cls_name: 'execution',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_execution.msgcode[0x3] = cls_execution.msg['exception'];

// error code indicating the         type of error
cls_execution.msg['exception'].fields.push(['error_code', _module.type.uint16, true, 1]);


// exceptional command
cls_execution.msg['exception'].fields.push(['command_id', _module.type.sequence_no, false, 2]);


// the class code of the command whose execution         gave rise to the error (if appropriate)
cls_execution.msg['exception'].fields.push(['class_code', _module.type.uint8, false, 4]);


// the class code of the command whose execution         gave rise to the error (if appropriate)
cls_execution.msg['exception'].fields.push(['command_code', _module.type.uint8, false, 8]);


// index of the exceptional field
cls_execution.msg['exception'].fields.push(['field_index', _module.type.uint8, false, 16]);


// descriptive text on the exception
cls_execution.msg['exception'].fields.push(['description', _module.type.str16, false, 32]);


// map to carry additional information about the         error
cls_execution.msg['exception'].fields.push(['error_info', _module.type.map, false, 64]);


amqp.protocol_0_10.cls['execution'] = amqp.protocol.MetaClass(cls_execution);
amqp.protocol_0_10.clscode[0x3] = amqp.protocol_0_10.cls['execution'];

// message transfer
var cls_message = {
    _defaults: {
        parsed_data: {},
        assembly: null
    },
    msg: {},
    msgcode: {},
    struct: {},
    structcode: {},
    code: 0x4,
    name: 'message',
    _init: function(options) {
        this._options = options;
        if (typeof(this._options.parsed_data) == 'undefined')
            this._options.parsed_data = {}
    },
    get_name: function() {
        return this.name;
    },
    get_message_name: function() {
        var cc = this.message_code;
        return this.msgcode[cc].name;
    },
    get: function (key) {
        return this._options.parsed_data[key];
    },

    set: function (key, value) {
        this._options.parsed_data[key] = value;
    },

    decode: function(code) {
        this.message_code = code;
        var results = this.msgcode[code].decode(this._options.assembly);
        for (key in results) {
            this.set(key, results[key]);
        }
    },

    encode: function(code) {
        this.msgcode[code].encode(assembly, this._options.parsed_data);
    },
};
 
cls_message.struct['DELIVERY_PROPERTIES'] = 0x1;
cls_message.struct['delivery_properties'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_message.struct['delivery_properties'].prototype = {
    name: 'delivery_properties',
    code: 0x1,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.message,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_message.structcode[0x1] = cls_message.struct['delivery_properties'];
 
// controls discard of unroutable messages
cls_message.struct['delivery_properties'].prototype.fields.push(['discard_unroutable', _module.type.bit, false, 1]);


// Consider message unroutable if it cannot be         processed immediately
cls_message.struct['delivery_properties'].prototype.fields.push(['immediate', _module.type.bit, false, 2]);


// redelivery flag
cls_message.struct['delivery_properties'].prototype.fields.push(['redelivered', _module.type.bit, false, 4]);


// message priority, 0 to 9
cls_message.struct['delivery_properties'].prototype.fields.push(['priority', _module.type.uint8, true, 8]);


// message persistence requirement
cls_message.struct['delivery_properties'].prototype.fields.push(['delivery_mode', _module.type.uint8, true, 16]);


// time to live in ms
cls_message.struct['delivery_properties'].prototype.fields.push(['ttl', _module.type.uint64, false, 32]);


// message timestamp
cls_message.struct['delivery_properties'].prototype.fields.push(['timestamp', _module.type.datetime, false, 64]);


// message expiration time
cls_message.struct['delivery_properties'].prototype.fields.push(['expiration', _module.type.datetime, false, 128]);


// originating exchange
cls_message.struct['delivery_properties'].prototype.fields.push(['exchange', _module.type.str8, false, 256]);


// message routing key
cls_message.struct['delivery_properties'].prototype.fields.push(['routing_key', _module.type.str8, false, 512]);


// global id for message transfer
cls_message.struct['delivery_properties'].prototype.fields.push(['resume_id', _module.type.str16, false, 1024]);


// ttl in ms for interrupted message data
cls_message.struct['delivery_properties'].prototype.fields.push(['resume_ttl', _module.type.uint64, false, 2048]);


cls_message.struct['FRAGMENT_PROPERTIES'] = 0x2;
cls_message.struct['fragment_properties'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_message.struct['fragment_properties'].prototype = {
    name: 'fragment_properties',
    code: 0x2,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.message,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_message.structcode[0x2] = cls_message.struct['fragment_properties'];
 
// None
cls_message.struct['fragment_properties'].prototype.fields.push(['first', _module.type.bit, false, 1]);


// None
cls_message.struct['fragment_properties'].prototype.fields.push(['last', _module.type.bit, false, 2]);


// None
cls_message.struct['fragment_properties'].prototype.fields.push(['fragment_size', _module.type.uint64, false, 4]);


cls_message.struct['REPLY_TO'] = 0;
cls_message.struct['reply_to'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_message.struct['reply_to'].prototype = {
    name: 'reply_to',
    code: 0,
    pack_size: 2,
    size: 2,
    cls: amqp.protocol_0_10.cls.message,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_message.structcode[0] = cls_message.struct['reply_to'];
 
// the name of the exchange to reply to
cls_message.struct['reply_to'].prototype.fields.push(['exchange', _module.type.str8, false, 1]);


// the routing-key to use when replying
cls_message.struct['reply_to'].prototype.fields.push(['routing_key', _module.type.str8, false, 2]);


cls_message.struct['MESSAGE_PROPERTIES'] = 0x3;
cls_message.struct['message_properties'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_message.struct['message_properties'].prototype = {
    name: 'message_properties',
    code: 0x3,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.message,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_message.structcode[0x3] = cls_message.struct['message_properties'];
 
// length of the body segment in bytes
cls_message.struct['message_properties'].prototype.fields.push(['content_length', _module.type.uint64, false, 1]);


// application message identifier
cls_message.struct['message_properties'].prototype.fields.push(['message_id', _module.type.uuid, false, 2]);


// application correlation identifier
cls_message.struct['message_properties'].prototype.fields.push(['correlation_id', _module.type.vbin16, false, 4]);


// destination to reply to
cls_message.struct['message_properties'].prototype.fields.push(['reply_to', cls_message.struct.reply_to, false, 8]);


// MIME content type
cls_message.struct['message_properties'].prototype.fields.push(['content_type', _module.type.str8, false, 16]);


// MIME content encoding
cls_message.struct['message_properties'].prototype.fields.push(['content_encoding', _module.type.str8, false, 32]);


// creating user id
cls_message.struct['message_properties'].prototype.fields.push(['user_id', _module.type.vbin16, false, 64]);


// creating application id
cls_message.struct['message_properties'].prototype.fields.push(['app_id', _module.type.vbin16, false, 128]);


// application specific headers table
cls_message.struct['message_properties'].prototype.fields.push(['application_headers', _module.type.map, false, 256]);


cls_message.msg['transfer'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x1,
    cls: cls_message,
    name: 'transfer',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0x1] = cls_message.msg['transfer'];

// message destination
cls_message.msg['transfer'].fields.push(['destination', _module.type.str8, false, 1]);


// None
cls_message.msg['transfer'].fields.push(['accept_mode', _module.type.uint8, true, 2]);


// None
cls_message.msg['transfer'].fields.push(['acquire_mode', _module.type.uint8, true, 4]);


cls_message.msg['accept'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x2,
    cls: cls_message,
    name: 'accept',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0x2] = cls_message.msg['accept'];

// None
cls_message.msg['accept'].fields.push(['transfers', _module.type.sequence_set, true, 1]);


cls_message.msg['reject'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x3,
    cls: cls_message,
    name: 'reject',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0x3] = cls_message.msg['reject'];

// None
cls_message.msg['reject'].fields.push(['transfers', _module.type.sequence_set, true, 1]);


// None
cls_message.msg['reject'].fields.push(['code', _module.type.uint16, true, 2]);


// informational text for message reject
cls_message.msg['reject'].fields.push(['text', _module.type.str8, false, 4]);


cls_message.msg['release'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x4,
    cls: cls_message,
    name: 'release',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0x4] = cls_message.msg['release'];

// None
cls_message.msg['release'].fields.push(['transfers', _module.type.sequence_set, true, 1]);


// mark the released messages as redelivered
cls_message.msg['release'].fields.push(['set_redelivered', _module.type.bit, false, 2]);


cls_message.msg['acquire'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x5,
    cls: cls_message,
    name: 'acquire',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0x5] = cls_message.msg['acquire'];

// None
cls_message.msg['acquire'].fields.push(['transfers', _module.type.sequence_set, true, 1]);


cls_message.struct['ACQUIRED'] = 0x4;
cls_message.struct['acquired'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_message.struct['acquired'].prototype = {
    name: 'acquired',
    code: 0x4,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.message,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_message.structcode[0x4] = cls_message.struct['acquired'];
 
// None
cls_message.struct['acquired'].prototype.fields.push(['transfers', _module.type.sequence_set, true, 1]);


cls_message.msg['resume'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x6,
    cls: cls_message,
    name: 'resume',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0x6] = cls_message.msg['resume'];

// None
cls_message.msg['resume'].fields.push(['destination', _module.type.str8, false, 1]);


// None
cls_message.msg['resume'].fields.push(['resume_id', _module.type.str16, true, 2]);


cls_message.struct['MESSAGE_RESUME_RESULT'] = 0x5;
cls_message.struct['message_resume_result'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_message.struct['message_resume_result'].prototype = {
    name: 'message_resume_result',
    code: 0x5,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.message,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_message.structcode[0x5] = cls_message.struct['message_resume_result'];
 
// None
cls_message.struct['message_resume_result'].prototype.fields.push(['offset', _module.type.uint64, false, 1]);


cls_message.msg['subscribe'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x7,
    cls: cls_message,
    name: 'subscribe',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0x7] = cls_message.msg['subscribe'];

// None
cls_message.msg['subscribe'].fields.push(['queue', _module.type.str8, true, 1]);


// incoming message destination
cls_message.msg['subscribe'].fields.push(['destination', _module.type.str8, false, 2]);


// None
cls_message.msg['subscribe'].fields.push(['accept_mode', _module.type.uint8, true, 4]);


// None
cls_message.msg['subscribe'].fields.push(['acquire_mode', _module.type.uint8, true, 8]);


// request exclusive access
cls_message.msg['subscribe'].fields.push(['exclusive', _module.type.bit, false, 16]);


// None
cls_message.msg['subscribe'].fields.push(['resume_id', _module.type.str16, false, 32]);


// None
cls_message.msg['subscribe'].fields.push(['resume_ttl', _module.type.uint64, false, 64]);


// arguments for vendor extensions
cls_message.msg['subscribe'].fields.push(['arguments', _module.type.map, false, 128]);


cls_message.msg['cancel'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x8,
    cls: cls_message,
    name: 'cancel',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0x8] = cls_message.msg['cancel'];

// None
cls_message.msg['cancel'].fields.push(['destination', _module.type.str8, true, 1]);


cls_message.msg['set_flow_mode'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x9,
    cls: cls_message,
    name: 'set_flow_mode',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0x9] = cls_message.msg['set_flow_mode'];

// None
cls_message.msg['set_flow_mode'].fields.push(['destination', _module.type.str8, false, 1]);


// None
cls_message.msg['set_flow_mode'].fields.push(['flow_mode', _module.type.uint8, true, 2]);


cls_message.msg['flow'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0xa,
    cls: cls_message,
    name: 'flow',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0xa] = cls_message.msg['flow'];

// None
cls_message.msg['flow'].fields.push(['destination', _module.type.str8, false, 1]);


// None
cls_message.msg['flow'].fields.push(['unit', _module.type.uint8, true, 2]);


// None
cls_message.msg['flow'].fields.push(['value', _module.type.uint32, false, 4]);


cls_message.msg['flush'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0xb,
    cls: cls_message,
    name: 'flush',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0xb] = cls_message.msg['flush'];

// None
cls_message.msg['flush'].fields.push(['destination', _module.type.str8, false, 1]);


cls_message.msg['stop'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0xc,
    cls: cls_message,
    name: 'stop',
    cls_name: 'message',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_message.msgcode[0xc] = cls_message.msg['stop'];

// None
cls_message.msg['stop'].fields.push(['destination', _module.type.str8, false, 1]);


amqp.protocol_0_10.cls['message'] = amqp.protocol.MetaClass(cls_message);
amqp.protocol_0_10.clscode[0x4] = amqp.protocol_0_10.cls['message'];

// work with standard transactions
var cls_tx = {
    _defaults: {
        parsed_data: {},
        assembly: null
    },
    msg: {},
    msgcode: {},
    struct: {},
    structcode: {},
    code: 0x5,
    name: 'tx',
    _init: function(options) {
        this._options = options;
        if (typeof(this._options.parsed_data) == 'undefined')
            this._options.parsed_data = {}
    },
    get_name: function() {
        return this.name;
    },
    get_message_name: function() {
        var cc = this.message_code;
        return this.msgcode[cc].name;
    },
    get: function (key) {
        return this._options.parsed_data[key];
    },

    set: function (key, value) {
        this._options.parsed_data[key] = value;
    },

    decode: function(code) {
        this.message_code = code;
        var results = this.msgcode[code].decode(this._options.assembly);
        for (key in results) {
            this.set(key, results[key]);
        }
    },

    encode: function(code) {
        this.msgcode[code].encode(assembly, this._options.parsed_data);
    },
};
 
cls_tx.msg['select'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x1,
    cls: cls_tx,
    name: 'select',
    cls_name: 'tx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_tx.msgcode[0x1] = cls_tx.msg['select'];

cls_tx.msg['commit'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x2,
    cls: cls_tx,
    name: 'commit',
    cls_name: 'tx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_tx.msgcode[0x2] = cls_tx.msg['commit'];

cls_tx.msg['rollback'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x3,
    cls: cls_tx,
    name: 'rollback',
    cls_name: 'tx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_tx.msgcode[0x3] = cls_tx.msg['rollback'];

amqp.protocol_0_10.cls['tx'] = amqp.protocol.MetaClass(cls_tx);
amqp.protocol_0_10.clscode[0x5] = amqp.protocol_0_10.cls['tx'];

// Demarcates dtx branches
var cls_dtx = {
    _defaults: {
        parsed_data: {},
        assembly: null
    },
    msg: {},
    msgcode: {},
    struct: {},
    structcode: {},
    code: 0x6,
    name: 'dtx',
    _init: function(options) {
        this._options = options;
        if (typeof(this._options.parsed_data) == 'undefined')
            this._options.parsed_data = {}
    },
    get_name: function() {
        return this.name;
    },
    get_message_name: function() {
        var cc = this.message_code;
        return this.msgcode[cc].name;
    },
    get: function (key) {
        return this._options.parsed_data[key];
    },

    set: function (key, value) {
        this._options.parsed_data[key] = value;
    },

    decode: function(code) {
        this.message_code = code;
        var results = this.msgcode[code].decode(this._options.assembly);
        for (key in results) {
            this.set(key, results[key]);
        }
    },

    encode: function(code) {
        this.msgcode[code].encode(assembly, this._options.parsed_data);
    },
};
 
cls_dtx.struct['XA_RESULT'] = 0x1;
cls_dtx.struct['xa_result'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_dtx.struct['xa_result'].prototype = {
    name: 'xa_result',
    code: 0x1,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.dtx,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_dtx.structcode[0x1] = cls_dtx.struct['xa_result'];
 
// None
cls_dtx.struct['xa_result'].prototype.fields.push(['status', _module.type.uint16, true, 1]);


cls_dtx.struct['XID'] = 0x4;
cls_dtx.struct['xid'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_dtx.struct['xid'].prototype = {
    name: 'xid',
    code: 0x4,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.dtx,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_dtx.structcode[0x4] = cls_dtx.struct['xid'];
 
// implementation specific format code
cls_dtx.struct['xid'].prototype.fields.push(['format', _module.type.uint32, true, 1]);


// global transaction id
cls_dtx.struct['xid'].prototype.fields.push(['global_id', _module.type.vbin8, true, 2]);


// branch qualifier
cls_dtx.struct['xid'].prototype.fields.push(['branch_id', _module.type.vbin8, true, 4]);


cls_dtx.msg['select'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x1,
    cls: cls_dtx,
    name: 'select',
    cls_name: 'dtx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_dtx.msgcode[0x1] = cls_dtx.msg['select'];

cls_dtx.msg['start'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x2,
    cls: cls_dtx,
    name: 'start',
    cls_name: 'dtx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_dtx.msgcode[0x2] = cls_dtx.msg['start'];

// Transaction xid
cls_dtx.msg['start'].fields.push(['xid', cls_dtx.struct.xid, true, 1]);


// Join with existing xid flag
cls_dtx.msg['start'].fields.push(['join', _module.type.bit, false, 2]);


// Resume flag
cls_dtx.msg['start'].fields.push(['resume', _module.type.bit, false, 4]);


cls_dtx.msg['end'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x3,
    cls: cls_dtx,
    name: 'end',
    cls_name: 'dtx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_dtx.msgcode[0x3] = cls_dtx.msg['end'];

// Transaction xid
cls_dtx.msg['end'].fields.push(['xid', cls_dtx.struct.xid, true, 1]);


// Failure flag
cls_dtx.msg['end'].fields.push(['fail', _module.type.bit, false, 2]);


// Temporary suspension flag
cls_dtx.msg['end'].fields.push(['suspend', _module.type.bit, false, 4]);


cls_dtx.msg['commit'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x4,
    cls: cls_dtx,
    name: 'commit',
    cls_name: 'dtx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_dtx.msgcode[0x4] = cls_dtx.msg['commit'];

// Transaction xid
cls_dtx.msg['commit'].fields.push(['xid', cls_dtx.struct.xid, true, 1]);


// One-phase optimization flag
cls_dtx.msg['commit'].fields.push(['one_phase', _module.type.bit, false, 2]);


cls_dtx.msg['forget'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x5,
    cls: cls_dtx,
    name: 'forget',
    cls_name: 'dtx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_dtx.msgcode[0x5] = cls_dtx.msg['forget'];

// Transaction xid
cls_dtx.msg['forget'].fields.push(['xid', cls_dtx.struct.xid, true, 1]);


cls_dtx.msg['get_timeout'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x6,
    cls: cls_dtx,
    name: 'get_timeout',
    cls_name: 'dtx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_dtx.msgcode[0x6] = cls_dtx.msg['get_timeout'];

// Transaction xid
cls_dtx.msg['get_timeout'].fields.push(['xid', cls_dtx.struct.xid, true, 1]);


cls_dtx.struct['GET_TIMEOUT_RESULT'] = 0x2;
cls_dtx.struct['get_timeout_result'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_dtx.struct['get_timeout_result'].prototype = {
    name: 'get_timeout_result',
    code: 0x2,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.dtx,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_dtx.structcode[0x2] = cls_dtx.struct['get_timeout_result'];
 
// The current transaction timeout value
cls_dtx.struct['get_timeout_result'].prototype.fields.push(['timeout', _module.type.uint32, true, 1]);


cls_dtx.msg['prepare'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x7,
    cls: cls_dtx,
    name: 'prepare',
    cls_name: 'dtx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_dtx.msgcode[0x7] = cls_dtx.msg['prepare'];

// Transaction xid
cls_dtx.msg['prepare'].fields.push(['xid', cls_dtx.struct.xid, true, 1]);


cls_dtx.msg['recover'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x8,
    cls: cls_dtx,
    name: 'recover',
    cls_name: 'dtx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_dtx.msgcode[0x8] = cls_dtx.msg['recover'];

cls_dtx.struct['RECOVER_RESULT'] = 0x3;
cls_dtx.struct['recover_result'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_dtx.struct['recover_result'].prototype = {
    name: 'recover_result',
    code: 0x3,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.dtx,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_dtx.structcode[0x3] = cls_dtx.struct['recover_result'];
 
// array of xids to be recovered
cls_dtx.struct['recover_result'].prototype.fields.push(['in_doubt', _module.type.array, true, 1]);


cls_dtx.msg['rollback'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x9,
    cls: cls_dtx,
    name: 'rollback',
    cls_name: 'dtx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_dtx.msgcode[0x9] = cls_dtx.msg['rollback'];

// Transaction xid
cls_dtx.msg['rollback'].fields.push(['xid', cls_dtx.struct.xid, true, 1]);


cls_dtx.msg['set_timeout'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0xa,
    cls: cls_dtx,
    name: 'set_timeout',
    cls_name: 'dtx',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_dtx.msgcode[0xa] = cls_dtx.msg['set_timeout'];

// Transaction xid
cls_dtx.msg['set_timeout'].fields.push(['xid', cls_dtx.struct.xid, true, 1]);


// Dtx timeout in seconds
cls_dtx.msg['set_timeout'].fields.push(['timeout', _module.type.uint32, true, 2]);


amqp.protocol_0_10.cls['dtx'] = amqp.protocol.MetaClass(cls_dtx);
amqp.protocol_0_10.clscode[0x6] = amqp.protocol_0_10.cls['dtx'];

// work with exchanges
var cls_exchange = {
    _defaults: {
        parsed_data: {},
        assembly: null
    },
    msg: {},
    msgcode: {},
    struct: {},
    structcode: {},
    code: 0x7,
    name: 'exchange',
    _init: function(options) {
        this._options = options;
        if (typeof(this._options.parsed_data) == 'undefined')
            this._options.parsed_data = {}
    },
    get_name: function() {
        return this.name;
    },
    get_message_name: function() {
        var cc = this.message_code;
        return this.msgcode[cc].name;
    },
    get: function (key) {
        return this._options.parsed_data[key];
    },

    set: function (key, value) {
        this._options.parsed_data[key] = value;
    },

    decode: function(code) {
        this.message_code = code;
        var results = this.msgcode[code].decode(this._options.assembly);
        for (key in results) {
            this.set(key, results[key]);
        }
    },

    encode: function(code) {
        this.msgcode[code].encode(assembly, this._options.parsed_data);
    },
};
 
cls_exchange.msg['declare'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x1,
    cls: cls_exchange,
    name: 'declare',
    cls_name: 'exchange',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_exchange.msgcode[0x1] = cls_exchange.msg['declare'];

// None
cls_exchange.msg['declare'].fields.push(['exchange', _module.type.str8, true, 1]);


// exchange type
cls_exchange.msg['declare'].fields.push(['type', _module.type.str8, true, 2]);


// exchange name for unroutable messages
cls_exchange.msg['declare'].fields.push(['alternate_exchange', _module.type.str8, false, 4]);


// do not create exchange
cls_exchange.msg['declare'].fields.push(['passive', _module.type.bit, false, 8]);


// request a durable exchange
cls_exchange.msg['declare'].fields.push(['durable', _module.type.bit, false, 16]);


// auto-delete when unused
cls_exchange.msg['declare'].fields.push(['auto_delete', _module.type.bit, false, 32]);


// arguments for declaration
cls_exchange.msg['declare'].fields.push(['arguments', _module.type.map, false, 64]);


cls_exchange.msg['delete'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x2,
    cls: cls_exchange,
    name: 'delete',
    cls_name: 'exchange',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_exchange.msgcode[0x2] = cls_exchange.msg['delete'];

// None
cls_exchange.msg['delete'].fields.push(['exchange', _module.type.str8, true, 1]);


// delete only if unused
cls_exchange.msg['delete'].fields.push(['if_unused', _module.type.bit, false, 2]);


cls_exchange.msg['query'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x3,
    cls: cls_exchange,
    name: 'query',
    cls_name: 'exchange',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_exchange.msgcode[0x3] = cls_exchange.msg['query'];

// the exchange name
cls_exchange.msg['query'].fields.push(['name', _module.type.str8, false, 1]);


cls_exchange.struct['EXCHANGE_QUERY_RESULT'] = 0x1;
cls_exchange.struct['exchange_query_result'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_exchange.struct['exchange_query_result'].prototype = {
    name: 'exchange_query_result',
    code: 0x1,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.exchange,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_exchange.structcode[0x1] = cls_exchange.struct['exchange_query_result'];
 
// indicate the exchange type
cls_exchange.struct['exchange_query_result'].prototype.fields.push(['type', _module.type.str8, false, 1]);


// indicate the durability
cls_exchange.struct['exchange_query_result'].prototype.fields.push(['durable', _module.type.bit, false, 2]);


// indicate an unknown exchange
cls_exchange.struct['exchange_query_result'].prototype.fields.push(['not_found', _module.type.bit, false, 4]);


// other unspecified exchange properties
cls_exchange.struct['exchange_query_result'].prototype.fields.push(['arguments', _module.type.map, false, 8]);


cls_exchange.msg['bind'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x4,
    cls: cls_exchange,
    name: 'bind',
    cls_name: 'exchange',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_exchange.msgcode[0x4] = cls_exchange.msg['bind'];

// None
cls_exchange.msg['bind'].fields.push(['queue', _module.type.str8, true, 1]);


// name of the exchange to bind to
cls_exchange.msg['bind'].fields.push(['exchange', _module.type.str8, true, 2]);


// identifies a binding between a given exchange and queue
cls_exchange.msg['bind'].fields.push(['binding_key', _module.type.str8, true, 4]);


// arguments for binding
cls_exchange.msg['bind'].fields.push(['arguments', _module.type.map, false, 8]);


cls_exchange.msg['unbind'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x5,
    cls: cls_exchange,
    name: 'unbind',
    cls_name: 'exchange',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_exchange.msgcode[0x5] = cls_exchange.msg['unbind'];

// None
cls_exchange.msg['unbind'].fields.push(['queue', _module.type.str8, true, 1]);


// None
cls_exchange.msg['unbind'].fields.push(['exchange', _module.type.str8, true, 2]);


// the key of the binding
cls_exchange.msg['unbind'].fields.push(['binding_key', _module.type.str8, true, 4]);


cls_exchange.msg['bound'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x6,
    cls: cls_exchange,
    name: 'bound',
    cls_name: 'exchange',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_exchange.msgcode[0x6] = cls_exchange.msg['bound'];

// the exchange name
cls_exchange.msg['bound'].fields.push(['exchange', _module.type.str8, false, 1]);


// a queue name
cls_exchange.msg['bound'].fields.push(['queue', _module.type.str8, true, 2]);


// a binding-key
cls_exchange.msg['bound'].fields.push(['binding_key', _module.type.str8, false, 4]);


// a set of binding arguments
cls_exchange.msg['bound'].fields.push(['arguments', _module.type.map, false, 8]);


cls_exchange.struct['EXCHANGE_BOUND_RESULT'] = 0x2;
cls_exchange.struct['exchange_bound_result'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_exchange.struct['exchange_bound_result'].prototype = {
    name: 'exchange_bound_result',
    code: 0x2,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.exchange,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_exchange.structcode[0x2] = cls_exchange.struct['exchange_bound_result'];
 
// indicate an unknown exchange
cls_exchange.struct['exchange_bound_result'].prototype.fields.push(['exchange_not_found', _module.type.bit, false, 1]);


// indicate an unknown queue
cls_exchange.struct['exchange_bound_result'].prototype.fields.push(['queue_not_found', _module.type.bit, false, 2]);


// indicate no matching queue
cls_exchange.struct['exchange_bound_result'].prototype.fields.push(['queue_not_matched', _module.type.bit, false, 4]);


// indicate no matching binding-key
cls_exchange.struct['exchange_bound_result'].prototype.fields.push(['key_not_matched', _module.type.bit, false, 8]);


// indicate no matching arguments
cls_exchange.struct['exchange_bound_result'].prototype.fields.push(['args_not_matched', _module.type.bit, false, 16]);


amqp.protocol_0_10.cls['exchange'] = amqp.protocol.MetaClass(cls_exchange);
amqp.protocol_0_10.clscode[0x7] = amqp.protocol_0_10.cls['exchange'];

// work with queues
var cls_queue = {
    _defaults: {
        parsed_data: {},
        assembly: null
    },
    msg: {},
    msgcode: {},
    struct: {},
    structcode: {},
    code: 0x8,
    name: 'queue',
    _init: function(options) {
        this._options = options;
        if (typeof(this._options.parsed_data) == 'undefined')
            this._options.parsed_data = {}
    },
    get_name: function() {
        return this.name;
    },
    get_message_name: function() {
        var cc = this.message_code;
        return this.msgcode[cc].name;
    },
    get: function (key) {
        return this._options.parsed_data[key];
    },

    set: function (key, value) {
        this._options.parsed_data[key] = value;
    },

    decode: function(code) {
        this.message_code = code;
        var results = this.msgcode[code].decode(this._options.assembly);
        for (key in results) {
            this.set(key, results[key]);
        }
    },

    encode: function(code) {
        this.msgcode[code].encode(assembly, this._options.parsed_data);
    },
};
 
cls_queue.msg['declare'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x1,
    cls: cls_queue,
    name: 'declare',
    cls_name: 'queue',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_queue.msgcode[0x1] = cls_queue.msg['declare'];

// None
cls_queue.msg['declare'].fields.push(['queue', _module.type.str8, true, 1]);


// exchange name for messages with exceptions
cls_queue.msg['declare'].fields.push(['alternate_exchange', _module.type.str8, false, 2]);


// do not create queue
cls_queue.msg['declare'].fields.push(['passive', _module.type.bit, false, 4]);


// request a durable queue
cls_queue.msg['declare'].fields.push(['durable', _module.type.bit, false, 8]);


// request an exclusive queue
cls_queue.msg['declare'].fields.push(['exclusive', _module.type.bit, false, 16]);


// auto-delete queue when unused
cls_queue.msg['declare'].fields.push(['auto_delete', _module.type.bit, false, 32]);


// arguments for declaration
cls_queue.msg['declare'].fields.push(['arguments', _module.type.map, false, 64]);


cls_queue.msg['delete'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x2,
    cls: cls_queue,
    name: 'delete',
    cls_name: 'queue',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_queue.msgcode[0x2] = cls_queue.msg['delete'];

// None
cls_queue.msg['delete'].fields.push(['queue', _module.type.str8, true, 1]);


// delete only if unused
cls_queue.msg['delete'].fields.push(['if_unused', _module.type.bit, false, 2]);


// delete only if empty
cls_queue.msg['delete'].fields.push(['if_empty', _module.type.bit, false, 4]);


cls_queue.msg['purge'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x3,
    cls: cls_queue,
    name: 'purge',
    cls_name: 'queue',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_queue.msgcode[0x3] = cls_queue.msg['purge'];

// None
cls_queue.msg['purge'].fields.push(['queue', _module.type.str8, true, 1]);


cls_queue.msg['query'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x4,
    cls: cls_queue,
    name: 'query',
    cls_name: 'queue',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_queue.msgcode[0x4] = cls_queue.msg['query'];

// the queried queue
cls_queue.msg['query'].fields.push(['queue', _module.type.str8, true, 1]);


cls_queue.struct['QUEUE_QUERY_RESULT'] = 0x1;
cls_queue.struct['queue_query_result'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_queue.struct['queue_query_result'].prototype = {
    name: 'queue_query_result',
    code: 0x1,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.queue,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_queue.structcode[0x1] = cls_queue.struct['queue_query_result'];
 
// None
cls_queue.struct['queue_query_result'].prototype.fields.push(['queue', _module.type.str8, true, 1]);


// None
cls_queue.struct['queue_query_result'].prototype.fields.push(['alternate_exchange', _module.type.str8, false, 2]);


// None
cls_queue.struct['queue_query_result'].prototype.fields.push(['durable', _module.type.bit, false, 4]);


// None
cls_queue.struct['queue_query_result'].prototype.fields.push(['exclusive', _module.type.bit, false, 8]);


// None
cls_queue.struct['queue_query_result'].prototype.fields.push(['auto_delete', _module.type.bit, false, 16]);


// None
cls_queue.struct['queue_query_result'].prototype.fields.push(['arguments', _module.type.map, false, 32]);


// number of messages in queue
cls_queue.struct['queue_query_result'].prototype.fields.push(['message_count', _module.type.uint32, true, 64]);


// number of subscribers
cls_queue.struct['queue_query_result'].prototype.fields.push(['subscriber_count', _module.type.uint32, true, 128]);


amqp.protocol_0_10.cls['queue'] = amqp.protocol.MetaClass(cls_queue);
amqp.protocol_0_10.clscode[0x8] = amqp.protocol_0_10.cls['queue'];

// work with file content
var cls_file = {
    _defaults: {
        parsed_data: {},
        assembly: null
    },
    msg: {},
    msgcode: {},
    struct: {},
    structcode: {},
    code: 0x9,
    name: 'file',
    _init: function(options) {
        this._options = options;
        if (typeof(this._options.parsed_data) == 'undefined')
            this._options.parsed_data = {}
    },
    get_name: function() {
        return this.name;
    },
    get_message_name: function() {
        var cc = this.message_code;
        return this.msgcode[cc].name;
    },
    get: function (key) {
        return this._options.parsed_data[key];
    },

    set: function (key, value) {
        this._options.parsed_data[key] = value;
    },

    decode: function(code) {
        this.message_code = code;
        var results = this.msgcode[code].decode(this._options.assembly);
        for (key in results) {
            this.set(key, results[key]);
        }
    },

    encode: function(code) {
        this.msgcode[code].encode(assembly, this._options.parsed_data);
    },
};
 
cls_file.struct['FILE_PROPERTIES'] = 0x1;
cls_file.struct['file_properties'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_file.struct['file_properties'].prototype = {
    name: 'file_properties',
    code: 0x1,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.file,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_file.structcode[0x1] = cls_file.struct['file_properties'];
 
// MIME content type
cls_file.struct['file_properties'].prototype.fields.push(['content_type', _module.type.str8, false, 1]);


// MIME content encoding
cls_file.struct['file_properties'].prototype.fields.push(['content_encoding', _module.type.str8, false, 2]);


// message header field table
cls_file.struct['file_properties'].prototype.fields.push(['headers', _module.type.map, false, 4]);


// message priority, 0 to 9
cls_file.struct['file_properties'].prototype.fields.push(['priority', _module.type.uint8, false, 8]);


// destination to reply to
cls_file.struct['file_properties'].prototype.fields.push(['reply_to', _module.type.str8, false, 16]);


// application message identifier
cls_file.struct['file_properties'].prototype.fields.push(['message_id', _module.type.str8, false, 32]);


// message filename
cls_file.struct['file_properties'].prototype.fields.push(['filename', _module.type.str8, false, 64]);


// message timestamp
cls_file.struct['file_properties'].prototype.fields.push(['timestamp', _module.type.datetime, false, 128]);


// intra-cluster routing identifier
cls_file.struct['file_properties'].prototype.fields.push(['cluster_id', _module.type.str8, false, 256]);


cls_file.msg['qos'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x1,
    cls: cls_file,
    name: 'qos',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0x1] = cls_file.msg['qos'];

// pre-fetch window in octets
cls_file.msg['qos'].fields.push(['prefetch_size', _module.type.uint32, false, 1]);


// pre-fetch window in messages
cls_file.msg['qos'].fields.push(['prefetch_count', _module.type.uint16, false, 2]);


// apply to entire connection
cls_file.msg['qos'].fields.push(['global', _module.type.bit, false, 4]);


cls_file.msg['qos_ok'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x2,
    cls: cls_file,
    name: 'qos_ok',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0x2] = cls_file.msg['qos_ok'];

cls_file.msg['consume'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x3,
    cls: cls_file,
    name: 'consume',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0x3] = cls_file.msg['consume'];

// None
cls_file.msg['consume'].fields.push(['queue', _module.type.str8, false, 1]);


// None
cls_file.msg['consume'].fields.push(['consumer_tag', _module.type.str8, false, 2]);


// None
cls_file.msg['consume'].fields.push(['no_local', _module.type.bit, false, 4]);


// no acknowledgement needed
cls_file.msg['consume'].fields.push(['no_ack', _module.type.bit, false, 8]);


// request exclusive access
cls_file.msg['consume'].fields.push(['exclusive', _module.type.bit, false, 16]);


// do not send a reply command
cls_file.msg['consume'].fields.push(['nowait', _module.type.bit, false, 32]);


// arguments for consuming
cls_file.msg['consume'].fields.push(['arguments', _module.type.map, false, 64]);


cls_file.msg['consume_ok'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x4,
    cls: cls_file,
    name: 'consume_ok',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0x4] = cls_file.msg['consume_ok'];

// None
cls_file.msg['consume_ok'].fields.push(['consumer_tag', _module.type.str8, false, 1]);


cls_file.msg['cancel'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x5,
    cls: cls_file,
    name: 'cancel',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0x5] = cls_file.msg['cancel'];

// None
cls_file.msg['cancel'].fields.push(['consumer_tag', _module.type.str8, false, 1]);


cls_file.msg['open'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x6,
    cls: cls_file,
    name: 'open',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0x6] = cls_file.msg['open'];

// staging identifier
cls_file.msg['open'].fields.push(['identifier', _module.type.str8, false, 1]);


// message content size
cls_file.msg['open'].fields.push(['content_size', _module.type.uint64, false, 2]);


cls_file.msg['open_ok'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x7,
    cls: cls_file,
    name: 'open_ok',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0x7] = cls_file.msg['open_ok'];

// already staged amount
cls_file.msg['open_ok'].fields.push(['staged_size', _module.type.uint64, false, 1]);


cls_file.msg['stage'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x8,
    cls: cls_file,
    name: 'stage',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0x8] = cls_file.msg['stage'];

cls_file.msg['publish'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x9,
    cls: cls_file,
    name: 'publish',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0x9] = cls_file.msg['publish'];

// None
cls_file.msg['publish'].fields.push(['exchange', _module.type.str8, false, 1]);


// Message routing key
cls_file.msg['publish'].fields.push(['routing_key', _module.type.str8, false, 2]);


// indicate mandatory routing
cls_file.msg['publish'].fields.push(['mandatory', _module.type.bit, false, 4]);


// request immediate delivery
cls_file.msg['publish'].fields.push(['immediate', _module.type.bit, false, 8]);


// staging identifier
cls_file.msg['publish'].fields.push(['identifier', _module.type.str8, false, 16]);


cls_file.msg['return'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0xa,
    cls: cls_file,
    name: 'return',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0xa] = cls_file.msg['return'];

// None
cls_file.msg['return'].fields.push(['reply_code', _module.type.uint16, false, 1]);


// The localized reply text.
cls_file.msg['return'].fields.push(['reply_text', _module.type.str8, false, 2]);


// None
cls_file.msg['return'].fields.push(['exchange', _module.type.str8, false, 4]);


// Message routing key
cls_file.msg['return'].fields.push(['routing_key', _module.type.str8, false, 8]);


cls_file.msg['deliver'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0xb,
    cls: cls_file,
    name: 'deliver',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0xb] = cls_file.msg['deliver'];

// None
cls_file.msg['deliver'].fields.push(['consumer_tag', _module.type.str8, false, 1]);


// None
cls_file.msg['deliver'].fields.push(['delivery_tag', _module.type.uint64, false, 2]);


// Indicate possible duplicate delivery
cls_file.msg['deliver'].fields.push(['redelivered', _module.type.bit, false, 4]);


// None
cls_file.msg['deliver'].fields.push(['exchange', _module.type.str8, false, 8]);


// Message routing key
cls_file.msg['deliver'].fields.push(['routing_key', _module.type.str8, false, 16]);


// staging identifier
cls_file.msg['deliver'].fields.push(['identifier', _module.type.str8, false, 32]);


cls_file.msg['ack'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0xc,
    cls: cls_file,
    name: 'ack',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0xc] = cls_file.msg['ack'];

// None
cls_file.msg['ack'].fields.push(['delivery_tag', _module.type.uint64, false, 1]);


// acknowledge multiple messages
cls_file.msg['ack'].fields.push(['multiple', _module.type.bit, false, 2]);


cls_file.msg['reject'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0xd,
    cls: cls_file,
    name: 'reject',
    cls_name: 'file',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_file.msgcode[0xd] = cls_file.msg['reject'];

// None
cls_file.msg['reject'].fields.push(['delivery_tag', _module.type.uint64, false, 1]);


// requeue the message
cls_file.msg['reject'].fields.push(['requeue', _module.type.bit, false, 2]);


amqp.protocol_0_10.cls['file'] = amqp.protocol.MetaClass(cls_file);
amqp.protocol_0_10.clscode[0x9] = amqp.protocol_0_10.cls['file'];

// work with streaming content
var cls_stream = {
    _defaults: {
        parsed_data: {},
        assembly: null
    },
    msg: {},
    msgcode: {},
    struct: {},
    structcode: {},
    code: 0xa,
    name: 'stream',
    _init: function(options) {
        this._options = options;
        if (typeof(this._options.parsed_data) == 'undefined')
            this._options.parsed_data = {}
    },
    get_name: function() {
        return this.name;
    },
    get_message_name: function() {
        var cc = this.message_code;
        return this.msgcode[cc].name;
    },
    get: function (key) {
        return this._options.parsed_data[key];
    },

    set: function (key, value) {
        this._options.parsed_data[key] = value;
    },

    decode: function(code) {
        this.message_code = code;
        var results = this.msgcode[code].decode(this._options.assembly);
        for (key in results) {
            this.set(key, results[key]);
        }
    },

    encode: function(code) {
        this.msgcode[code].encode(assembly, this._options.parsed_data);
    },
};
 
cls_stream.struct['STREAM_PROPERTIES'] = 0x1;
cls_stream.struct['stream_properties'] = function(value, encode_type) {
    if (typeof(encode_type) == 'undefined')
        encode_type = true;

    this._value = value;
    this._encode_type = encode_type;
}
cls_stream.struct['stream_properties'].prototype = {
    name: 'stream_properties',
    code: 0x1,
    pack_size: 2,
    size: 4,
    cls: amqp.protocol_0_10.cls.stream,
    fields: [],
    is_struct: true,
    decode: function(assembly) {
        var result = {};
        // read size octet for session.header packing flags
        var pack_size = this.pack_size;
        var packing_flags = 0;
        for (var i=0; i < pack_size; i++)
            packing_flags += new amqp.protocol_0_10.type.int8().decode(assembly) << (i*8);

        for (i in this.fields) {
            if (packing_flags & this.fields[i][3]) {
                var name = this.fields[i][0];
                var type_class = this.fields[i][1];
                var type = new type_class();
                var size = 0;
                
                // if this is a struct we need to get the encoded size of the 
                // struct first
                if (type.is_struct)
                    size = amqp.protocol.decode_int(assembly, type.size);
                
                result[name] = type.decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {
        if(typeof(values) == 'undefined')
            values = this._value;

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = '';
        if(this._encode_type)
            header += String.fromCharCode(this.cls.code, this.code)

        var pf = amqp.protocol.int_to_bytestr(packing_flags, this.pack_size);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
};
cls_stream.structcode[0x1] = cls_stream.struct['stream_properties'];
 
// MIME content type
cls_stream.struct['stream_properties'].prototype.fields.push(['content_type', _module.type.str8, false, 1]);


// MIME content encoding
cls_stream.struct['stream_properties'].prototype.fields.push(['content_encoding', _module.type.str8, false, 2]);


// message header field table
cls_stream.struct['stream_properties'].prototype.fields.push(['headers', _module.type.map, false, 4]);


// message priority, 0 to 9
cls_stream.struct['stream_properties'].prototype.fields.push(['priority', _module.type.uint8, false, 8]);


// message timestamp
cls_stream.struct['stream_properties'].prototype.fields.push(['timestamp', _module.type.datetime, false, 16]);


cls_stream.msg['qos'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x1,
    cls: cls_stream,
    name: 'qos',
    cls_name: 'stream',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_stream.msgcode[0x1] = cls_stream.msg['qos'];

// pre-fetch window in octets
cls_stream.msg['qos'].fields.push(['prefetch_size', _module.type.uint32, false, 1]);


// pre-fetch window in messages
cls_stream.msg['qos'].fields.push(['prefetch_count', _module.type.uint16, false, 2]);


// transfer rate in octets/second
cls_stream.msg['qos'].fields.push(['consume_rate', _module.type.uint32, false, 4]);


// apply to entire connection
cls_stream.msg['qos'].fields.push(['global', _module.type.bit, false, 8]);


cls_stream.msg['qos_ok'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x2,
    cls: cls_stream,
    name: 'qos_ok',
    cls_name: 'stream',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_stream.msgcode[0x2] = cls_stream.msg['qos_ok'];

cls_stream.msg['consume'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x3,
    cls: cls_stream,
    name: 'consume',
    cls_name: 'stream',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_stream.msgcode[0x3] = cls_stream.msg['consume'];

// None
cls_stream.msg['consume'].fields.push(['queue', _module.type.str8, false, 1]);


// None
cls_stream.msg['consume'].fields.push(['consumer_tag', _module.type.str8, false, 2]);


// None
cls_stream.msg['consume'].fields.push(['no_local', _module.type.bit, false, 4]);


// request exclusive access
cls_stream.msg['consume'].fields.push(['exclusive', _module.type.bit, false, 8]);


// do not send a reply command
cls_stream.msg['consume'].fields.push(['nowait', _module.type.bit, false, 16]);


// arguments for consuming
cls_stream.msg['consume'].fields.push(['arguments', _module.type.map, false, 32]);


cls_stream.msg['consume_ok'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x4,
    cls: cls_stream,
    name: 'consume_ok',
    cls_name: 'stream',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_stream.msgcode[0x4] = cls_stream.msg['consume_ok'];

// None
cls_stream.msg['consume_ok'].fields.push(['consumer_tag', _module.type.str8, false, 1]);


cls_stream.msg['cancel'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x5,
    cls: cls_stream,
    name: 'cancel',
    cls_name: 'stream',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_stream.msgcode[0x5] = cls_stream.msg['cancel'];

// None
cls_stream.msg['cancel'].fields.push(['consumer_tag', _module.type.str8, false, 1]);


cls_stream.msg['publish'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x6,
    cls: cls_stream,
    name: 'publish',
    cls_name: 'stream',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_stream.msgcode[0x6] = cls_stream.msg['publish'];

// None
cls_stream.msg['publish'].fields.push(['exchange', _module.type.str8, false, 1]);


// Message routing key
cls_stream.msg['publish'].fields.push(['routing_key', _module.type.str8, false, 2]);


// indicate mandatory routing
cls_stream.msg['publish'].fields.push(['mandatory', _module.type.bit, false, 4]);


// request immediate delivery
cls_stream.msg['publish'].fields.push(['immediate', _module.type.bit, false, 8]);


cls_stream.msg['return'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x7,
    cls: cls_stream,
    name: 'return',
    cls_name: 'stream',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_stream.msgcode[0x7] = cls_stream.msg['return'];

// None
cls_stream.msg['return'].fields.push(['reply_code', _module.type.uint16, false, 1]);


// The localized reply text.
cls_stream.msg['return'].fields.push(['reply_text', _module.type.str8, false, 2]);


// None
cls_stream.msg['return'].fields.push(['exchange', _module.type.str8, false, 4]);


// Message routing key
cls_stream.msg['return'].fields.push(['routing_key', _module.type.str8, false, 8]);


cls_stream.msg['deliver'] = {
    masks: [1, 2, 4, 8, 16, 32, 64, 128],
    fields: [],
    code: 0x8,
    cls: cls_stream,
    name: 'deliver',
    cls_name: 'stream',
    type: 1,
    decode: function(assembly) {
        var result = {};
        // read one octet for session.header packing flags
        var session_packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        // if present read the next byte
        // TODO: read the actual struct which is not needed right now since
        //       we only respond to controls for now
        if (session_packing_flags)
            session_struct = new amqp.protocol_0_10.type.int8().decode(assembly);

        var packing_flags = new amqp.protocol_0_10.type.int8().decode(assembly);
        var packing_flags2 = new amqp.protocol_0_10.type.int8().decode(assembly) << 8;
        packing_flags += packing_flags2;

        for (i in this.fields) {
            if (packing_flags & this.masks[i]) {
                var name = this.fields[i][0];
                var type = this.fields[i][1];
                result[name] = new type().decode(assembly);
            }
        }

        return result;
    },
    encode: function(assembly, values) {

        var packing_flags = 0;
        for (var i in this.fields) {
            var name = this.fields[i][0];
            var type = this.fields[i][1];
            var v = values[name];

            if (typeof(v) != 'undefined') {
                // special case bits
                if(type == _module.type.bit) {
                    if (v)
                        packing_flags += (1 << i);
                } else {
                    packing_flags += (1 << i);
                    new type(v, false).encode(assembly);
                }
            }
        }

        var header = String.fromCharCode(this.cls.code, this.code)
        // FIXME: session headers are version dependent so we should
        //        do this in a generate_session_header method
        if (values['sync']) {
            // request sync call
            var sync_flags = amqp.protocol.int_to_bytestr(0x01,1);
            // add twice since both packing flags and values = 1
            header += sync_flags;
            header += sync_flags;
        } else {
            // only add packing flag = 0
            var sync_flags = amqp.protocol.int_to_bytestr(0x00,1);
            header += sync_flags;
            header += sync_flags;
        }
        var pf = amqp.protocol.int_to_bytestr(packing_flags, 2);
        for (var i=pf.length - 1; i >= 0; i--)
            header += pf[i];

        assembly.prepend(header);

    }
}

cls_stream.msgcode[0x8] = cls_stream.msg['deliver'];

// None
cls_stream.msg['deliver'].fields.push(['consumer_tag', _module.type.str8, false, 1]);


// None
cls_stream.msg['deliver'].fields.push(['delivery_tag', _module.type.uint64, false, 2]);


// None
cls_stream.msg['deliver'].fields.push(['exchange', _module.type.str8, false, 4]);


// None
cls_stream.msg['deliver'].fields.push(['queue', _module.type.str8, true, 8]);


amqp.protocol_0_10.cls['stream'] = amqp.protocol.MetaClass(cls_stream);
amqp.protocol_0_10.clscode[0xa] = amqp.protocol_0_10.cls['stream'];

amqp.protocol.register('0.10', amqp.protocol_0_10);
})();