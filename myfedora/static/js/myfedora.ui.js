var _mf_current_hover_menu = "";

function mf_menu_hover_start(menu_name)
{
    var div;

    if (_mf_current_hover_menu)
      return;

    _mf_current_hover_menu = "#" + menu_name;
    div = $(_mf_current_hover_menu);

    div.fadeIn('fast');   
}

function _mf_menu_hover_fadeout(menu_name)
{
    if (_mf_current_hover_menu != menu_name)
      $(menu_name).fadeOut('fast');
}

function mf_menu_hover_stop()
{
    setTimeout("_mf_menu_hover_fadeout('" + _mf_current_hover_menu + "')", 50);
    _mf_current_hover_menu = "";
}

function mf_replace_block_async(block_name, url, user_callback, user_data)
{
    $.getJSON(url + "&tg_format=json", 
      function (data) 
          {
            var html = user_callback(data, user_data);
            var div = $("#" + block_name);
            
            div.html(html);
          } 
    ); 
    
}
