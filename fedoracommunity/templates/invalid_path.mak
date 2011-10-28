<%namespace file="fedoracommunity.mokshaapps.fedoracommunity.templates.header" import="*" />
<%namespace file="fedoracommunity.mokshaapps.fedoracommunity.templates.footer" import="*" />
<% from tg import flash %>
<html>
    <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
    <title>${title} - Fedora Community</title>

    <link href="/images/favicon.ico"
      type="image/vnd.microsoft.icon" rel="shortcut icon" />
    <link href="http://fedoraproject.org/favicon.ico"
      type="image/x-icon" rel="shortcut icon"/>

    <!--[if lt IE 7]>
    <style type="text/css">
        #wrapper
        {
            height: 100%;
            overflow: visible!important;
        }
    </style>
    <![endif]-->
</head>

<body id="chrome" class="home">
  <div id="wrapper">
   ${header()}
   <div id="main_app">
     <div id="main_nav">
         <div id="app-sidebar">
           <div id="navigation_sidebar" class="nav">
           </div>
         </div>
         <div id="content">
           <div class="left-content-column">
                <h1>${title}</h1>
                % if not login:
                    Sorry! Sometimes things break. The path <strong>"${invalid_path}"</strong> does not exist.  You have somehow
                    been directed to an invalid path.  If this was a link please
                    file a bug at
                    <a href="http://fedoracommunity.fedorahosted.org/">http://fedoracommunity.fedorahosted.org/</a>
                    with the path to the page that brought you here.
                    <br/><br/>
                    <a href="/" moksha_url="dynamic">Click here to go back to the Fedora Community front page.</a>

                % else:
                    <div class="login-error-message" style="margin-left: 0em;"><img alt="" src="${tg.url('/images/16_failured.png')}"/>&nbsp; The page you requested, <em>"${invalid_path}"</em> is available only to logged-in users. Please log in to view this page.</div>

                    ${tmpl_context.widget(came_from=invalid_path) | n}
                % endif
                <script type="text/javascript">
                    moksha.update_marked_anchors($('a'));
                </script>
             </div>
         </div>
       </div>
   </div>
  </div>
    ${footer()}
</body>
</html>
