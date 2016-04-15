<html>
    <%def name="footer(package_name=None)">
        <div class="container_24">
          <div id="bottom" class="grid_24">
            <p>Found a bug on this website?  <a href="https://github.com/fedora-infra/fedora-packages/issues/new">File a ticket.</a> For bugs in packages, click the "Open a New Bug" link on the packages Bugs page.   Note:  There's some caching going on here.  If you expect something and don't see it, check back in 5 minutes.</p>
            This Web Site is licensed under the GNU Affero General Public License.  You may get sources for the current running code from these repositories:
            <ul>
                <li><a href="https://fedoraproject.org/wiki/Legal/TrademarkGuidelines">Trademark Guidelines</a></li>
                <li><a href="https://github.com/fedora-infra/fedora-packages">Get the source for Fedora Packages</a></li>
                <li><a href="https://fedorahosted.org/moksha">Get the source for Moksha</a></li>

                <li><a href="https://infrastructure.fedoraproject.org/testing/6/SRPMS/">RHEL6 Testing SRPMS</a></li>
                <li><a href="https://infrastructure.fedoraproject.org/6/SRPMS/">RHEL6 Production SRPMS</a></li>
            </ul>
          </div>
        </div>

        % if 'fedmenu.url' in config:
        <script src="${config['fedmenu.url']}/js/fedmenu.js"></script>
        <script>
          fedmenu({
              'url': '${config["fedmenu.data_url"]}',
              'mimeType': 'application/javascript',
              'position': 'bottom-right',
              % if package_name:
              'package': '${package_name}',
              % endif
          });
        </script>
        % endif

    </%def>
</html>
