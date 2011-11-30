<div id="overview">
    <div class="description-block">
        <h3>Description</h3>
        <p class="package-description">${w.description}</div>
    </div>
    <div class="active-release-block">
        <h3>Active Releases Overview</h3>
        <div>${w.children[0].display(package_name=w.package_info['name'])}</div>
    </div>
    <div class="upstream-block">
        <h3>Upstream Summary</h3>
        <div class="homepage-block">
            <h4>Project Homepage</h4>
            <%
                homepage = w.package_info.get('upstream_url', 'Unknown')
            %>
            <a href="${homepage}">${homepage}</a>
        </div>
    </div>
</div>
