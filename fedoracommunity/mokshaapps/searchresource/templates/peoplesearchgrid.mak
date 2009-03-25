<div>
   <table id="${id}">
    <thead>
      <th>Name</th>
      <th>Username</th>
    </thead>
    <tbody class="rowtemplate">
        <tr>
            <td>
                <span class="person-name"><a href="javascript:moksha.goto('/people/?username=@{username}')">@{human_name}</a></span>
            </td>
            <td>
                <span class="person-name"><a href="javascript:moksha.goto('/people/?username=@{username}')">@{username}</a></span>
            </td>
        </tr>
    </tbody>
   </table>
</div>