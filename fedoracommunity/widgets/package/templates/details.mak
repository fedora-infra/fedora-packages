<% import tg %>
<div id="package-overview">
  <div class="description-block">
        <h3>Description</h3>
        <p class="package-description">${w.description}</p>
    </div>
    <div class="active-release-block">
        <h3>Active Releases Overview</h3>
        <div>${w.children[0].display(package_name=w.package_info['name'])}</div>
    </div>
    <%
        homepage = w.package_info.get('upstream_url', 'Unknown')
    %>
    % if homepage:
    <div class="upstream-block">
        <h3>Upstream Summary</h3>
        <div class="homepage-block">
            <h4>Project Homepage</h4>
            <a href="${homepage}">${homepage}</a>
        </div>
    </div>
    % endif
    <div class="history-block">
        <h3>Recent History</h3>
        <div class="history-cards">
          <div class="overlay"> <div class="message"></div> </div>
        </div>
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
          var line = '<span class="message-card">';
          if (msg.link != null) {
            line = line + '<a href="' + msg.link + '">';
          }
          if (msg.icon != null) {
            line = line + '<img src="' + msg.icon + '"/>'
          }
          if (msg.secondary_icon != null) {
            line = line + '<img src="' + msg.secondary_icon + '"/>'
          }
          if (msg.subtitle != null) {
            line = line + ' ' + msg.subtitle;
          }
          if (msg.link != null) {
            line = line + '</a>';
          }
          line = line + '<span class="datetime">' + msg['human_time'] + '</span>';
          line = line + '</span>';
          $('.history-cards').append(line + '<hr/>');
      });
    }
    var overlay = $('.history-cards .overlay');
    moksha.ajax_load(url, {}, callback, overlay, 'jsonp');
});
</script>

