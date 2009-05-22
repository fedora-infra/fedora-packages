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
                <tr class="@{bug_class}">
                    <td>
                        <a href="https://bugzilla.redhat.com/show_bug.cgi?id=@{id}" target="_blank">@{id}</a>
                    </td>
                    <td>
                        @{status}
                    </td>
                    <td>
                        @{description}
                    </td>
                    <td>
                        @{release}
                    </td>
                </tr>
            </tbody>
    </table>
    <div id="grid-controls" if="total_rows == 0">
        <div class="message template" id="info_display" >
            This package has no bugs - go file some!!!
        </div>
    </div>
    <div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0">
        <div class="message template" id="info_display" >
           Viewing all bugs for this package
        </div>
    </div>
    <div id="grid-controls" if="visible_rows < total_rows">
        <div class="message template" id="info_display" >
           Viewing @{visible_rows} of @{total_rows} bugs
        </div>
        <div class="pager" id="pager" type="numeric" ></div>
    </div>
</div>
