<html>
  <head></head>
  <body>
  <div id="container">
    % if title:
        <h2>${title}</h2>
    % endif
    ${tmpl_context.widget(**options)}
  </div>
  </body>
</html>