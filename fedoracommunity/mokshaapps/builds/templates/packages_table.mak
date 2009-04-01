<html>
    <head>
    </head>
    <body>

        ${tmpl_context.widget(resource = 'koji',
                            resource_path = 'query_packages',
                            filters = filters,
                            rows_per_page = rows_per_page,
                            more_link=more_link,
                            alphaPager=True)}
    </body>
</html>