    <div id="container">
       <div id="right-content-column">
          ${applist_widget(category = 'right-content-column-apps', layout = layout)}
          <div id="clear"></div>
       </div>

       <div id="left-content-column">
         % if tmpl_context.auth('Not(not_anonymous())'):
         <div id="banner-header">
<a href="/pages/tour">
<img src="${tmpl_context.get_url('/images/banners/main-banner_tour-promo.png')}"/>
</a>
         </div>

         <h2>Welcome to Fedora Community!</h2>
         <p>
           FIXME: This is not correct wording. Fedora Community is a place where
           Fedora package maintainers can collaborate on building and maintaining
           their packages.  Logging into your Fedora account in Fedora Community
           allows you to keep up with your packages and to keep track of your
           friends&rsquo; packages as well. 
         </p>
         <p><strong><a href="https://admin.fedoraproject.org/accounts/user/new">Need an account?</a></strong></p>
         <br />

       % else:
         <h2>Welcome back, ${tmpl_context.identity['person']['human_name']}!</h2>
       % endif

       ${applist_widget(category = 'left-content-column-apps', layout = layout)}
     </div>
   </div>
