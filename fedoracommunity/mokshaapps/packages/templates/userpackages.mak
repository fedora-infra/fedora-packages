<html>
    <head>
    </head>
    <body>
     % if categories:
      % for c in categories:
        <div>
          <h4>${c['label']} </h4>
          ${tmpl_context.widget(resource = 'pkgdb',
                            resource_path = 'query_userpackages',
                            filters = c['filters'],
                            rows_per_page = c['rows_per_page'],
                            more_link = c['more_link'])}
        </div>
      % endfor
     % else:
        ${tmpl_context.widget(resource = 'pkgdb',
                            resource_path = 'query_userpackages',
                            filters = filters,
                            rows_per_page = rows_per_page,
                            more_link = more_link)}
     % endif
    </body>
</html>
