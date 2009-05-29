    <div id="container">
       <div id="right-content-column">
          ${applist_widget(category = 'right-content-column-apps', layout = layout)}
          <div id="clear"></div>
       </div>

       <div id="left-content-column">
         % if tmpl_context.auth('Not(not_anonymous())'):
         <div id="banner-header">
<a href="/pages/tour">
<img id="main-banner" src="${tmpl_context.get_url('/images/banners/main-banner_tour-promo.png')}"/>
</a>
         </div>

         <h2>Welcome to Fedora Community!</h2>
         <p>
		 Fedora Community provides a window into the Fedora distribution,
		 leveraging the power of Fedora's Account System, Bodhi, Bugzilla,
		 Koji, and PackageDB into a single user-friendly website. Built
		 entirely with Free Software such as Moksha and TurboGears 2, Fedora
		 Community is designed to simplify Fedora workflows and bring
		 transparency to Fedora processes.
         </p>
         <p><strong><a href="https://admin.fedoraproject.org/accounts/user/new">Need an account?</a></strong></p>
         <br />

       % else:
         <h2>Welcome back, ${tmpl_context.identity['person']['human_name']}!</h2>
       % endif

       ${applist_widget(category = 'left-content-column-apps', layout = layout)}
     </div>
   </div>
