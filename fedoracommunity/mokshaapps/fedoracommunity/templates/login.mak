<%namespace file="fedoracommunity.mokshaapps.fedoracommunity.templates.header" import="*" />
<%namespace file="fedoracommunity.mokshaapps.fedoracommunity.templates.footer" import="*" />
<% from tg import flash %>
<html>
    <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
    <title>${title}</title>

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
        % if flash.message:
           <div class="login-error-message">
        <img src="/images/16_failured.png" alt="" />&nbsp; ${flash.message}
           </div>
        % endif
             <div id="banner-header" class="login-banner">
             <a href="/tour"><img src="/images/banners/paintain.png" alt="" /></a>
             <div id="login-box">
               ${tmpl_context.widget(**options)}
             </div>
             </div>
           </div>
         </div>
       </div>
   </div>
  </div>
    ${footer()}
</body>
</html>
