<div id="${id}">
  % for a in alerts:
    <dl>
      <dt>${a['label']}</dt>
      % for i in a['items']:
        <dd>
          <img src="/images/${i['icon']}" />
            <span>
            <a href="javascript:moksha.goto('${i['url']}')">${i['count']} ${i['label']}</a>
                 [ <a href="javascript:moksha.goto('${i['url']}')]">View details</a> ]
            </span>
        </dd>
      % endfor
   </dl>
  % endfor
</div>
