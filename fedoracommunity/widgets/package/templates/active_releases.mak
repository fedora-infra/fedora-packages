<html>
<head></head>
<body>
<div class="list header-list">
    <table id="${w.id}" class="table table-sm table-hover">
        <thead class="thead-default">
            <tr>
                <th>Release</th>
                <th class="nowrap">Latest Released Version</th>
                <th class="nowrap">Version in Testing</th>
            </tr>
        </thead>
        <tbody class="rowtemplate">
            <tr>
                <td class="stretch-table-column">
                    <div>{{html release}}&nbsp;</div>
                </td>
                <td class="nowrap">{{html stable_version}}</td>
                <td class="nowrap">{{html testing_version}}</td>
            </tr>
        </tbody>
    </table>
</div>
</body>
</html>
