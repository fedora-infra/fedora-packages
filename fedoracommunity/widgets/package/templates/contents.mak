<div class="tab-container">
        <div id="grid-controls"">
          <form>
            <div id="filter" class="grid_filter" name="build_filter"
                <!-- BEGIN Release Dropdown Filter **/ -->
                <div class="filter grid_9 alpha">
                <label for="build_id"><h4>Release:</h4></label>
                  <script type="text/javascript">
                    <%
                    import json
                    import tg
                    json_repo_arch_tasks = json.dumps(w.repo_to_archtask_map)
                    %>
                      var repo_arch_tasks = ${json_repo_arch_tasks};

                      function on_repo_change(self) {
                          var archs = repo_arch_tasks[self.value];
                          var $arch_select = $('#arch_select');
                          $arch_select.html('');
                          for (var i in archs) {
                              var task = archs[i];
                              var arch_name = task['label'];
                              var task_id = task['id'];
                              var $option = $("<option></option>").text(arch_name).attr('value', i);
                              $arch_select.append($option);
                          }

                          displayTree();
                      }

                      function displayTree() {
                          var $tc = $('#tree_content').html('');
                          var $arch_select = $('#arch_select');
                          var $repo_select = $('#repo_select');

                          var arch_index = $arch_select.val();
                          var repo = $repo_select.val();
                          var task = repo_arch_tasks[repo][arch_index];
                          var nvr = task['nvr'];
                          var package = task['package'];
                          var arch = task['label'];

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
                                                   'arch': arch,
                                                   'repo': repo
                                               }
                                           }
                                       }
                                     });
                         /*
                          fcomm.connector_load('yum', 'get_file_tree', {'package': package,
                                                                         'arch': arch,
                                                                         'repo': repo}, done_cb);
                          */
                      }
                  </script>
                  <select name="repo" id="repo_select" onChange="on_repo_change(this)">
                    % for (i, repo) in enumerate(w.latest_builds.keys()):
                      <%
                          selected = ""
                          if i == 0:
                              selected = 'selected = "selected"'
                          build_values = w.latest_builds[repo]

                          display_ver = ""

                          epoch = build_values.get('epoch', None)
                          vr = "%s-%s" % (build_values['version'], build_values['release'])
                          if epoch is not None:
                              display_ver = "%s:%s" % (epoch, vr)
                          else:
                              display_ver = vr
                      %>
                      <option ${selected} value="${repo}">${repo} (${display_ver})</option>
                    % endfor
                  </select>
              </div>
              <!-- END Release Dropdown Filter -->
              <!-- BEGIN Arch Dropdown Filter -->
              <div class="filter grid_9 omega">
                <label for="arch_task_id"><h4>Architecture:</h4></label>
                <select name="arch_task_id" id="arch_select" onChange="displayTree(this.value)">
                  % for (i, arch_task) in enumerate(w.latest_builds.values()[0]['arch_tasks']):
                    <%
                        selected=  ""
                        if i == 0:
                            selected = 'selected'
                        task_id = str(arch_task['id'])
                        arch = arch_task['label']
                    %>
                    <option ${selected} value="${str(i)}">${arch}</option>
                  % endfor
                </select>
              </div>
              <!-- END Arch Dropdown Filter -->
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

