   <div class="list header-list">
        <table id="${id}">
            <thead>
               <th>Group</th>
               <th>Type</th>
            </thead>
            <tbody class="rowtemplate">
                <tr>
                    <td>
                        <span class="group-name">
                        <a href="https://admin.fedoraproject.org/accounts/group/view/@{name}">@{display_name} <img src="${tmpl_context.get_url('/images/16-fas.png')}"/></a>
                        </span>
                    </td>
                    <td>
                        @{group_type}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
