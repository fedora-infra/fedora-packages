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
    <div class="history-block">
        <h3>History</h3>
        <div class="history-cards">
        <% 
            result = w.history
        %>
        <div> ${result['text'] | n} </div>
        </div>
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
</div>

