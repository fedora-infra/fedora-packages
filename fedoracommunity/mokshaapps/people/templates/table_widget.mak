
    <div class="list header-list">
        <table id="${id}">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Username</th>
                </tr>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <span class="person-name">
                                <a href="javascript:moksha.goto('/people/', {'user': '@{username}'});">@{human_name}</a>
                            </span>

                        <td>
                            <span class="person-name"><a href="javascript:moksha.goto('/people/', {'username': '@{username}'})">@{username}</a></span>&nbsp;
                        </td>
                </tbody>

        </table>
    </div>