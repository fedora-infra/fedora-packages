
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
              <th>Version</th>
              <th>Changes</th>
              <th>Author</th>
              <th>Date</th>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            @{version}
                        </td>
                        <td>
                            @{text:filter(_text_filter)}
                        </td>
                        <td>
                            <div>@{author}</div>
                            <div>@{email}</div>
                        </td>
                        <td>
                            @{display_date}
                        </td>
                    </tr>
                </tbody>
        </table>
    </div>