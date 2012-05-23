
fcomm = {
        connector_load: function(resource, method, params, callback, $overlay_div, loading_icon) {
                var path = moksha.url('/fcomm_connector/' + resource + '/' + method);
                // TODO -- this used to be settable in the configuration
                // (development.ini).  I disabled it since it spanned the
                // moksha/fcomm divide in the Great Migration of February 9,
                // 2012.
                var moksha_profile_connectors = false;
                if (moksha_profile_connectors == true) {
                        var start_time = new Date().getTime();
                        var profile_callback = function(data) {
                                var profile_id = data['moksha_profile_id'];
                                var callback_start_time = new Date().getTime();
                                callback(data);
                                var end_time = new Date().getTime();

                                profile_info = {
                                        'id'                 : profile_id, 
                                        'start_time'         : start_time,
                                        'callback_start_time': callback_start_time,
                                        'end_time'           : end_time
                                };

                                // fire and forget the profile collector
                                moksha.json_load(moksha.url('/fcomm_connector/prof_collector'), profile_info, function(data){}, null, null);
                        }
                        return moksha.json_load(path, params, profile_callback, $overlay_div, loading_icon);
                } else {
                        return moksha.json_load(path, params, callback, $overlay_div, loading_icon);
                }
        },
}
