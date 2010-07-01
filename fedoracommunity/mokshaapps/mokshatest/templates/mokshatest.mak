<html moksha:xmlns="https://fedorahosted.org/moksha">
    
    <head>
    <script type="text/javascript" src="/toscawidgets/resources/tw.jquery.base/static/javascript/jquery-1.4.2.js"></script>
<script type="text/javascript" src="/toscawidgets/resources/moksha/public/javascript/moksha.js"></script>
<script type="text/javascript" src="/toscawidgets/resources/tw.jquery.ui_core/static/javascript/ui/ui.core.js"></script>
<script type="text/javascript" src="/toscawidgets/resources/tw.jquery.ui/static/javascript/ui/ui.widget.js"></script>
<script type="text/javascript" src="/toscawidgets/resources/tw.jquery.ui/static/javascript/ui/ui.tabs.js"></script>

<script type="text/javascript" src="/toscawidgets/resources/moksha/public/javascript/jquery.json.js"></script>
<script type="text/javascript" src="/toscawidgets/resources/moksha/public/javascript/jquery.template.js"></script>
<script type="text/javascript" src="/toscawidgets/resources/moksha/public/javascript/moksha.extensions.js"></script>
<script type="text/javascript" src="/toscawidgets/resources/moksha/public/javascript/ui/moksha.ui.tabs.js"></script>
<script type="text/javascript" src="/toscawidgets/resources/moksha/public/javascript/ui/moksha.ui.grid.js"></script>

    </head>
    <body>

        <script type="text/javascript">
          moksha_base_url = "/";
          moksha_csrf_token = "";
          moksha_csrf_trusted_domains = {"admin.fedoraproject.org": true};
          moksha_userid = "";
          moksha_debug = true;
          moksha_profile = false;
        </script>

        

        <div class="list header-list">
        <table id="koji_grid">
            <thead>
                <tr>
                    <th><a href="#build_id">Build ID</a></th>
                    <th><a href="#nvr">Name</a></th>
                    <th><a href="#owner_name">Built By</a></th>
                    <th>State</th>
                </tr>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>@{build_id}</td>

                        <td>
                            <span class="package-name">
                                <a href="http://localhost/koji/buildinfo?buildID=@{build_id}">@{package_name}</a>
                            </span>
                            <div>@{version}</div>
                            <div class="moksha_extpoint">
                        	    {
                        	        'type': 'make_menu',
                        	        'placeholder_id': 'menu_@{build_id}',
                        	        'build_id': '@{build_id}',
                        	        'show_effect': 'slideDown(\"slow\")'
                        	    }
                            </div>
                        </td>
                        <td>
                            <span class="person-name"><a href="/people/package_maintenance/builds_overview?username=@{owner_name}" moksha_url="dynamic">@{owner_name}</a></span>
                        </td>
                        <td><img src="@{build['mf_state_img']}" /></td>
                        <td id="@{release_id}">
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td colspan="7"
                            id="@{message_id}"
                            class="message_row">
                        </td>
                    </tr>
                </tbody>

        </table>
        <div id="bodhi_grid" />
       </div>

      <script type="text/javascript">
            var kg = $("#koji_grid").mokshagrid({resource:'koji', resource_path:'query_builds'});
            var bg = $("#bodhi_grid").mokshagrid({resource:'bodhi', resource_path:'query_updates'});

        </script>
    </body>
</html>
