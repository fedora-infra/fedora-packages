<html>
  <head></head>
  <body>
  <div id="container">
    % if title:
        <h${title_level}>${title}</h${title_level}>
    % endif
    ${tmpl_context.widget(**options)}
  </div>
  </body>
</html>