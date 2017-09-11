<%namespace file="fedoracommunity.templates.header" import="resources" />
<%namespace file="fedoracommunity.templates.footer" import="*" />

<html>
    <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
    <title>${title}</title>
		<link rel="stylesheet" type="text/css" href="https://apps.fedoraproject.org/global/fedora-bootstrap-1.0.2/fedora-bootstrap.css" media="all" />
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/fedora-packages.css')}" media="all" />

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
    ${resources()}
    <div id="wrapper">
        <div id="main_app" class="bodycontent">
    <div class="container">
           <!-- START Logo -->
           <div class="grid_8 prefix_9" id="header-search">
               <h1 class="text-xs-center py-3"><img src="${tg.url('/images/fedora_packages_logo.png')}" alt="Fedora Packages"></h1>
           </div>
           <!-- END Logo -->
           <div class="clear"></div>
    </div>
       <div id="searchbar" class="masthead py-3">
           <div class="container">
		<div class="grid_2">
		&nbsp;
               <!--
                   <a href="#" class="active">Search</a>
                   <a href="#">Browse</a>
	       -->
               	</div>
               <script type="text/javascript">
                   function do_search(form) {
                       var value = encodeURIComponent(encodeURIComponent(form.search['value']));
                       window.history.pushState({search: value}, '',
                                                form.action + '/' + value);
                       update_search_grid(value);
                       return False;
                   }
               </script>
               <form action="${tg.url('/s')}"
                      onSubmit="return do_search(this);">
                      <div class="input-group">
                        <input class ="form-control form-control-lg" type="text" name="search"
                               autofocus="autofocus"
                               value="${options['filters']['search']}" />
                         <span class="input-group-btn">
                           <input type="submit" value="Search" class="btn btn-primary btn-lg" />
                         </span>
                     </div>
               </form>
               <div class="clear"></div>
           </div>
       </div>
       <div id="search_grid" class="container front-search-results">
           ${tmpl_context.widget.display(**options) | n}
       </div>
</div>
        </div>
    </div>
    ${footer()}
</body>
</html>
