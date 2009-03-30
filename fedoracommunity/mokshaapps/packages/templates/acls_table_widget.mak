
    <div class="list header-list">
        <script type="text/javascript">
            function _roles_filter(v) {
                var results = "";
                for (i in v) {
                    role = v[i];

                    results += "<div>" + role + "</div>";
                }

                return results;
            }
        </script>
        <table id="${id}">
            <thead>
              <th>Name</th>
              <th>Type</th>
              <th>Role(s)</th>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <span>
                                <a href="">@{name}</a>
                            </span>
                        </td>
                        <td>
                            @{type}
                        </td>
                        <td>
                            @{roles:filter(_roles_filter)}
                        </td>
                    </tr>
                </tbody>
        </table>
    </div>