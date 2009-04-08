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
                    <a href="javascript:moksha.goto('/package_maintenance/packages',{'package':'@{name}'})">@{name}</a>
                </span>
            </td>
            <td>
                @{summary}
            </td>
        </tr>
    </tbody>
   </table>
</div>
