<html>
    <head>
    </head>
    <body>
     % if categories:
      % for c in categories:
        <div>
          <h4>${c['label']} </h4>
          ${tmpl_context.widget(filters = c['filters'],
                                rows_per_page = c['rows_per_page'],
                                more_link = c['more_link'])}
        </div>
      % endfor
     % else:
        % if title:
            <h3>${title}</h3>
        % endif
        ${tmpl_context.widget(filters = filters,
                              rows_per_page = rows_per_page,
                              more_link = more_link)}
     % endif
    </body>
</html>
