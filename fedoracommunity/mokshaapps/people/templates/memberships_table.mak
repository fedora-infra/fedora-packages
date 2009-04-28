 <html>
    <head>
    </head>
    <body>
      ${tmpl_context.widget(resource = 'fas',
                            resource_path = 'query_usermemberships',
                            filters = filters,
                            rows_per_page = rows_per_page,
                            more_link = more_link)}
    </body>
</html>