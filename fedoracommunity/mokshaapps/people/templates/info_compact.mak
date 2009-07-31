<div id="${id}" class="info-profile">
  % if not profile:
      <script type="text/javascript">
          moksha.update_title("User: ${person['username']}", 2);
      </script>
  % endif
  <div class="compact_info_content">
    <div class="info_details">

      <div class="hackergotchi"><img src="${tmpl_context.get_url(face)}"/></div>

      <div class="col left_col">
        <div class="info_basic_details info_container">
            <h3>${person['username']}</h3>
            % if not person.get('privacy'):
            <p><strong>Location:</strong> ${person['country_code']}</p>
            % if person.get('timezone') and person['timezone'] != 'UTC':
            <div class="timezone">
               <img src="${tmpl_context.get_url('/images/16_clock.png')}" />
               <p>
                  <span id="clock_${id}" class="clock" />
                  <span class="timezone_label">${person['timezone']}</span>
               </p>
            </div>
            % endif
            <div class="timezone">
               <img src="${tmpl_context.get_url('/images/16_clock.png')}" />
               <p>
                  <span id="utc_clock_${id}" class="clock" />
                  <span class="timezone_label">UTC</span>
               </p>
            </div>
            % endif # privacy
        </div>
      </div>

      <div class="col right_col">
        <div class="info_contact info_container">
          % if person.get('ircnick') and not person.get('privacy'):
          <p><img src="${tmpl_context.get_url('/images/16_chat.png')}" /> ${person['ircnick']} <br /><em class="note">irc.freenode.net</em></p>
          % endif
          % if person.get('email') and not person.get('privacy'):
              <p><img src="${tmpl_context.get_url('/images/16_mail.png')}" /> <a href="mailto:${person['email']}">${person['email']}</a></p>
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
          format: '%I:%M',
          utc: true,
          timeout: 60000
      });

    });
  </script>
</div>
