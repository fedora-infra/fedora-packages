<div class="tab-container">
        <div id="grid-controls">
          <form>
            <div id="filter" class="grid_filter" name="build_filter"
                <!-- BEGIN Release Dropdown Filter **/ -->
                <div class="filter grid_9 alpha">
                <label for="build_id"><h4>Release:</h4></label>
                  <script type="text/javascript">
                    <%
                    import json
                    import tg
                    %>
                      function on_repo_change(self) {
                          displayTree();
                      }

                      function displayTree() {
                          var $tc = $('#tree_content').html('');
                          var repo = $('#repo_select').val();
                          var package = "${w.package_name}";

                          $tc.jstree({"plugins": ["json_data", "themes"],
                                      "themes": {
                                          "url": moksha.url('/css/filetreetheme/style.css'),
                                          "icons": true,
                                          "dots": false
                                       },
                                       "json_data": {
                                           "ajax": {
                                               "url": moksha.url("/fcomm_connector/yum/get_file_tree"),
                                               "data": {
                                                   'package': package,
                                                   'repo': repo
                                               }
                                           }
                                       }
                                     });
                      }
                  </script>
                  <select name="repo" id="repo_select" onChange="on_repo_change(this)">
                    % for (i, repo) in enumerate(w.repos):
                      <%
                          selected = ""
                          if i == 0:
                              selected = 'selected = "selected"'
                      %>
                      <option ${selected} value="${repo}">${repo}</option>
                    % endfor
                  </select>
              </div>
              <!-- END Release Dropdown Filter -->
            </div>
            <div class="clear"></div>
          </form>
        </div>
        <div id="tree_content">
        </div>
        <script type="text/javascript">
            $(document).ready( function () { displayTree(); } );
        </script>
</div>
