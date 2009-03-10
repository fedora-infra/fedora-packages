
    <div class="list header-list">
        <script type="text/javascript">
            function _release_filter(v) {
                var results = "";
                for (i in v) {
                    collection = v[i];
                    console.log(collection);
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
              <th>Release(s)</th>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <span class="package-name">
                                <a href="">@{name}</a>
                            </span>
                        </td>
                        <td>
                            @{collections:filter(_release_filter)}
                        </td>
                    </tr>
                </tbody>
        </table>
    </div>