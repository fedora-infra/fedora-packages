
        <div class="list header-list">
        <table id="${id}">
            <thead>
                <tr>
                    <th><a href="#nvr">Package</a></th>
                    <th><a href="#owner_name">Built By</a></th>
                    <th>Build Time</th>
                    <th>Finished</th>
                    <th><a href="#state">Status</a></th>
                </tr>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <span class="package-name">
                                <a href="http://localhost/koji/buildinfo?buildID=@{build_id}" target="_blank">@{package_name}</a>
                            </span>
                            <div>@{version}</div>
                        </td>
                        <td>
                            <span class="person-name"><a href="/people/name/@{owner_name}/builds">@{owner_name}</a></span>
                        </td>
                        <td>@{completion_time_display:index("elapsed")}
                        </td>
                        <td>@{completion_time_display:index("when")}
                            <div>
                               @{completion_time_display:index("time")}
                            </div>
                        </td>

                        <td><img src="/images/16_build_state_@{state}.png" /></td>
                        <td id="@{release_id}">
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td colspan="7"
                            id="@{message_id}"
                            class="message_row">
                        </td>
                    </tr>
                </tbody>

        </table>
