<div id="${id}">
  <div class="info_content">
    <div class="hackergotchi"></div>
    <div class="info_details">
      <div class="info_basic_details">
        <h4>Basic Details</h4>

        <div><span class="label">Username</span> ${person['username']}</div>
        <div><span class="label">Member Since</span> ${person['created_display']}</div>
        <div><span class="label">Location</span> ${person['country_code']}</div>
        <div><span class="label">Timezone</span> ${person['timezone']}</div>
      </div>

      <div class="info_identity">
        <h4>Identity</h4>
        <div><span class="label">Public SSH Key</span> ${person['ssh_key']}</div>
        <div><span class="label">PGP Key</span> ${person['gpg_keyid']}</div>
      </div>

      <div class="info_contact">
        <h4>Contacting ${person['human_name']}</h4>
        <div><span class="label">IRC Nick</span> ${person['ircnick']}</div>
        <div><span class="label">Email</span> ${person['email']}</div>
        <div>
        <span class="label">Phone</span> ${person['telephone']}
        <div class="address">
          <span class="label">Postal Address</span>
          <span>
            % for l in person['postal_address'].split('\n'):
               <div>${l}</div>
            % endfor
          </span>
        </div>
       </div>
      </div>
    </div>
  </div>
  </div>
  <script type="text/javascript">
     % if compact:
        $(".label", $("${id}")).hide();
     % endif
  </script>
</div>