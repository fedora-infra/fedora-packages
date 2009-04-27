<div id="${id}" class="info-profile">
  <h2>${person['human_name']}</h2>
  <div class="info_content">
    <div class="info_details">

      <div class="hackergotchi"><img src="${face}"/></div>

      <div class="col left_col">
        <div class="info_basic_details info_container">
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
            <td>${person['timezone']} <span id="clock_${id}" class="clock"/><br/>
            UTC <span id="utc_clock_${id}" class="clock" /></td>
          </tr>
          </table>
        </div>
        <div class="info_identity info_container">
          <h4>Identity</h4>
          <table>
            % if person.get('ssh_key'):
              <tr>
                <th>Public SSH Key</th>
                <td>${person['ssh_key'][:7]}<div id="ssh_key_${id}"><div>${person['ssh_key']}</div></div></td>
              </tr>
            % endif
            % if person.get('gpg_keyid'):
            <tr>
              <th>PGP Key</th>
              <td>${person['gpg_keyid']}</td>
            </tr>
            % endif
          </table>
        </div>
      </div>

      <div class="col right_col">
        <div class="info_contact info_container">
          <h4>Contacting ${person['human_name']}</h4>
          <table>
          % if person.get('ircnick'):
          <tr>
            <th>IRC Nick</th>
            <td>${person['ircnick']}</td>
          </tr>
          % endif
          % if person.get('email'):
          <tr>
            <th>Email</th>
            <td>${person['email']}</td>
          </tr>
          % endif
          % if person.get('telephone'):
          <tr>
            <th>Phone</th>
            <td>${person['telephone']}</td>
          </tr>
          % endif
          % if person.get('postal_address'):
          <tr>
            <th>Postal Address</th>
            <td class="address">
                  % for l in person['postal_address'].split('\n'):
                      ${l}<br />
                  % endfor
            </td>
          </tr>
          % endif
          </table>
        </div>
    </div>
  </div>
<div class="clear" />
  </div>

  <script type="text/javascript">
    $(document).ready(function(){
     % if person.get('ssh_key'):
      $("#ssh_key_${id}").expander({
            slicePoint: 0,
            widow: 1,
            userCollapse: true,
            expandText: 'Show full key <img src="/images/arrow_down.png">',
            userCollapseText: 'Hide full key <img src="/images/arrow_up.png">',
      });
     % endif

      $("#clock_${id}").jclock({
          format: '%I:%M %p',
          utc_offset: ${utc_offset},
          timeout: 60000
      });

      $("#utc_clock_${id}").jclock({
          format: '%I:%M %p',
          utc: true,
          timeout: 60000
      });
     });

  </script>
</div>
