<div id="${id}">
  <div class="info_content">
    <div class="hackergotchi"></div>
    <div class="info_details">
      <div class="info_basic_details">
        <h4>Basic Details</h4>
        <table>
        <tr>
          <th>Username</th>
          <td>${person['username']}</td>
        </tr><tr>
          <th>Member Since</th>
          <td>${person['created_display']}</td>
        </tr><tr>
          <th>Location</th>
          <td>${person['country_code']}</td>
        </tr><tr>
          <th>Timezone</th>
          <td>${person['timezone']}</td>
        </tr>
        </table>
      </div>

      <div class="info_identity">
        <h4>Identity</h4>
	<table>
        <tr>
          <th>Public SSH Key</th> 
          <td>${person['ssh_key']}</td>
        </tr><tr>
          <th>PGP Key</th>
          <td>${person['gpg_keyid']}</td>
        </tr>
        </table>
      </div>

      <div class="info_contact">
        <h4>Contacting ${person['human_name']}</h4>
        <table>
        <tr>
          <th>IRC Nick</th>
          <td>${person['ircnick']}</td>
        </tr><tr>
          <th>Email</th>
          <td>${person['email']}</td>
        </tr><tr>
          <th>Phone</th>
          <td>${person['telephone']}</td>
        </tr><tr>
          <th>Postal Address</th>
          <td><span>
            % for l in person['postal_address'].split('\n'):
               <div>${l}</div>
            % endfor
          </span>
          </td>
        </tr>
        </table>
      </div>
    </div>
  </div>
  <script type="text/javascript">
     % if compact:
        $(".label", $("${id}")).hide();
     % endif
  </script>
</div>
