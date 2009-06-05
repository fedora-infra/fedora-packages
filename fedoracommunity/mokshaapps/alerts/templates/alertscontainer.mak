<div id="${id}">
  % for alert_cat in alerts:
    <h4>${alert_cat['label']}</h4>
      % for a in alert_cat['alerts']:
        <h5>${a['label']}</h5>
        <dl>
          % for i in a['items']:
            <dd>
              <img src="${tmpl_context.get_url('/images/' + i['icon'])}" />
                <a href="${i['url']}" moksha_url="dynamic">${i['count']} ${i['label']}</a>
            </dd>
          % endfor
       </dl>
      % endfor
  % endfor
</div>
