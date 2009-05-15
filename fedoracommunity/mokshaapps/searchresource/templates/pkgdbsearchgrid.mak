<div class="list header-list">
   <table id="${id}">
    <thead>
      <th>Package Name</th>
      <th>Summary</th>
    </thead>
    <tbody class="rowtemplate">
        <tr>
            <td>
                <span class="package-name">
                    <a href="/package_maintenance/packages?package=@{parent_pkg}" moksha_url="dynamic">@{name}</a>
                </span>
            </td>
            <td>
                @{summary}
            </td>
        </tr>
    </tbody>
   </table>
   <div id="grid-controls">
        <div class="message template" id="info_display" >
           Viewing @{visible_rows} of @{total_rows} packages in search results
        </div>
        <div class="pager" id="pager" type="numeric" ></div>
   </div>
</div>
