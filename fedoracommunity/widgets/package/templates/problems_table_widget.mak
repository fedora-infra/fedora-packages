<% import tg %>
<html>
<head></head>
<body>
<div style="padding-top: 10px; padding-bottom: 30px;">
Listing problems occurred in the last two weeks. For more information see <a href="https://retrace.fedoraproject.org/faf/problems/?component_names=${w.package}">FAF server</a>.
</div>
<div class="list header-list">
    <table id="${w.id}" class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Status</th>
                <th>Crash function</th>
                <th>Count</th>
            </tr>
        </thead>
        <tbody class="rowtemplate">
            <tr class="">
                <td><a href="https://retrace.fedoraproject.org/faf/problems/${'${id}'}">${'${id}'}</a></td>
                <td>${'${status}'}</td>
                <td>${'${crash_function}'}</td>
                <td>${'${count}'}</td>
            </tr>
        </tbody>
    </table>
</div>
</body>
</html>
