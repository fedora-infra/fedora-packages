<div>
  <div id="container">
    <h2>Updates Overview:
    % if profile:
        Packages I Own
    % else:
        All Packages
    % endif
    </h2>
    % for c in layout:
        ${applist_widget(category=c)}
    % endfor
    </div>
</div>