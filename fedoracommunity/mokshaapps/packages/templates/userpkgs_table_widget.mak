
    <div class="list header-list">
        <script type="text/javascript">
            function _release_filter(v) {
                var results = "";
                for (i in v) {
                    collection = v[i];

                    cname = collection.collectionname
                    cver = collection.collectionversion
                    if (cver == "devel")
                        release = "Rawhide";
                    else
                        release = cname + " " + cver;

                    results += "<div>" + release + "</div>";
                }

                return results;
            }
        </script>
        <table id="${id}">
            <thead>
              <th>Package Name</th>
              <th>Summary</th>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <span class="package-name">
                                <a href="/package_maintenance?package=@{name}" moksha_url="dynamic">@{name}</a>
                            </span>
                        </td>
                        <td>
                            @{summary}
                        </td>
                    </tr>
                </tbody>
        </table>
        <div id="grid-controls" if="total_rows == 0">
            <div class="message template" id="info_display" >
               This user has no packages
            </div>
        </div>
        <div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0">
            <div class="message template" id="info_display" >
               Viewing all @{total_rows} packages
            </div>
        </div>
        <div id="grid-controls" if="visible_rows < total_rows && total_rows != 0">
            <div class="message template" id="info_display">
               Viewing @{first_visible_row}-@{last_visible_row} of @{total_rows} packages
            </div>
            <div class="pager" id="pager" type="numeric" ></div>
        </div>
    </div>