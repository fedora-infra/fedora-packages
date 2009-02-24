<div id="${id}">
  % for a in alerts:
    <dl>
      <dt>${a['label']}</dt>
      % for i in a['items']:
        <dd>
          <span><img src="/images/${i['icon']}" /><span>
            <div><a href="${i['url']}">${i['count']} ${i['label']}</a><br />
                 [ <a href="${i['url']}">View details</a> ]
            </div>
        </dd>
      % endfor
    </dl>
  % endfor
</div>
