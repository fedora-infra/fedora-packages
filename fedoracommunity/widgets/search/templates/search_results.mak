<!-- START Search Results -->
<% import tg %>
<div class="container_24">
  <div class="grid_24" id="search-results-table">
    <div class="grid_12 suffix_12" id="search-notes">
      <div id="grid-controls" if="filters.search!=''">
        <div class="message template text-xs-center text-muted py-1" id="info_display">
           ${'${total_rows}'} results
        </div>
      </div>
    </div>
    <table id="${w.id}" class="table">
      <tbody class="rowtemplate">
        <tr class="priority4">
            <td>
                <span><a href="${tg.url('/${link}')}">${'{{html name}}'}</a></span>
            </td>
            <td>
                ${'{{html summary}}'}
            </td>
        </tr>
          <!-- {{each(index, pkg) sub_pkgs}} -->
          <tr class="subpackage">
              <td>
                  <span><a href="${tg.url('/') + '${pkg[\'link\']}'}">${'{{html pkg["name"]}}'}</a></span>
              </td>
              <td>${'{{html pkg["summary"]}}'}</td>
          </tr>
          <!-- {{/each}} -->
      </tbody>
    </table>
    <div id="grid-controls">
        <div class="pager text-xs-center mb-3" id="pager" type="more"></div>
   </div>
   <script type="text/javascript">

       function update_search_grid(search_term) {
            var grid = $("#${w.id}").mokshagrid("request_update", {"filters":{"search": search_term}});
       }

       function ready_search() {
           var search_term = "${w.filters['search']}";
           if (search_term) {
               search_term = encodeURIComponent(encodeURIComponent(search_term));
               moksha.defer(this, update_search_grid, [search_term]);
           }

       }
   </script>
</div>

<!-- END Search Results -->
