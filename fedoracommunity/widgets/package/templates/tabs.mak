<!-- start tabs -->
    <div class="tabs">
        % for key, value in tabs.items():
          <ul>
            <li>
            <a href="${key}" onClick="moksha.dynamic_goto('/_w/${value['widget_key']}', {},
                                      '#tab_content_${_uuid}', '${key}'); return false;">
                ${value['display_name']}
            </a>
            </li>
          </ul>
        % endfor
    </div>
    <div id="tab_content_${_uuid}">
        ${widget(args=args, kwds=kwds) | n }
    <div>
<!-- end tabs -->
