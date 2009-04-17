<div class="count-summary-dashboard">
  <div class="overlay"><div class="message"></div></div>
    <script type="text/javascript">
        function got_bug_stats(json) {
            $('#${id}_open_bugs').text(json.results.open);
            $('#${id}_num_new').text(json.results.new);
            $('#${id}_num_new_this_week').text(json.results.new_this_week + ' new this week.');
            $('#${id}_num_closed').text(json.results.closed);
            $('#${id}_num_closed_this_week').text(json.results.closed_this_week + ' closed this week.');
        }
        $(document).ready(function(){
            moksha.connector_load('bugzilla', 'call/${filters}', {}, got_bug_stats, $(".count-summary-dashboard .overlay"));
        });
    </script>
    <dl class="count-box">
       <dt class="count-header main-count-header">Open Bugs</dt>
       <a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&product=${product}&component=${package}&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED" target="_blank"><dd class="main-count-value" id="${id}_open_bugs">${num_open}</dd></a>
        <dd><span class="count-header">New</span> <a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&product=${product}&component=${package}&bug_status=NEW" target="_blank"><span id="${id}_num_new">${num_new}</span></a></dd>
        <dd class="additional-info" colspan="2" id="${id}_num_new_this_week">${num_new_this_week}</dd>
    </dl>
    <dl class="count-box">
       <dt class="count-header main-count-header">Closed Bugs</dt>
       <a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&product=${product}&component=${package}&bug_status=CLOSED" target="_blank"><dd class="main-count-value" id="${id}_num_closed">${num_closed}</dd></a>
        <dd class="additional-info" colspan="2" id="${id}_num_closed_this_week">${num_closed_this_week}</dd>
    </dl>
    <div class="action-box"><a class="action-header" href="https://bugzilla.redhat.com/enter_bug.cgi?product=${product}&version=${version}&component=${package}">Open A New Bug<br /> <img src="/images/action-box_add-button.png"></a>
    </div>
<div class="clear" />
</div>
