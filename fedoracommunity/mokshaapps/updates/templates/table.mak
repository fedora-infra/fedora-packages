<html>
    <head>
    </head>
    <body>
        ${tmpl_context.widget(rows_per_page = rows_per_page,
                            resource = 'bodhi',
                            resource_path = 'query_updates',
                            filters = filters)}
    </body>
</html>