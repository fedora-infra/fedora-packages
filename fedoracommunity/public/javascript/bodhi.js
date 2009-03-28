function update_action(update, action) {
    args = {}
    args['update'] = update;
    args['action'] = action;

    if (typeof(moksha_csrf_token)!='undefined' && moksha_csrf_token) {
        args['_csrf_token'] = moksha_csrf_token;
    }

    $.getJSON('/moksha_connector/bodhi/request_data/request', args, function(json) {
        console.log(json);
        $('span.main_table').prepend($('<span/>').text(json['tg_flash']));
        if (json['update']['request'] == action) {
            console.log('Request successful');
            $(update + '_' + action).hide();
        }
    });

}
