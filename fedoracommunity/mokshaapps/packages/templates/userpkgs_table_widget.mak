
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
        <div id="grid-controls">
            <div class="message template" id="info_display" >
               Viewing @{visible_rows} of @{total_rows} packages
            </div>
            <div class="pager" id="pager" type="numeric" ></div>
        </div>
    </div>