<% import tg %>
<div class="count-summary-dashboard">
  <div class="overlay"><div class="message"></div></div>
    <script type="text/javascript">
        function got_bug_stats(json) {
            $('#${w.id}_open_bugs').text(json.results.open);
            $('#${w.id}_num_new_this_week').text(json.results.new_this_week + ' new this week.');
            $('#${w.id}_num_closed_this_week').text(json.results.closed_this_week + ' closed this week.');
        }
        $(document).ready(function(){

fcomm.connector_load('bugzilla', 'get_bug_stats', {package: '${w.package}'}, got_bug_stats, $(".count-summary-dashboard .overlay"));
        });
    </script>
    <dl class="count-box">
       <dt class="count-header main-count-header">Open Bugs</dt>
       <a href="${w.bz_prefix}?${w.base_query_string}&${w.status_open_string}" target="_blank">
         <dd class="main-count-value" id="${w.id}_open_bugs">${w.num_open}</dd>
       </a>
       <dd><span class="count-header">New</span> <a
           href="${w.bz_prefix}?${w.base_query_string}&bug_status=NEW" target="_blank">
           <span id="${w.id}_num_new">${w.num_new}</span>
         </a>
       </dd>
       <a href="${w.bz_prefix}?${w.base_query_string}&${w.open_query_string}&${w.status_open_string}" target="_blank">
         <dd class="additional-info" colspan="2" id="${w.id}_num_new_this_week">
             ${w.num_new_this_week}
         </dd>
       </a>
    </dl>
    <dl class="count-box">
       <dt class="count-header main-count-header">Closed Bugs</dt>
       <a href="${w.bz_prefix}?${w.base_query_string}&${w.status_closed_string}" target="_blank">
         <dd class="main-count-value" id="${w.id}_num_closed">${w.num_closed}</dd>
       </a>
       <a href="${w.bz_prefix}?${w.base_query_string}&${w.closed_query_string}&${w.status_closed_string}" target="_blank">
         <dd class="additional-info" colspan="2" id="${w.id}_num_closed_this_week">
           ${w.num_closed_this_week}
         </dd>
       </a>
    </dl>
    <div class="action-box"><a class="action-header"
        target="_blank" href="https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora&version=${w.version}&component=${w.package}">Open A New Bug (Fedora)<br /> <img src="${tg.url('/images/action-box_add-button.png')}"></a>
    </div>
    <div class="action-box"><a class="action-header"
        target="_blank" href="https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora EPEL&version=${w.version}&component=${w.package}">Open A New Bug (EPEL)<br /> <img src="${tg.url('/images/action-box_add-button.png')}"></a>
    </div>
<div class="clear" />
</div>
