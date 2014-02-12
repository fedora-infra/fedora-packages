<div>
    <div>
        <div>
        <div id='grid-controls'>
          <form>
            <div id="filter" class="grid_filter" name="build_filter">
              <label for="repo">Repo:</label>
                <script type="text/javascript">

                    <%
                    import json
                    json_repo_arch_tasks = json.dumps(w.repo_to_archtask_map)
                    %>

                    var $grid = null;
                    var repo_arch_tasks = ${json_repo_arch_tasks|n};

                    function update_grid() {
                        if ($grid == null)
                            throw "Grid is not registered";

                        var build_repo = $("#repo_select").val();
                        var arch_index = $("#arch_select").val();
                        var task = repo_arch_tasks[build_repo][arch_index];
                        var vr = task['version'];
                        var package = task['package'];
                        var arch = task['label'];

                        $grid.mokshagrid("request_update",{"filters":{
                                                             "package": package,
                                                             "version": vr,
                                                             "repo": build_repo,
                                                             "arch": arch}
                                                          });
                    }

                    function register_grid(grid) {
                        $grid = grid;
                    }

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
                        update_grid();
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
                <label for="arch_task_id">Arch:</label>
                <select name="arch_task_id" id="arch_select" onChange="update_grid()">
                  % for (i, arch_task) in enumerate(w.latest_builds.values()[0]['arch_tasks']):
                    <%
                        selected=  ""
                        arch = arch_task['label']
                        if arch == 'x86_64' or arch == 'noarch':
                            selected = 'selected'
                    %>
                    <option ${selected} value="${str(i)}">${arch}</option>
                  % endfor
                </select>
            </div>
          </form>
        </div>
        <div id="relationship_content">
            ${w.children[0].display(args=w.args, kwds=w.kwds) | n}
        </div>
        </div>
    </div>
</div>
