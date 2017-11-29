<html>
    <%def name="footer(package_name=None)">
        <div class="container">
          <div id="bottom" class="text-muted text-xs-center pt-3 pb-3">
            <p>Found a bug on this website?  <a href="https://github.com/fedora-infra/fedora-packages/issues/new">File a ticket.</a> For bugs in packages, click the "Open a New Bug" link on the packages Bugs page.   Note:  There's some caching going on here.  If you expect something and don't see it, check back in 5 minutes.</p>
            This Web Site is licensed under the GNU Affero General Public License.  You may get sources for the current running code from these repositories:
            <div>
                <a href="https://fedoraproject.org/wiki/Legal/TrademarkGuidelines">Trademark Guidelines</a> |
                <a href="https://github.com/fedora-infra/fedora-packages">Get the source for Fedora Packages</a> |
                <a href="https://github.com/mokshaproject">Get the source for Moksha</a> |
                <a href="https://kojipkgs.fedoraproject.org/packages/fedora-packages/">Fedora Packages SRPMS</a>
            </div>
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
				<script>
				/*quick re-implement of dropdowns as fedora-bootstrap requires 1.9.1 of jquery*/
				$(".dropdown").click(function(e){
					e.stopPropagation();
					$(".dropdown-menu", this).toggle();
				});

					$(document).click(function(){
					$('.dropdown-menu').hide();

					});
				</script>
    </%def>
</html>