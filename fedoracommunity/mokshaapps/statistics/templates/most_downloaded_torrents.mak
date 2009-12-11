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
          <th>Torrent Name</th>
   	      <th>Number of completed downloads</th>
        </thead>
        <tbody class="rowtemplate">
                <tr>
                    <td>
                        @{torrent_name}
                    </td>
		    <td>
		        @{number_of_completed}
		    </td>
            </tr>
            </tbody>
    </table>
<div id="grid-controls" if="total_rows == 0">
    <div class="message template" id="info_display" >
        No torrents downloaded.
    </div>
</div>
<div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0">
    <div class="message template" id="info_display" >
       Viewing all torrents being downloaded.
    </div>

    <div class="pager template" id="pager" type="more_link">
       <a href="http://torrent.fedoraproject.org:6969/">View complete torrent statistics information &gt;</a>
    </div>
</div>
<div id="grid-controls" if="visible_rows < total_rows">
    <div class="message template" id="info_display" >
       Viewing @{first_visible_row}-@{last_visible_row} of @{total_rows} most downloaded torrents
    </div>
    <div class="pager" id="pager" type="numeric" ></div>
    <div class="pager template" id="pager" type="more_link">
       <a href="@{more_link}" moksha_url="dynamic">View more torrents &gt;</a>
    </div>
</div>
</div>
