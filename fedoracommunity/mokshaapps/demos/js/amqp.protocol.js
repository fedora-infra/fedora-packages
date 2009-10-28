(function(){

// noop console if it doesn't exist
if (typeof(console) == 'undefined') {
    console = {log:function() {return;}};
}

/******************************************************************
 * Class metaclass
 * Simplifys creating classes
 *
 * args:
 *    cls_members - a dictionary of class variables and methods
 *
 * returns - a constructor function which calls this._init
 *           when constucted with the 'new' keyword
 ******************************************************************/

var deep_copy_defaults = function(o) {
    var results = null;
    if (o != null && typeof(o) == 'object') {
        if (o instanceof Array) {
            results = [];
            for(var i=0; i<o.length; i++)
                results.push(deep_copy_defaults(o[i]));
        } else {
            results = {}
            for(var prop in o) {
                results[prop] = deep_copy_defaults(o[prop]);
            }
        }
    } else {
        results = o;
    }

    return results;
}
var MetaClass = function (cls_members) {
    // create the class
    var self = function(options) {
        // we call the _init constructor when the object is created
        var complete_options = deep_copy_defaults(this._defaults);
        for (var o in options) {
             if (typeof(complete_options[o]) != 'undefined')
                complete_options[o] = options[o];
        }

        this._init.call(this, complete_options);
    }

    // default to a noop for the constructor
    self._init = function() {};
    self._new = function() {};

    // add class members to the prototype
    for (var m in cls_members)
        self.prototype[m] = cls_members[m];

    // call the _new constructor when a class is first created
    self._new.call(self);

    return self;
}

var extend = function(module, ext) {
    for (var key in ext) {
        module[key] = ext[key]
    }
}

// predefine amqp
amqp = {protocol:null};

// classes
amqp.protocol = {
    default_version: '0.10',
    protocols: {},
    MetaClass: MetaClass,
    extend: extend,
    register: function(version, module) {
        if (this.protocols[version])
            throw "Version " + version + " of the AMQP bindings has already been registered.  Duplicate registration!!!";

        this.protocols[version] = module;

        var def_ver_check = this.default_version.split('.');
        var ver_check = version.split('.');

        for (var i=0; i < ver_check.length; i++) {
            if (ver_check[i] > def_ver_check[i]) {
                default_version = version;
                return;
            }
        }
    },

    get_connection: function(version, options) {
        if (!version)
            version = this.default_version;

        var module = this.protocols[version];
        if (!module)
            throw ("Version " + version + " of the AMQP protocol was requested but has not yet been registered");

        options['_module'] = module;
        return new module.Connection(options);
    },

    Assembly:MetaClass({
        _defaults: {
            data: '',
        },

        _init: function(options) {
            // in bytes
            this._seek_pos = 0;
            this._bit_offset = 0;
            this._options = options;
            this._start_marker = 0;
        },

        read_bit: function(count) {
            var final_offset = this._bit_offset + count;
            if (final_offset > 8)
                throw RangeError("You tried to read beyond the byte boundry.  This is not allowed.  You may only read inside a single byte when reading individual bits");

            var c = this._options.data.charCodeAt(this._seek_pos);
            var mask = 1;
            for (var i = 1; i < count; i++)
                mask = (mask << 1) + 1;

            mask = mask << (7 - this._bit_offset);
            var c_offset = c & mask;
            var results = c_offset >> (8 - (count + this._bit_offset));

            if (final_offset == 8) {
                this._seek_pos++;
                this._bit_offset = 0;
            } else {
                this._bit_offset = final_offset;
            }

            return results;
        },

        read_byte: function(count) {
            if (this._bit_offset)
                throw RangeError("You tried to read a non-aligned byte.  This is not allowed.  This happens if you had previously called bit read and did not end your reads on a byte boundry!");

            var results = this._options.data.substr(this._seek_pos, count);
            this._seek_pos += count;

            return results;
        },

        write: function(bytes) {
            if (!this._options.data)
                this._options.data = bytes;
            else
                this._options.data += bytes;
        },

        prepend: function(bytes) {
            this._options.data = bytes + this._options.data;
        },

        get_data: function() {
            return this._options.data;
        },

        get_size: function(from_current_pos) {
            var length = this._options.data.length;
            if (from_current_pos)
                return length - this._seek_pos;
            else
                return length;
        },

        seek: function(pos) {
            this._seek_pos = pos;
            this._bit_offset = 0;
        },

        eof: function() {
            if (this._options.data.length == this._seek_pos)
                return true;
        },

        /* Debug metadata */
        mark_start: function() {
            this._start_marker = this._seek_pos;
        },

        get_start_pos: function() {
            return this._start_marker;
        },

        get_pos: function() {
            return this._seek_pos;
        }
    }),

    Message: MetaClass({
        _defaults: {
            parsed_data: {},
            template: null
        },

        _init: function(options) {
            this._options = options;
            if (typeof(this._options.parsed_data) == 'undefined')
                this._options.parsed_data = {}

            this._options.assembly = new amqp.protocol.Assembly();
        },

        get: function (key) {
            return this._options.parsed_data[key];
        },

        set: function (key, value) {
            this._options.parsed_data[key] = value;
        },

        get_size: function() {
            return this._options.assembly.get_size(true);
        },

        get_data: function(size) {
            return this._options.assembly.read_byte(size);
        },

        get_type: function() {
            return this._options.template.type;
        },

        get_name: function() {
            return this._options.template.cls_name;
        },

        get_message_name: function() {
            return this._options.template.name;
        },

        decode: function() {
            var results = this._options.template.decode(this._options.assembly);
            for (key in results) {
                this.set(key, results[key]);
            }
        },

        encode: function() {
            var o = this._options;
            o.template.encode(o.assembly, o.parsed_data);
        },


    }),
}

// decoders and encoders
extend(amqp.protocol, {
    int_to_bytestr: function(u, size) {
        var results = '';
        var u_shifted = u;
        var mask = 255;
        for (var i=0; i < size; i++) {
            // shift and mask bits in network order
            var u_mask = u_shifted & mask;
            results = String.fromCharCode(u_mask) + results;

            u_shifted = u_shifted >> 8;
        }

        return results;
    },

    decode_typecode: function(assembly) {
        return amqp.protocol.decode_uint(assembly, 1);
    },

    encode_typecode: function(assembly, typecode) {
        if (typecode != null) {
            var b = amqp.protocol.int_to_bytestr(typecode, 1);
            assembly.write(b);
        }
    },

    decode_bin: function(assembly, size) {
        return (assembly.read_byte(size));
    },

    encode_bin: function(assembly, typecode, size, value) {
        amqp.protocol.encode_typecode(assembly, typecode);
        assembly.write(value)
    },

    decode_int: function(assembly, size) {
        var stream = assembly.read_byte(size);
        var first_byte = stream.charCodeAt(0);
        var sign_mask = 128;
        var num_mask = 127;
        var sign = first_byte & sign_mask;
        first_byte = first_byte & num_mask;
        if(sign)
            first_byte = ~first_byte

        first_byte = first_byte << (size - 1);

        var result = first_byte;
        for (var i = 0; i < size-1; i++) {
            var byte_pos = size - (i + 1);
            var byte = stream.charCodeAt(byte_pos);
            if (sign)
                byte = ~byte;
            result += byte << i;
        }

        if (sign)
            result = (result + 1) * -1;

        return result;

    },

    encode_int: function(assembly, typecode, size, value) {
        amqp.protocol.encode_typecode(assembly, typecode);
        var byte_value = amqp.protocol.int_to_bytestr(value, size);
        assembly.write(byte_value);
    },

    decode_uint: function(assembly, size) {
        var stream = assembly.read_byte(size);

        var result = 0;
        for (var i = 0; i < size; i++) {
            var byte_pos = size - (i + 1);
            result += stream.charCodeAt(byte_pos) << i;
        }

        return result;
    },

    encode_uint: function(assembly, typecode, size, value) {
        // should be the same as encoding an int unless
        // we have to deal with endieness on different archs
        // I'll have to check that
        amqp.protocol.encode_int(assembly, typecode, size, value);

    },

    decode_void: function(assembly, size) {
        if (size != 0)
            throw "Error while decoding a void type.  Expecting size = 0 but got size = " + size;

        return null;
    },

    encode_void: function(assembly, typecode, size, value) {
        if (size != 0)
            throw "Error while encoding a void type.  Size must be 0";

        amqp.protocol.encode_typecode(assembly, typecode);
    },

    decode_bool: function(assembly, size) {
        var value = amqp.protocol.decode_uint(assembly, size);
        if (value)
            return true;
        else
            return false;
    },

    encode_bool: function(assembly, typecode, size, value) {
        if (value)
            amqp.protocol.encode_uint(assembly, typecode, size, 1);
        else
            amqp.protocol.encode_uint(assembly, typecode, size, 0);
    },

    decode_dec: function(assembly, size) {
        var dec = amqp.protocol.decode_uint(assembly, 1);
        var num = amqp.protocol.decode_int(assembly, size - 1);
        var result = num / (dec * 10);

        return result;
    },

    encode_dec: function(assembly, typecode, size, value) {
        // FIXME: We might need a new class to represent this type
        throw "Not implemented yet!!!"
        
    },

    decode_datetime: function(assembly, size) {
        var epoc = amqp.protocol.decode_uint(assembly, size);
        var datetime = new Date();
        datetime.setTime(epoc);

        return datetime;
    },

    encode_datetime: function(assembly, typecode, size, value) {
        if (value.getTime)
            value = value.getTime();

        amqp.protocol.encode_uint(assembly, typecode, size, value);
    },

    decode_float: function(assembly, size) {
        var dec = amqp.protocol.decode_uint(assembly, 1);
        var num = amqp.protocol.decode_int(assembly, size - 1);
        var result = num / (dec * 10);

        return result;
    },

    encode_float: function(assembly, typecode, size, value) {
        throw "Not implemented yet!!!"
    },

    encode_bit: function(assembly, typecode, size, value) {
        // no-op since bits are special cases which use
        // the packing flags for values
        // special cased in the versioned protocol code
    },

    decode_bit: function(assembly, size) {
        // since bits are special cases which use
        // the packing flags for values if this is called
        // it means the bit was set so return 1

        return 1;
    },

    /************** variable types *******************/

    decode_map: function(assembly, varsize) {
        var result = {};
        var size = amqp.protocol.decode_uint(assembly, varsize);
        var count = amqp.protocol.decode_uint(assembly, 4);

        for(var i=0; i < count; i++) {
            var key = amqp.protocol.decode_str(assembly, 1);
            var typecode = amqp.protocol.decode_uint(assembly, 1);
            var type = this.get_type(typecode);
            var value = new type().decode(assembly);
            result[key] = value;
        }

        return result;
    },

    encode_map: function(assembly, typecode, size, value) {
        var map_assembly = new amqp.protocol.Assembly();
        var count = 0;
        var map_size = 1;

        amqp.protocol.encode_typecode(assembly, typecode);
        // encode each key/value pair, guessing at the value type
        // if not implicitly specified
        for(var k in value) {
            count++;

            var v = value[k];
            var type = this.guess_type(v);
            amqp.protocol.encode_str(map_assembly, null, 1, k);
            type.encode(map_assembly);
        }

        map_size += map_assembly.get_size();

        assembly.write(amqp.protocol.int_to_bytestr(map_size, 4));
        assembly.write(amqp.protocol.int_to_bytestr(count, 4));
        assembly.write(map_assembly.get_data());
    },

    decode_array: function(assembly, varsize) {
        var result = [];
        var size = amqp.protocol.decode_uint(assembly, varsize);
        var typecode = amqp.protocol.decode_uint(assembly, 1);
        var type = this.get_type(typecode);
        var count = amqp.protocol.decode_uint(assembly, 4);

        for(var i=0; i < count; i++) {
            var value = new type().decode(assembly);
            result.push(value)
        }

        return result;
    },

    encode_array: function(assembly, typecode, size, value) {
        throw "Not implemented yet!!!"
    },

    decode_str: function(assembly, varsize) {
        var result = '';
        var size = amqp.protocol.decode_uint(assembly, varsize);
        var result = amqp.protocol.decode_bin(assembly, size);

        return result;
    },

    encode_str: function(assembly, typecode, size, value) {
        var var_size = value.length;
        amqp.protocol.encode_typecode(assembly, typecode);
        assembly.write(amqp.protocol.int_to_bytestr(var_size, size));
        assembly.write(value);
    },

    decode_seq_set: function(assembly, varsize) {
        var results = [];
        var size = amqp.protocol.decode_uint(assembly, varsize);
        const mask = 0x0f;
        for (var i=0; i<size; i++) {
            var seq = amqp.protocol.decode_uint(assembly, 1);
            var lower = seq >> 4;
            var upper = seq & mask;
            results.push([lower, upper]);
        }

        return results;
    },

    encode_seq_set: function(assembly, typecode, size, value) {
        throw "Not implemented yet!!!"
    },

    /******************* higher level constructs **************************/

    encode_header: function(assembly) {
        var header = this.get_header();
        assembly.write(header);
    },

    decode_header: function(assembly) {
        var header = {}
        header['id'] = this.decode_bin(assembly, 4);
        if (header['id']!='AMQP')
            throw "Malformed AMQP header";

        header['class'] = this.decode_int(assembly, 1);
        header['instance'] = this.decode_int(assembly, 1);
        header['version_major'] = this.decode_int(assembly, 1);
        header['version_minor'] = this.decode_int(assembly, 1);

        return header;
    },
});

})();
