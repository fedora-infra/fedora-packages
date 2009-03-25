<html>
    <head>
    </head>
    <body>

        ${tmpl_context.widget(resource = 'pkgdb',
                            resource_path = 'list_packages',
                            filters = filters,
                            rows_per_page = rows_per_page)}
    </body>
</html>