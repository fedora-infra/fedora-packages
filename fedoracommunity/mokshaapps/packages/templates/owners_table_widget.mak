
    <div class="list header-list">
        <table id="${id}">
            <thead>
              <th>Release</th>
              <th>Owner</th>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            @{release}
                        </td>
                        <td>
                            <span class='username'>
                                <a href="/people/?username=@{owner}" moksha_url="dynamic">@{owner}</a>
                            </span>
                        </td>

                    </tr>
                </tbody>
        </table>
    </div>