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
             <div>
                <H1>${title}</H1>
                % if not login:
                    Sorry! Sometimes things break. The path <strong>"${invalid_path}"</strong> does not exist.  You have somehow
                    been directed to an invalid path.  If this was a link please
                    file a bug at
                    <a href="http://fedoracommunity.fedorahosted.org/">http://fedoracommunity.fedorahosted.org/</a>
                    with the path to the page that brought you here.
                    <br/><br/>
                    <a href="/" moksha_url="dynamic">Click here to go back to the Fedora Community front page.</a>

                % else:
                    The page you requested <strong>"${invalid_path}"</strong> requires that you be logged in to access it.
                    Please login to view this page.

                    ${tmpl_context.widget(came_from=invalid_path)}
                % endif
                <script type="text/javascript">
                    moksha.update_marked_anchors($('a'));
                </script>
             </div>
           </div>
         </div>
       </div>
   </div>
  </div>
    ${footer()}
</body>
</html>
