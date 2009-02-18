
        <div class="list header-list">
        <table id="${id}">
            <thead>
                <tr>
                    <th><a href="#nvr">Package</a></th>
                    <th>Build Age</th>
                    <th>Date Pushed</th>
                    <th>Release(s)</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <span class="package-name">
                                @{package_name}
                            </span>
                            <div>@{version}</div>
                        </td>
                        <td>n/a</td>
                        <td>@{completion_time}</td>
                        <td>@{release_label}</td>
                        <td><span>@{status}</span>
                        <div><img src="/images/16_karma-@{karma_level}.png" />@{karma_str} karma</div>
                        </td>
                    </tr>
                </tbody>

        </table>
