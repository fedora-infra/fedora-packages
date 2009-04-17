<div id="${id}">
  <H2>People</H2>
  % for c in layout:
    ${applist_widget(category=c)}
  % endfor
</div>