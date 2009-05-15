<div class="list header-list">
   <table id="${id}">
    <thead>
      <th>Name</th>
      <th>Username</th>
    </thead>
    <tbody class="rowtemplate">
        <tr>
            <td>
                <span class="person-name"><a href="/people/?username=@{username}" moksha_url="dynamic">@{human_name}</a></span>
            </td>
            <td>
                <span class="person-name"><a href="/people/?username=@{username}" moksha_url="dynamic">@{username}</a></span>
            </td>
        </tr>
    </tbody>
   </table>
   <div id="grid-controls" if="total_rows == 0"">
        <div class="message template" id="info_display" >
           There are no people found who match the search terms
        </div>
   </div>
   <div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0"">
        <div class="message template" id="info_display" >
           Viewing @{visible_rows} of @{total_rows} people in search results
        </div>
   </div>
   <div id="grid-controls" if="visible_rows < total_rows">
        <div class="message template" id="info_display" >
           Viewing @{visible_rows} of @{total_rows} people in search results
        </div>
        <div class="pager" id="pager" type="numeric" ></div>
   </div>
</div>
