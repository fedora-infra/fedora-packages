<!-- this is the beginning of single_col_dashboard.mak -->
    <div id="container">
       <div id="content-column">
          <div>
             <h2 class="package-header"><span class="package-name">${package}</span> <span class="package-summary">${pkg_summary}</span></h2>
             <script type="text/javascript">
                 moksha.update_title("Package: ${package}", 2);
             </script>
          </div>

          % if error:
              ${error}
          % else:
              ${applist_widget(category = 'content-col-apps', layout = layout)}
          % endif
       </div>
    </div>
<!-- this is the end of single_col_dashboard.mak -->
