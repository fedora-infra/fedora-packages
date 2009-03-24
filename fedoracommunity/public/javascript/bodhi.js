function update_action(update, action) {
    args = {}
    args['update'] = update;
    args['action'] = action;

    if (typeof(moksha_csrf_token)!='undefined' && moksha_csrf_token) {
        args['_csrf_token'] = moksha_csrf_token;
    }

    $.getJSON('/moksha_connector/bodhi/request_data/request', args, function(json) {
        console.log(json);
        // flash json['tg_flash']
        // if json['update']['request'] matches our action,
        //      remove the action link
    });

}
