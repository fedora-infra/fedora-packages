<div class="list header-list">
    <script type="text/javascript">
        function _text_filter(text) {
            var results = $("<div />");
            var ul = $("<ul />");
            results.append(ul);
            var v=text.split('\n');
            for (i in v) {
                line = v[i];
                ul.append("<li>" + line + "</li>");
            }

            return results.html();
        }
    </script>
    <table id="${id}">
        <thead>
          <th>Bug</th>
          <th>Status</th>
          <th>Description</th>
          <th>Release</th>
        </thead>
        <tbody class="rowtemplate">
                <tr>
                    <td>
                        <a href="https://bugzilla.redhat.com/show_bug.cgi?id=@{id}" target="_blank">@{id}</a>
                    </td>
                    <td>
                        @{status}
                    </td>
                    <td>
                        @{description}</div>
                    </td>
                    <td>
                        @{release}
                    </td>
                </tr>
            </tbody>
    </table>
</div>
