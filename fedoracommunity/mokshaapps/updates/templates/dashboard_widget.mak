<div class="list simple-border-list">
<ul id="${id}">
  <li>
  <a href="javascript:moksha.goto('/package_maintenance/updates/unpushed_updates');"><img src="/images/16_status-attention.png" alt="" /> ${pending} updates</a> are currently waiting to be pushed.  <a href="javascript:moksha.goto('/package_maintenance/updates/unpushed_updates');">More details ></a>
  </li>
  <li>
  <a href="javascript:moksha.goto('/package_maintenance/updates/testing_updates');"><img src="/images/16_status-attention.png" alt="" /> ${testing} updates</a> are currently in testing.  <a href="javascript:moksha.goto('/package_maintenance/updates/testing_updates');">More details ></a>
  </li>
  <li>
  <a href="javascript:moksha.goto('/package_maintenance/updates/stable_updates');"><img src="/images/16_status-success.png" alt ="" /> ${stable} updates</a> were pushed to stable this week.  <a href="javascript:moksha.goto('/package_maintenance/updates/stable_updates');">More details ></a>
  </li>
</ul>
</div>
