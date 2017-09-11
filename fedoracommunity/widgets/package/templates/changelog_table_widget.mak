<html>
<head></head>
<body>
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
        <div id="grid-controls">
          <form>
            <div id="filter" class="grid_filter" name="build_filter">
              <label for="version"><h4>Release:</h4></label>
                <select name="release">
                  % for (i, release) in enumerate(w.all_releases):
                    <%
                        selected = ""
                        if i == 0:
                            selected = 'selected = "selected"'
                    %>
                    <option ${selected} value="${release}">${release}</option>
                  % endfor
                </select>
            </div>
          </form>
        </div>
        <table id="${w.id}" class="table">
            <thead>
              <th>Version</th>
              <th>Changes</th>
              <th>Author</th>
              <th>Date</th>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <strong>${'${version}'}</strong>
                        </td>
                        <td>
                            {{html _text_filter(text)}}
                        </td>
                        <td>
                            <strong>${'${author}'}</strong><br/>
                            <a href="mailto:${'${email}'}">&lt;${'${email}'}&gt;</a>
                        </td>
                        <td>
                            ${'${display_date}'}
                        </td>
                    </tr>
                </tbody>
        </table>
        <div id="grid-controls" if="total_rows == 0">
            <div class="message template" id="info_display" >
                This package has no Changelog entries
            </div>
        </div>
        <div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0">
            <div class="message template" id="info_display" >
               Viewing all Changelog entries
            </div>
        </div>
        <div id="grid-controls" if="visible_rows < total_rows && total_rows != 0">
            <div class="message template" id="info_display" >
               Viewing ${'${first_visible_row}'}-${'${last_visible_row}'} of ${'${total_rows}'} Changelog entries
            </div>
            <div class="pager" id="pager" type="more" ></div>

        </div>
    </div>
</body>
</html>
