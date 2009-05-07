<div id="${id}" class="info-profile">
  <h2>${person['human_name']}</h2>
  <div class="compact_info_content">
    <div class="info_details">

      <div class="hackergotchi"><img src="${face}"/></div>

      <div class="col left_col">
        <div class="info_basic_details info_container">
            <h3>${person['username']}</h3>
            <p><strong>Location:</strong> ${person['country_code']}</p>
            <div class="timezone">
               <img src="/images/16_clock.png" />
               <p>
                  <span id="clock_${id}" class="clock" />
                  <span class="timezone_label">${person['timezone']}</span>
               </p>
            </div>
            <div class="timezone">
               <img src="/images/16_clock.png" />
               <p>
                  <span id="utc_clock_${id}" class="clock" /> 
                  <span class="timezone_label">UTC</span>
               </p>
            </div>
        </div>
      </div>

      <div class="col right_col">
        <div class="info_contact info_container">
          % if person.get('ircnick'):
          <p><img src="/images/16_chat.png" /> ${person['ircnick']}</p>
          % endif
          % if person.get('email'):
              <p><img src="/images/16_mail.png" /> <a href="mailto:${person['email']}">${person['email']}</a></p>
          % endif
          % if person.get('telephone'):
          <p><img src="/images/16_phone.png" />${person['telephone']}</p>
          % endif
        </div>
    </div>
  </div>
<div class="clear" />
  </div>
  <script type="text/javascript">
    $(document).ready(function(){
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
