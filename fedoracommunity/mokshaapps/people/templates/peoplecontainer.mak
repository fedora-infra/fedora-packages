    <div id="container">
       <div class="header-content-column">
          % if not profile:
              <script type="text/javascript">
                  moksha.update_title("User: ${username}", 2);
              </script>
          % endif
          <div>
          <h2>${human_name}</h2>
          % if error:
            ${error}
          % else:
          ${applist_widget(category = 'header-content-column-apps', layout = layout)}
       </div>
       <div class="right-content-column">
          ${applist_widget(category = 'right-content-column-apps', layout = layout)}
       </div>
       <div class="left-content-column">
          ${applist_widget(category = 'left-content-column-apps', layout = layout)}
          % endif
       </div>

    </div>
    <div class="clear" />
