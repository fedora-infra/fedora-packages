<div class="list header-list">
    <script type="text/javascript">
        function got_bug_stats(json) {
            $('#${id}_open_bugs').text(json.results[0]);
            $('#${id}_num_new').text(json.results[1]);
            $('#${id}_num_new_this_week').text(json.results[2] + ' new this week.');
            $('#${id}_num_closed').text(json.results[3]);
            $('#${id}_num_closed_this_week').text(json.results[4] + ' closed this week.');
        }
        $(document).ready(function(){
            console.log('making request');
            $.getJSON('/moksha_connector/bugzilla/call/${filters}', {}, got_bug_stats);
        });
    </script>
    <table id="${id}">
        <tbody>
                <tr>
                    <td>
                        Open Bugs: <div id="${id}_open_bugs">${num_open}</div>
                        New: <div id="${id}_num_new">${num_new}</div>
                        <div id="${id}_num_new_this_week">${num_new_this_week}</div>
                    </td>
                    <td>
                        Closed Bugs: <div id="${id}_num_closed">${num_closed}</div>
                        <div id="${id}_num_closed_this_week">${num_closed_this_week}</div>
                    </td>
                    <td>
                        <a href="https://bugzilla.redhat.com/enter_bug.cgi?product=${product}&version=${version}&component=${component}">Open A New Bug</a>
                    </td>
                </tr>
            </tbody>
    </table>
</div>
