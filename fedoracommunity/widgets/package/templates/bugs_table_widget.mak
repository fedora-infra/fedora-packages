<div class="list header-list col-sm-9 pull-sm-3">
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

        $(document).ready(function() {
          $("#bug_search").keypress(function(e) {
            if (e.which == 13) {
              window.location = 'https://bugzilla.redhat.com/buglist.cgi?' + $.param({
                bug_status: ['NEW', 'ASSIGNED', 'REOPENED'],
                short_desc: $(this).val(),
                short_desc_type: 'allwords',
                component: '${w.package}',
                product: ['Fedora', 'Fedora EPEL'],
                query_format: 'advanced',
              }, traditional=true);
              return false;
            }
          });
        });
    </script>
    <div id='grid-controls'>
    <form>
        <div id="filter" class="grid_filter" name="release_filter">
            <label for="version">Release:</label>
            <select name="version">
                <option selected="selected" value="">All Dists</option>
                % for (i, rel) in enumerate(w.release_table):
                    <option value="${rel['value']}">${rel['label']}</option>
                % endfor
            </select>

            <!--<span class="pull-right">
                <label for="version">Search:</label>
                <input id="bug_search" type="text" name="search" placeholder="Bugzilla..."/>
            </span>-->
        </div>
    </form>
    </div>
    <table id="${w.id}" class="table">
        <thead>
          <th>Bug</th>
          <th>Status</th>
          <th>Description</th>
          <th>Release</th>
        </thead>
        <tbody class="rowtemplate">
                <tr class="${'${bug_class}'}">
                    <td>
                        <a href="https://bugzilla.redhat.com/show_bug.cgi?id=${'${id}'}" target="_blank">${'${id}'}</a>
                    </td>
                    <td>
                        ${'${status}'}
                    </td>
                    <td>
                        ${'${description}'}
                    </td>
                    <td>
                        ${'${release}'}
                    </td>
                </tr>
            </tbody>
    </table>
    <div id="grid-controls" if="total_rows == -1">
        <div class="message template" id="info_display" >
            Loading bugs... please hold on.
        </div>
    </div>
    <div id="grid-controls" if="total_rows == 0">
        <div class="message template" id="info_display" >
            This package has no bugs - go file some!!!
        </div>
    </div>
    <!--<div id="grid-controls" if="visible_rows >= total_rows && total_rows > 0">
        <div class="message template" id="info_display" >
           Viewing all bugs for this package
        </div>
    </div>-->
    <div id="grid-controls" if="visible_rows < total_rows && total_rows > 0">
        <div class="message template" id="info_display" >
           Viewing ${'${first_visible_row}'}-${'${last_visible_row}'} of ${'${total_rows}'} bugs
        </div>
        <div class="pager" id="pager" type="numeric" ></div>
    </div>
</div>
