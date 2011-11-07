<html>
<head></head>
<body>
<div class="list header-list">
    <table id="${w.id}">
        <thead>
            <tr>
                <th>Release</th>
                <th>Latest Released Version</th>
                <th>Version in Testing</th>
            </tr>
        </thead>
        <tbody class="rowtemplate">
            <tr>
                <td>
                    <div>{{html release}}&nbsp;</div>
                </td>
                <td>{{html stable_version}}</td>
                <td>{{html testing_version}}</td>
            </tr>
        </tbody>
    </table>
</div>
</body>
</html>
