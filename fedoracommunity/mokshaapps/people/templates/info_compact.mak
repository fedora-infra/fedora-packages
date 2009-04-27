<div id="${id}" class="info-profile">
  <h2>${person['human_name']}</h2>
  <div class="compact_info_content">
    <div class="info_details">

      <div class="hackergotchi"><img src="${face}"/></div>

      <div class="col left_col">
        <div class="info_basic_details info_container">
          <table>
          <tr>
            <td colspan="2">${person['username']}</td>
          </tr><tr>
            <td colspan="2">${person['country_code']}</td>
          </tr><tr>
            <td>
              <img src="/images/16_clock.png" />
            </td>
            <td><span><span id="clock_${id}" class="clock"/></span><br />${person['timezone']}</td>
          </tr>
          <tr>
            <td>
              &nbsp;
            </td>
            <td><span><span id="utc_clock_${id}" class="clock" /></span><br />UTC</td>
          </tr>
          </table>
        </div>
      </div>

      <div class="col right_col">
        <div class="info_contact info_container">
          <table>
          % if person.get('ircnick'):
          <tr>
            <td><img src="/images/16_chat.png" /></td><td>${person['ircnick']}</td>
          </tr>
          % endif
          % if person.get('email'):
          <tr>
            <td><img src="/images/16_mail.png" /><td>${person['email']}</td>
          </tr>
          % endif
          % if person.get('telephone'):
          <tr>
            <td><img src="/images/16_phone.png" /><td>${person['telephone']}</td>
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
      $("#clock_${id}").jclock({
          timeNotation: '12h',
          am_pm: true,
          utc_offset: ${utc_offset},
      });

      $("#utc_clock_${id}").jclock({
          timeNotation: '12h',
          am_pm: true,
          utc: true,
      });

    });
  </script>
</div>
