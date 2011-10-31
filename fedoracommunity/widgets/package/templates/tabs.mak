<!-- start tabs -->
  <div class="tab-container">
    <div class="tabs">
        % for key, value in tabs.items():
          <ul>
            <li>
            <a href="${base_url}${key}" onClick="return moksha.dynamic_goto('/_w/${value['widget_key']}', ${kwds},
                                      '#tab_content_${_uuid}', '${base_url}${key}');">
                ${value['display_name']}
            </a>
            </li>
          </ul>
        % endfor
    </div>
    <div id="tab_content_${_uuid}">
        ${widget(args=args, kwds=kwds) | n }
    <div>
  </div>
<!-- end tabs -->
