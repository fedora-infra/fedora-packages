
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
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <span class="@{roles}">
                                <a href="/people/?username=@{name}" moksha_url="dynamic">@{name}</a>
                            </span>
                        </td>
                    </tr>
                </tbody>
        </table>
    </div>