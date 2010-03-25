// This file is part of Fedora Community.
// Copyright (C) 2008-2009  Red Hat, Inc.
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

function get_nvr(build) {
    var nvr = build.split('-');
    var version = nvr.slice(nvr.length - 2, nvr.length - 1).join('-');
    var release = nvr.slice(nvr.length - 1, nvr.length).join('-');
    var name = nvr.slice(0, nvr.length - 2).join('-');
    return {
        'name': name,
        'version': version,
        'release': release,
        'nvr': build,
        }
}

function update_id(update) {
    return update.replace(/\./g, '').replace(/,/g, '');
}

function update_action(update, action) {
    args = {}
    args['update'] = update;
    args['action'] = action;

    if (typeof(moksha_csrf_token)!='undefined' && moksha_csrf_token) {
        args['_csrf_token'] = moksha_csrf_token;
    }

    $.getJSON(moksha.url('/moksha_connector/bodhi/request_data/request'), args, function(json) {
        json = json[1];
        $('#flash').text('');
        $('div.left-content-column')
            .prepend($('<span/>')
            .attr('id', 'flash')
            .text(json.tg_flash))
            .show('slow');

        if (typeof(json.update) != 'undefined' && json.update.request == action) {
            $('#' + update_id(update) + '_' + action).hide('slow');
        }
    });

}

function get_menu_links(nvr) {
    return $('<ul/>').append(
       $('<li/>').append(
         $('<a/>').attr('href', 'https://admin.fedoraproject.org/updates/' + nvr.nvr).append(
           $('<img/>').attr('src', moksha.url('/images/16_bodhi.png'))
         ).append(
           $('<span/>')
             .append('Go to this ')
             .append($('<strong/>').text('update'))
             .append(' in Bodhi')
         ).append(
           $('<img/>').attr('src', moksha.url('/images/16_offsite-link.png'))
         )
       )
    ).append(
       $('<li/>').append(
         $('<a/>').attr('href', 'http://koji.fedoraproject.org/koji/search?type=build&match=glob&terms=' + nvr.nvr).append(
           $('<img/>').attr('src', moksha.url('/images/16_koji.png'))
         ).append(
           $('<span/>')
             .append('Go to the ')
             .append($('<strong/>').text('build'))
             .append(' in Koji')
         ).append(
           $('<img/>').attr('src', moksha.url('/images/16_offsite-link.png'))
         )
       )
    ).append(
       $('<li/>').append(
         $('<a/>').attr('href', 'https://admin.fedoraproject.org/pkgdb/acls/name/' + nvr.name).append(
           $('<img/>').attr('src', moksha.url('/images/16_pkgdb.png'))
         ).append(
           $('<span/>')
             .append('Go to ' + nvr.name + ' ')
             .append($('<strong/>').text('package info'))
             .append(' in the PackageDB')
         ).append(
           $('<img/>').attr('src', moksha.url('/images/16_offsite-link.png'))
         )
       )
    ).append(
       $('<li/>').append(
         $('<a/>').attr('href', 'https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&classification=Fedora&product=Fedora&bug_status=NEW&bug_status=ASSIGNED&bug_status=MODIFIED&component=' + nvr.name).append(
           $('<img/>').attr('src', moksha.url('/images/16_bugzilla.png'))
         ).append(
           $('<span/>')
             .append('Go to ' + nvr.name + ' ')
             .append($('<strong/>').text('bugs'))
             .append(' in Bugzilla')
         ).append(
           $('<img/>').attr('src', moksha.url('/images/16_offsite-link.png'))
         )
       )
    );
}

function generate_package_column(build) {
    var nvr = get_nvr(build);
    var build_id = update_id(build);
    var entry = $('<div/>').addClass('menu')
                  .attr('id', 'menu_' + build_id)
                  .attr('panel', 'menu_panel_' + build_id);

    $('<span/>').addClass('package-name')
      .append(
        $('<a/>')
            .attr('href', '/package_maintenance/tools/updates?package=' + nvr.name)
            .attr('moksha_url', 'dynamic')
            .text(nvr.name))
      .append('<br/>')
      .appendTo(entry);

    $('<span/>').addClass('version')
      .append(nvr.version + '-' + nvr.release)
      .append('<br/><br/>')
      .appendTo(entry);

    $('<span/>').addClass('menu_panel')
      .attr('id', 'menu_panel_' + build_id)
      .append(
        $('<h4/>')
          .append('Quick links for ')
          .append($('<strong/>').text(nvr.name)))
      .append(get_menu_links(nvr))
      .appendTo(entry);

    $("<moksha_extpoint/>")
      .append("{'type': 'make_menu', 'placeholder_id': 'menu_" + build_id + "', 'id': '" + build_id + "_id'}")
      .appendTo(entry);

    return entry;
}


function render_update_builds(update) {
    var updateid = update_id(update) + '_packages';
    var result = $('<div/>').attr('id', updateid);
    var builds = update.split(',');
    var partial = false;
    var orig_result = null;

    if (builds.length > 2) {
        partial = true;
        result.append(
            $('<span/>')
              .append($('<strong/>').text('Multiple-Build Update '))
              .append('(' + builds.length + ' packages)')
        );
        result.append('<br/><br/>');
        result.append(generate_package_column(builds[0]));
        orig_result = result;
        result = $('<div/>').attr('id', updateid + '_hidden');
        builds = builds.slice(1, builds.length);
    }

    $.each(builds, function(i, build) {
        result.append(generate_package_column(build));
    });

    $('span.version br:last').remove();

    if (partial) {
        orig_result.append(result);
        result = orig_result;
    }

    result = $('<div/>').append(result);
    html = result.html();

    if (partial) {
        html += '<script>$("#' + updateid + '_hidden").expander({slicePoint: 0, expandText: "<strong>Show package list</strong> <img src=/community/images/arrow_down.png />", userCollapseText: "<strong>Hide package list</strong> <img src=/community/images/arrow_up.png />", expandPrefix: ""});</script>';
    }

    return html;
}
