
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
                                <a href="/package_maintenance?package=@{name}" moksha_url="dynamic">@{name}</a>
                            </span>
                        </td>
                    </tr>
                </tbody>
        </table>
        <div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0">
            <div class="pager template" id="pager" type="more_link">
               <a href="@{more_link}?username=@{filters:index('username')}" moksha_url="dynamic">Goto users packages &gt;</a>
            </div>
        </div>
        <div id="grid-controls" if="visible_rows < total_rows && total_rows != 0">
            <div class="pager template" id="pager" type="more_link">
               <a href="@{more_link}?username=@{filters:index('username')}" moksha_url="dynamic">View more packages &gt;</a>
            </div>
        </div>
        <div class="clear"></div>
    </div>