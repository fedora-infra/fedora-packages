<html>
<head><title>Orbited Test</title></head>
<body>
<h1>This is a test page to test Orbited with AMQP through a direct socket</h1>

<ul id="message_list" style="line-height: 2em;">

</ul>
<script>
Orbited.settings.port = 443;
Orbited.settings.hostname = 'admin.stg.fedoraproject.org/orbited';
settings = {};
settings.DEBUG_LEVEL = 1;
settings.amqp_broker_port = 5672;
settings.amqp_broker_host = 'admin.stg.fedoraproject.org';
settings.remote_queue = 'org.fedoraproject';
settings.bind_to = [['amq.topic', 'org.fedoraproject.#'],
                    ['amq.topic', 'control']];

var DEBUG_LEVEL = settings.DEBUG_LEVEL;
 
if (typeof(console) == 'undefined')
    console = {'log':function(){}};


function str_to_bytearray(str) {
  var result = [];
  for (i = 0; i < str.length; i++)
    result.push('0x' + str.charCodeAt(i).toString(16));

  return result;

}

var toggle_value_format = function () {
      var $this = $(this);
      var value16 = $this.attr('value16');
      var value2 = $this.attr('value2');
      var value10 = $this.attr('value10');
      if ($this.text() == value16)
         $this.text(value2);
      else if ($this.text() == value2)
         $this.text(value10);
      else
         $this.text(value16);
}
  
$toggle_a_template = $('<a/>').attr('href', 'javascript:void(0)');

function append_msg(label, frame, id) {
  if (!DEBUG_LEVEL)
      return;
  var $li = $('<li />');
  var $link = $('<a />').attr('href', 'javascript:void(0)');
  $li.append($link);
  $li.append('<br />');
  
  var date = new Date()
  var st = frame.get('segment_type');
  var header='';
  if (st==0 || st == 1) {
    var message_class = frame.get('msg');
    header = date.toString() + ' ' + label + ': Class: ' + message_class.get_name() + ' Message: ' + message_class.get_message_name() + '';
  } else if (st == 2) {
    header = date.toString() + ' ' + label + ' Header';
  } else if (st == 3) {
    var body = frame.get('body');
    header = date.toString() + ' ' + label + ' Body: ' + body;
  }

  $link.text(header);  

  $('#' + id).append($li);
  var $bottom = $('#bottom');
  $bottom[0].scrollIntoView(true);
  
  if (DEBUG_LEVEL < 2)
      return;
  
  var $content = $('<div />').addClass('content');
  $content.hide();
  $li.append($content);
  $link.click(function() {
      var $content = $('.content', $(this).parent());
      $content.slideToggle();
      return false;
  });

  var $table = $('<table style="font-family: monospace;"><thead><th>byte dump</th><th>ascii</th></thead><tbody></tbody></table>');
  var $body = $('tbody', $table);
  var col_counter = 0;
  // display
  var $ascii_col;
  var $byte_col;

  var assembly = frame.get_assembly();
  var msg_data = assembly.get_data();
  var start = assembly.get_start_pos();
  var end = msg_data.length;
  if (label == "RECV:")
      end = assembly.get_pos();
  
  for (var i=start; i<end; i++) {
      
      if (col_counter==0) {
        $byte_col = $('<td style="padding-right: 10px"/>');
        $ascii_col = $('<td style="padding-left:10px"/>');
      }
     
      var ascii = $('<span />').text(msg_data[i]);
      var byte = msg_data.charCodeAt(i);
      if (!(byte >= 40 && byte <= 176))
        ascii = '.';

      var byte16 = byte.toString(16);
      if (byte16.length != 2)
        byte16 = '0' + byte16

      byte16 = '0x' + byte16;
      var byte2 = byte.toString(2);
      if (byte2.length != 8) {
          var padding = '';
        for (var j = 0; j < 8 - byte2.length; j++)
          padding += '0';

        byte2 = padding + byte2;
      }

      $byte_span = $('<span/>').addClass('byte_' + (i-start));
      
      if(DEBUG_LEVEL >= 3)
          $byte_a = $toggle_a_template.clone().click(toggle_value_format);
      else
          $byte_a = $('<span/>');
          
      $byte_a.text(byte16);
      
      $byte_a.attr('value10', byte.toString(10));
      $byte_a.attr('value16', byte16);
      $byte_a.attr('value2', byte2);

      $byte_span.append($byte_a).append(' ');
      $byte_col.append($byte_span);
      $ascii_col.append(ascii);
      
      
      col_counter++;
      
      if (col_counter == 8) {
          $byte_col.append('<span>&nbsp;</span>');
          $ascii_col.append('<span>&nbsp;</span>');
      } else if (col_counter == 16) {
          col_counter = 0;
          var $row = $('<tr />');
          $row.append($byte_col).append($ascii_col);
          $body.append($row);
      }
  }
  
  
  if (col_counter != 16) {
      var $row = $('<tr />');
      $row.append($byte_col).append($ascii_col);
      $body.append($row);
    }
  
  
  $content.append($table);
  
}


</script>
<script>
   var num_msgs = 0;
   // Edit this script for testing
   amqp_conn = new amqp.Connection({host:settings.amqp_broker_host,
                                    port:settings.amqp_broker_port,
                                    username: 'guest',
                                    password: 'guest',
                                    send_hook: function(data, frame) {
                                        num_msgs++;
                                        append_msg('SENT', frame, 'message_list');
                                    },
                                    recive_hook: function(data, frame) {
                                        num_msgs++;
                                        append_msg('RECV', frame, 'message_list');
                                    }
                                   });

    amqp_conn.start();
    
    // You should have your server generate a UUID since browser methods
    // are unreliable at best
    session = amqp_conn.create_session('not_a_great_id' + (new Date().getTime() + Math.random()));
    var remote_queue =  settings.remote_queue + session.name;
    session.Queue('declare', {queue: remote_queue});
    
    var queue = session.create_local_queue({name: 'local_queue'});
    
    var output_cb = function(msg) {
        $('#output_content').append(msg.header.delivery_properties.routing_key + ' sent ' + msg.body + '<br />');
    }
 
    for (var i in settings.bind_to) 
        queue.subscribe({exchange: settings.bind_to[i][0],
                         remote_queue:remote_queue,
                         binding_key:settings.bind_to[i][1],
                         callback: output_cb});
    
    queue.start();

</script>
<div id="output" style="float:right; zindex: 2; position:fixed;  bottom: 10px; right: 10px; background-color: #FFFFFF; opacity:0.6; padding: 5px; border-style:solid; border-width: 1px;">
    
    <div id="output_content" style="float:left">
        <strong>Output:</strong><br />
    </div> 
    <div style="float:right"><a href="javascript:void(0);" id="output_hide_button">x</a></div>
</div>
<div id="bottom"></div>
<script type="text/javascript">
$('#output_hide_button').click(function() {
    var o = $(this);
    if (o.text() == 'x') {
        o.text('o');
        $('#output_content').fadeOut();
    } else {
        o.text('x');
        $('#output_content').fadeIn();
    }
});
</script>
</body>

</html>
