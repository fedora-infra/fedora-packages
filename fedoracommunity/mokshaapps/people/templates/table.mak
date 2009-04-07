<html>
    <head>
    </head>
    <body>
        <% filters['prefix'] = 'a' %>
        ${tmpl_context.widget(resource = 'fas',
                            resource_path = 'query_people',
                            filters = filters,
                            rows_per_page = rows_per_page,
                            more_link=more_link,
                            alphaPager=True)}
    </body>
</html>