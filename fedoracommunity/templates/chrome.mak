<!doctype html>
<%namespace file="fedoracommunity.templates.header" import="*" />
<%namespace file="fedoracommunity.templates.footer" import="*" />

<html>
    <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
    <title>${title}</title>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/960_24_col.css')}" media="all" />
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/text.css')}" media="all" />
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/application-chrome.css')}" media="all" />
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/myfedora-branding.css')}" media="all" />
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/fedora.css')}" media="all" />
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/reset.css')}" media="all" />

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
        ${header()}

        <div id="main_app">
           ${tmpl_context.widget.display(**options) | n}
        </div>
    </div>
    ${footer(options['kwds']['package_name'])}
</body>
</html>
