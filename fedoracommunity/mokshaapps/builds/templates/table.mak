<html>
    <head>
    </head>
    <body>
        
        ${tmpl_context.widget(resource = 'koji',
                            resource_path = 'query_builds',
                            filters = filters,
                            rows_per_page = rows_per_page,
                            uid = uid)}
    </body>
</html>