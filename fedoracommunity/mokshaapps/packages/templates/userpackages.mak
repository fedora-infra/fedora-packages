<html>
    <head>
    </head>
    <body>
     % if categories:
      % for c in categories:
        <div class="panel">
          <h4>${c['label']} </h4>
          ${tmpl_context.widget(resource = 'pkgdb',
                            resource_path = 'query_userpackages',
                            filters = c['filters'],
                            rows_per_page = c['rows_per_page'])}
        </div>
      % endfor
     % else:
        ${tmpl_context.widget(resource = 'pkgdb',
                            resource_path = 'query_userpackages',
                            filters = filters,
                            rows_per_page = rows_per_page)}
     % endif
    </body>
</html>
