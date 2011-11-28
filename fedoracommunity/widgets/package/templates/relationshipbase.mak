<div>
    <div>
        <h3>Contents</h3>
        <div>
        <div id='grid-controls'>
          <form>
            <div id="filter" class="grid_filter" name="build_filter">
              <label for="build_id">Build:</label>
                <script type="text/javascript">

                    <%
                    import json
                    json_build_arch_tasks = json.dumps(w.build_to_archtask_map)
                    %>

                    var build_arch_tasks = ${json_build_arch_tasks};
                    var $grid = null;

                    function update_grid() {
                        if ($grid == null)
                            throw "Grid is not registered";

                        var build_id = $("#build_select").val();
                        var arch_index = $("#arch_select").val();
                        var task = build_arch_tasks[build_id][arch_index];
                        var nvr = task['nvr'];
                        var arch = task['label'];

                        $grid.mokshagrid("request_update",{"filters":{"nvr": nvr,
                                                           "arch": arch}});
                    }

                    function register_grid(grid) {
                        $grid = grid;
                    }

                    function on_build_change(self) {
                        var archs = build_arch_tasks[self.value];
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
                <select name="build_id" id="build_select" onChange="on_build_change(this)">
                  % for (i, build) in enumerate(w.latest_builds.keys()):
                    <%
                        selected = ""
                        if i == 0:
                            selected = 'selected = "selected"'
                        build_values = w.latest_builds[build]

                        display_ver = ""

                        epoch = build_values.get('epoch', None)
                        vr = "%s-%s" % (build_values['version'], build_values['release'])
                        if epoch is not None:
                            display_ver = "%s:%s" % (epoch, vr)
                        else:
                            display_ver = vr
                    %>
                    <option ${selected} value="${str(build_values['build_id'])}">${build} (${display_ver})</option>
                  % endfor
                </select>
                <label for="arch_task_id">Arch:</label>
                <select name="arch_task_id" id="arch_select" onChange="update_grid()">
                  % for (i, arch_task) in enumerate(w.latest_builds.values()[0]['arch_tasks']):
                    <%
                        selected=  ""
                        if i == 0:
                            selected = 'selected'

                        arch = arch_task['label']
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
