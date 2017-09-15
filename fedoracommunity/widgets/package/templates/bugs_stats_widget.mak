<% import tg %>
<div class="count-summary-dashboard col-sm-3 push-sm-9">
  <div class="overlay"><div class="message"></div></div>
    <script type="text/javascript">
        function got_bug_stats(json) {
            $('#${w.id}_open_bugs').text(json.results.open);
            $('#${w.id}_blockers').text(json.results.blockers);
            $('#${w.id}_blocker_url').attr('href', json.blocker_url);
        }
        $(document).ready(function(){

fcomm.connector_load('bugzilla', 'get_bug_stats', {package: '${w.package}'}, got_bug_stats, $(".count-summary-dashboard .overlay"));
        });
    </script>
    <div class="dropdown ml-2 mb-2">
      <button class="btn btn-primary btn-block dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        File a new Bug
      </button>
      <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
        <a class="dropdown-item" target="_blank" href="https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora&version=${w.version}&component=${w.package}">against Fedora</a>
        <a class="dropdown-item"   target="_blank" href="https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora EPEL&version=${w.epel_version}&component=${w.package}">against EPEL</a>
      </div>
    </div>
    <div class="count-box card ml-2">
      <div class="card-block">
       <h4 class="text-xs-center">Open Bugs</h4>
       <div class="bugcount">
       <a href="${w.bz_prefix}?${w.base_query_string}&${w.status_open_string}" target="_blank">
         <span class="main-count-value" id="${w.id}_open_bugs">${w.num_open}</span>
       </a>
     </div>
     </div>
    </div>
    <div class="count-box card ml-2">
      <div class="card-block">
       <h4 class="text-xs-center">Blocking Bugs</h4>
       <div class="bugcount">
         <a id="${w.id}_blocker_url" href="#" target="_blank">
         <span class="main-count-value" id="${w.id}_blockers">${w.num_open}</span>
       </a>
     </div>
     </div>
    </div>
<div class="clear"></div>
</div>
