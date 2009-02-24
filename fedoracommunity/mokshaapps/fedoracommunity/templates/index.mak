<%namespace file="fedoracommunity.mokshaapps.fedoracommunity.templates.header" import="*" />
<%namespace file="fedoracommunity.mokshaapps.fedoracommunity.templates.footer" import="*" />

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
           ${tmpl_context.widget()}
        </div>
    </div>
    ${footer()}
</body>
</html>
