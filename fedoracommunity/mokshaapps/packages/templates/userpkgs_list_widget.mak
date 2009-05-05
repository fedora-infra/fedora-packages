
    <div class="list header-list">
       <span id="grid-controls" attach="h4:first" ancestor="2">
          <span id="info_display" class="template">
             (@{total_rows})
          </span>
        </span>
        <table id="${id}">
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <span class="package-name">
                                <a href="/package_maintenance/packages?package=@{name}" moksha_url="dynamic">@{name}</a>
                            </span>
                        </td>
                    </tr>
                </tbody>
        </table>
        <div id="grid-controls">
            <div class="pager template" id="pager" type="more_link">
               <a href="@{more_link}" moksha_url="dynamic">View more packages &gt;</a>
            </div>
        </div>
        <div class="clear"></div>
    </div>