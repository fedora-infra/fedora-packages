<%namespace file="fedoracommunity.templates.header" import="*" />
<%namespace file="fedoracommunity.templates.footer" import="*" />
<% from tg import flash %>
<html>
    <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
    <title>${title}</title>
    <link rel="stylesheet" type="text/css" href="https://apps.fedoraproject.org/global/fedora-bootstrap-1.0.2/fedora-bootstrap.css" media="all" />
    <link rel="stylesheet" type="text/css" href="${tg.url('css/text.css')}" media="all" />

    <script type="text/javascript">
        moksha.update_title("${title}", 0);
    </script>
    <link href="/images/favicon.ico"
      type="image/vnd.microsoft.icon" rel="shortcut icon" />
    <link href="//fedoraproject.org/favicon.ico"
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
        <div id="head">
            ${tmpl_context.moksha_global_resources() | n}
        </div>
        <div id="main_app">
           % if flash.message:
             ${flash.message}
           % endif
           <div class="fedora-package-logo" />
           ${tmpl_context.widget(**options).display() | n}
        </div>
    </div>
</body>
</html>
