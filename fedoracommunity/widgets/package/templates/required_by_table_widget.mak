<%
import tg
%>
<html>
<head></head>
<body>
    <div class="list header-list">
        <div id="grid-controls">
            <div class="message template" id="info_display" >
               ${'${total_rows}'} total requirements
            </div>
        </div>
        <table id="${w.id}" class="">
            <thead>
                <tr>
                    <th>Required By</th>
                    <th>Details</th>
                </tr>
            </thead>

            <tbody class="rowtemplate">
                    <tr>
                        <td>
                          <a href="${tg.url('/${name}/relationships/requiredby')}">${'${name}'}</a>
                        </td>

                        <td>
                            ${'${requires["name"]}'} ${'${requires["ops"]}'} ${'${requires["version"]}'}
                        </td>

                    </tr>
                </tbody>
        </table>
        <div id="grid-controls" if="visible_rows < total_rows">
            <div class="pager" id="pager" type="more" ></div>
        </div>
    </div>
    <script type="text/javascript">
        var $grid = $("#${w.id}");
        register_grid($grid);
    </script>
</body>
</html>
