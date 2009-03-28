function update_action(update, action) {
    args = {}
    args['update'] = update;
    args['action'] = action;

    if (typeof(moksha_csrf_token)!='undefined' && moksha_csrf_token) {
        args['_csrf_token'] = moksha_csrf_token;
    }

    $.getJSON('/moksha_connector/bodhi/request_data/request', args, function(json) {
        json = json[1];
        $('#flash').text('');
        $('div.left-content-column').prepend($('<span/>').attr('id', 'flash').text(json.tg_flash)).show('slow');
        if (typeof(json.update) != 'undefined' && json.update.request == action) {
            $('#' + update.replace(/\./g, '') + '_' + action).hide('slow');
        }
    });

}
