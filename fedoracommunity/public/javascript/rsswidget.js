var ie_nocache = 1;

create_xhr = function() {
  return window.ActiveXObject ?
                new ActiveXObject("Microsoft.XMLHTTP") :
                new XMLHttpRequest();
}

widget_connect = function(username, feed, callback) {
  Orbited.connect(callback, 'bobvila', "/feed/" + feed, "0");
  var xhr = create_xhr();
  xhr.open("GET", "/join?feed=" + feed, true);
  xhr.send(null);
}
