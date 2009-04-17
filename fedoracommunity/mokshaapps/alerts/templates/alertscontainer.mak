<div id="${id}">
  % for a in alerts:
    <dl>
      <dt>${a['label']}</dt>
      % for i in a['items']:
        <dd>
          <img src="/images/${i['icon']}" />
            <a href="javascript:moksha.goto('${i['url']}')">${i['count']} ${i['label']}</a>
        </dd>
      % endfor
   </dl>
  % endfor
</div>
