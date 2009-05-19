<div id="${id}" class="info-profile">
  % if not profile:
      <script type="text/javascript">
          moksha.update_title("User: ${person['username']}", 2);
      </script>
  % endif
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
            <td>
<div class="timezone">
<span id="clock_${id}" class="clock"/>
<span class="timezone_label">${person['timezone']}</span>
</div>
<div class="timezone">
<span id="utc_clock_${id}" class="clock" />
<span class="timezone_label">UTC</span>
</div>
</td>
          </tr>
          </table>
        </div>
        <div class="info_identity info_container">
          <h4>Identity</h4>
          <table>
            % if person.get('ssh_key'):
              <tr>
                <th>Public SSH Key</th>
                <td>${person['ssh_key'][:7]}<div class="ssh_key" id="ssh_key_${id}"><div>${person['ssh_key']}</div></div></td>
              </tr>
            % endif
            % if person.get('gpg_keyid'):
            <tr>
              <th>PGP Key</th>
              <td><a href="http://pgp.mit.edu:11371/pks/lookup?search=0x${person['gpg_keyid']}&op=index&exact=on">${person['gpg_keyid']}</a></td>
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
            <td>${person['ircnick']}<br /><em class="note">irc.freenode.net</em></td>
          </tr>
          % endif
          % if person.get('email'):
          <tr>
            <th>Email</th>
              <td><a href="mailto:${person['email']}">${person['email']}</a></td>
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
