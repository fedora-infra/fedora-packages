<% import tg %>
<div class="col-sm-9">
<div id="package-overview">
  <div class="description-block">
        <p class="package-description">${w.description}</p>
    </div>
    <div class="active-release-block">
        <h3>Active Releases Overview</h3>
        <div>${w.children[0].display(package_name=w.package_info['name'])}</div>
    </div>
    <%
        homepage = w.package_info.get('upstream_url', 'Unknown')
    %>

    <div class="history-block">
        <h3>Recent History</h3>
        <div class="history-cards list-group">
          <div class="overlay"> <div class="message"></div> </div>
        </div>
    </div>
</div>
</div>
<div class="col-sm-3 pl-2">

  % if homepage:
  <div class="upstream-block mb-1">
      <h4>Upstream</h4>
      <a href="${homepage}">${homepage}</a>
  </div>
  % endif

  <div class="package-tree mb-1">
      <div><h4>Package Tree</h4></div>
      <ul>
        <li><a class="package-name" href="${tg.url('/%s' % w.package_info['name'])}">${w.package_info['name']}</a>
        <ul>
            % for subpkg in w.package_info['sub_pkgs']:
                  <li><a class="package-name" href="${tg.url('/%s' % subpkg['name'])}">${subpkg['name']}</a></li>
            % endfor
        </ul>
      </li>
      </ul>
  </div>
  <div class="owner mb-1">
      <div><h4>Point of Contact</h4></div>
      % if w.package_info.get('devel_owner', None):
          % if w.package_info['devel_owner'].endswith('-maint'):
              <div class="package-owner"><a class="package-owner" href="https://admin.fedoraproject.org/pkgdb/users/packages/${w.package_info['devel_owner']}">${w.package_info['devel_owner']}</a> <span class="tag tag-info">Rawhide</span></div>
          % else:
              <div class="package-owner"><a class="package-owner" href="https://fedoraproject.org/wiki/User:${w.package_info['devel_owner']}">${w.package_info['devel_owner']}</a> <span class="tag tag-info">Rawhide</span> </div>
          % endif
      % else:
          <div class="package-owner orphan">Orphaned <span class="tag tag-info">Rawhide</span></div>
      % endif
  </div>
  <div class="build mb-1">
      <div><h4>Latest Build</h4></div>
      <div class="package-name">${w.latest_build}</div>
  </div>
</div>
<script>
$(document).ready(function() {
    var url = 'https://apps.fedoraproject.org/datagrepper/raw';
    var params = {
      'order': 'desc',
      'meta': ['subtitle', 'link', 'icon', 'secondary_icon'],
      'package': "${w.package_info['name']}",
      'grouped': true,
      'not_topic': [
        'org.fedoraproject.prod.buildsys.rpm.sign',
        'org.fedoraproject.prod.buildsys.tag',
        'org.fedoraproject.prod.buildsys.untag',
        'org.fedoraproject.prod.buildsys.package.list.change',
      ],
      'rows_per_page': 20,
    };
    url = url + '?' + $.param(params, traditional=true);
    var callback = function(whatever) {
      $.each(whatever.raw_messages, function(i, msg) {
          var line = '<div class="list-group-item">';
          if (msg.icon != null) {
            line = line + '<img src="' + msg.icon + '"/>'
          }
          if (msg.secondary_icon != null) {
            line = line + '<img src="' + msg.secondary_icon + '"/>'
          }

          line = line + ' <span class="datetime">' + msg['human_time'] + ' </span>';

	  var link = $("<a>");

          if (msg.link != null) {
	    link = link.attr("href", msg.link);
          }

          if (msg.subtitle != null) {
	    link = link.text(msg.subtitle);
          }

          line = line + link.html() + '</div>';
          $('.history-cards').append(line);
      });
    }
    var overlay = $('.history-cards .overlay');
    moksha.ajax_load(url, {}, callback, overlay, 'jsonp');
});
</script>
