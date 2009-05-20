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
                    <a href="/package_maintenance?package=@{parent_pkg}" moksha_url="dynamic">@{name}</a>
                </span>
            </td>
            <td>
                @{summary}
            </td>
        </tr>
    </tbody>
   </table>
   <div id="grid-controls" if="total_rows == 0"">
        <div class="message template" id="info_display" >
           There are no packages found which match the search terms
        </div>
   </div>
   <div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0"">
        <div class="message template" id="info_display" >
           Viewing @{visible_rows} of @{total_rows} packafe in search results
        </div>
   </div>
   <div id="grid-controls" if="visible_rows < total_rows">
        <div class="message template" id="info_display" >
           Viewing @{visible_rows} of @{total_rows} packages in search results
        </div>
        <div class="pager" id="pager" type="numeric" ></div>
   </div>
</div>
