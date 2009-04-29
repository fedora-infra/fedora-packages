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
</div>
