<html>
    <head>
    </head>
        <div class="list header-list">
        <table id="grid">
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
                                <a href="http://localhost/koji/buildinfo?buildID=@{build_id}" target="_blank">@{package_name}</a>
                            </span>
                            <div>@{version}</div>
                        </td>
                        <td>
                            <span class="person-name"><a href="/people/name/@{owner_name}/builds">@{owner_name}</a></span>
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
       </div>
      <script type="text/javascript">
            var g = $("#grid").mokshagrid({resource:'koji', resource_path:'query_builds'});
        </script>
</html>