<%
import tg
%>
<html>
<head></head>
<body>
    <script type="text/javascript">
        function render_provided_by_list(prov_by_list) {
            var result = "";
            for (var i = 0; i < prov_by_list.length; i++) {
                if (i > 0)
                    result += "<br />";
                var url = moksha.url('/' + prov_by_list[i] + '/relationships/requires');
                result += '<a href="'+ url + '">' + prov_by_list[i] + '</a>';
            }
            return result;
        }
    </script>
    <div class="list header-list">
        <div id="grid-controls">
            <div class="message template" id="info_display" >
               ${'${total_rows}'} total requirements
            </div>
        </div>
        <table id="${w.id}" class="">
            <thead>
                <tr>
                    <th>Requires</th>
                    <th>Provided By</th>
                </tr>
            </thead>

            <tbody class="rowtemplate">
                    <tr>
                        <td>
                          ${'${name}'} ${'${ops}'} ${'${version}'}
                        </td>

                        <td>
                          {{html render_provided_by_list(provided_by)}}
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
