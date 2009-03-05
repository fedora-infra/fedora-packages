<html>
    <head>
    </head>
    <body>
      % for c in categories:
        <div>
          <h4>${c['label']}</h4>
          ${tmpl_context.widget(resource = 'pkgdb',
                            resource_path = 'query_userpackages',
                            filters = c['filters'],
                            rows_per_page = c['rows_per_page'])}
        </div>
      % endfor
    </body>
</html>