<html>
<head></head>
<body>
    <div class="list header-list">
        <div id="grid-controls">
            <div class="message template" id="info_display" >
               ${'${total_rows}'} total provides
            </div>
        </div>
        <table id="${w.id}" class="">
            <thead>
                <tr>
                    <th>Provides</th>
                </tr>
            </thead>

            <tbody class="rowtemplate">
                    <tr>
                        <td>
                          ${'${name}'} ${'${ops}'} ${'${version}'}
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
