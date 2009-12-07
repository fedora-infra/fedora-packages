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
                        <a href="/people?username=@{last_edited_by}" moksha_url="dynamic">@{last_edited_by}</a>
                    </td>
                </tr>
            </tbody>
    </table>
<div id="grid-controls" if="total_rows == 0">
    <div class="message template" id="info_display" >
        No recently-edited wiki pages.
    </div>
</div>
<div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0">
    <div class="message template" id="info_display" >
       Viewing all recently-edited wiki pages
    </div>

    <div class="pager template" id="pager" type="more_link">
       <a href="https://fedoraproject.org/wiki/Special:RecentChanges">View recent wiki changes &gt;</a>
    </div>
</div>
<div id="grid-controls" if="visible_rows < total_rows">
    <div class="message template" id="info_display" >
       Viewing @{first_visible_row}-@{last_visible_row} of @{total_rows} recently-edited pages
    </div>
    <div class="pager" id="pager" type="numeric" ></div>
    <div class="pager template" id="pager" type="more_link">
       <a href="@{more_link}" moksha_url="dynamic">View more in-progress builds &gt;</a>
    </div>
</div>
</div>
