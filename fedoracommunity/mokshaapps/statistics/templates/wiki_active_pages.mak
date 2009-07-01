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
          <th>Page Name</th>
	  <th>Number of edits</th>
          <th>Last edited by</th>
        </thead>
        <tbody class="rowtemplate">
                <tr>
                    <td>
                        <a href="https://fedoraproject.org/wiki/@{title}" target="_blank">@{title}</a>
                    </td>
		    <td>
		        <a href="https://fedoraproject.org/w/index.php?title=@{title}&action=history">@{number_of_edits}</a>
		    </td>
                    <td>
                        @{last_edited_by}
                    </td>
                </tr>
            </tbody>
    </table>
</div>
