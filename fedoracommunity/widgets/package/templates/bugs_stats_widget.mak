<% import tg %>
<div class="count-summary-dashboard">
  <div class="overlay"><div class="message"></div></div>
    <script type="text/javascript">
        function got_bug_stats(json) {
            $('#${w.id}_open_bugs').text(json.results.open);
            $('#${w.id}_num_new').text(json.results.new);
            $('#${w.id}_num_new_this_week').text(json.results.new_this_week + ' new this week.');
            $('#${w.id}_num_closed').text(json.results.closed);
            $('#${w.id}_num_closed_this_week').text(json.results.closed_this_week + ' closed this week.');
        }
        $(document).ready(function(){

moksha.connector_load('bugzilla', 'get_bug_stats', {package: '${w.package}'}, got_bug_stats, $(".count-summary-dashboard .overlay"));
        });
    </script>
    <dl class="count-box">
       <dt class="count-header main-count-header">Open Bugs</dt>
       <a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&product=${w.product}&component=${w.package}&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED" target="_blank"><dd class="main-count-value" id="${w.id}_open_bugs">${w.num_open}</dd></a>
        <dd><span class="count-header">New</span> <a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&product=${w.product}&component=${w.package}&bug_status=NEW" target="_blank"><span id="${w.id}_num_new">${w.num_new}</span></a></dd>
        <dd class="additional-info" colspan="2" id="${w.id}_num_new_this_week">${w.num_new_this_week}</dd>
    </dl>
    <dl class="count-box">
       <dt class="count-header main-count-header">Closed Bugs</dt>
       <a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&product=${w.product}&component=${w.package}&bug_status=CLOSED" target="_blank"><dd class="main-count-value" id="${w.id}_num_closed">${w.num_closed}</dd></a>
        <dd class="additional-info" colspan="2" id="${w.id}_num_closed_this_week">${w.num_closed_this_week}</dd>
    </dl>
    <div class="action-box"><a class="action-header" href="https://bugzilla.redhat.com/enter_bug.cgi?product=${w.product}&version=${w.version}&component=${w.package}">Open A New Bug<br /> <img src="${tg.url('/images/action-box_add-button.png')}"></a>
    </div>
<div class="clear" />
</div>
