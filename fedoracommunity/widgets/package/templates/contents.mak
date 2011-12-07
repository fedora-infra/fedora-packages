<div class="tab-container">
        <div id="grid-controls"">
          <form>
            <div id="filter" class="grid_filter" name="build_filter">

							<!-- BEGIN Arch Dropdown Filter **/ -->
							<div class="filter grid_9 alpha">
             		<label for="build_id"><h4>Release:</h4></label>
              	  <script type="text/javascript">
              	  	<% 
											import json
											json_build_arch_tasks = json.dumps(w.build_to_archtask_map)
              	    %>
              	      var build_arch_tasks = ${json_build_arch_tasks};

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

              	          displayTree();
              	      }

              	      function displayTree() {
              	          var construct_ul_from_dir_list = function(list) {
              	              var $ul = $('<ul></ul>');
              	              for (var i in list) {
              	                  var $li = $('<li></li>');
              	                  var obj = list[i];
              	                  if (undefined != obj.dirname) {
              	                      // we are an directory, recurse
              	                      var $a = $("<a>" +obj.dirname + "</a>");
              	                      $a.addClass('jstree-directory');
              	                      $li.append($a);
              	                      $li.append(construct_ul_from_dir_list(obj.content));
              	                      $li.addClass('jstree-open');
              	                  } else {
              	                      var display = obj.name;
              	                      if (obj.type == 'L')
              	                          display += '->' + obj.linked_to;
	
              	                      var $a = $("<a>" + display + "</a>");
	
              	                      if (obj.type == 'L')
              	                          $a.addClass("jstree-link");
              	                      $li.append($a);
              	                  }
              	                  $ul.append($li);
              	              }

               	             return($ul);
                	        }
                	        var done_cb = function(data) {
                	            var $tc = $('#tree_content').html('');
                	            if (undefined != data.length) {
                	                var $root = construct_ul_from_dir_list(data);
                	                $root.attr('id','file_tree');
                	                $tc.append($root);
                	                $tc.jstree({"plugins": ["html_data", "themes", "search"],
                	                            "themes":{"url":"/css/filetreetheme/style.css",
                	                                      "icons": true,
                	                                      "dots": false}});
                	            } else if (undefined != data['error']) {
                	                $tc.append(data['error'].toString());
                	            } else {
                	                $tc.append(data.toString());
                	            }
                	        }

                	        var $arch_select = $('#arch_select');
                	        var $build_select = $('#build_select');
	
                	        var arch_index = $arch_select.val();
                	        var build_id = $build_select.val();
                	        var task = build_arch_tasks[build_id][arch_index];
                	        var nvr = task['nvr'];
                	        var arch = task['label'];
                	        moksha.connector_load('koji', 'get_file_tree', {'nvr': nvr,
            	                                                            'arch': arch}, done_cb);
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
          <script type="text/javascript">
              displayTree();
          </script>
        </div>
        <div id="tree_content">
        </div>
</div>

