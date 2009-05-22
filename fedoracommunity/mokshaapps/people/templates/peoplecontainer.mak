    <div id="container">
       <div class="header-content-column">
          % if not profile:
              <script type="text/javascript">
                  moksha.update_title("User: ${username}", 2);
              </script>
          % endif
          % if not profile:
            <h2>${human_name}</h2>
          % endif
          % if error:
            ${error}
      </div>
          % else:
      </div>
            % for c in layout:
                ${applist_widget(category=c)}
            % endfor
          % endif
    </div>
    <div class="clear" />
