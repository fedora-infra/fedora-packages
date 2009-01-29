<div>
    <div id="container">
      <div id="banner-header">
         <img width="600" src="${tmpl_context.get_url('/images/fedora_intro_banner1.png')}">
      </div>
      <div>
       <div id="right-content-column">
          ${applist_widget(category = 'right-content-column', layout = layout)}
       </div>
       
       <div id="left-content-column">
          % if tmpl_context.auth('Not(not_anonymous())'):
          <H2>Welcome to Fedora Community!</H2>
          FIXME: This is not correct wording. Fedora Community is a place where 
          Fedora package maintainers can collaborate on building and maintaining
          their packages.  Logging into your Fedora account in Fedora Community
          allows you to keep up with your packages and to keep track of your
          friends' packages as well.<br/>
          <strong><a href="">Need an account?</a>
          % endif
          ${applist_widget(category = 'left-content-column', layout = layout)}
       </div>
     </div>
    </div>
    
    <div id="overlay">
        <div id="preloader"><img src="/toscawidgets/resources/moksha.widgets.layout.layout/static/loader.gif" alt="" /></div>
    </div>
</div>