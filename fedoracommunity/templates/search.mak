<%namespace file="fedoracommunity.templates.header" import="resources" />
<%namespace file="fedoracommunity.templates.footer" import="*" />
<% from tg import flash %>
<html>
    <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
    <title>${title}</title>

    <script type="text/javascript">
        moksha.update_title("${title}", 0);
    </script>
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
    ${resources()}
    <div id="wrapper">
        % if flash.message:
             ${flash.message}
        % endif
        <div id="main_app">
    <div id="container">
       <div class="container_24">
           <!-- START Logo -->
           <div class="grid_8 prefix_9" id="header-search">
               <h1><a href="/"><span id="logo">Fedora</span> Packages</a></h1>
           </div>
           <!-- END Logo -->
           <div class="clear"></div>
       </div>
       <div id="searchbar">
           <div class="container_24">
		<div class="grid_2">
		&nbsp;
               <!-- 
                   <a href="#" class="active">Search</a>
                   <a href="#">Browse</a>
	       -->
               	</div>
               <script type="text/javascript">
                   function do_search(form) {
                       window.history.pushState({search:form.search['value']}, '', 
                                                 form.action + '/' + form.search['value']);
                       update_search_grid(form.search['value']);
                       return False;
                   }
               </script>
               <form action="${tg.url('/s')}"
                      onSubmit="return do_search(this);">
                   <div class="grid_20">
                       <input type="text" name="search" value="${options['filters']['search']}" />
                   </div>
                   <div class="grid_2">
                       <input type="submit" value="Search"/>
                   </div>
               </form>
               <div class="clear"></div>
           </div>
       </div>
       <div id="search_grid" class="container_24">
           ${tmpl_context.widget.display(**options) | n}
       </div>
</div>
        </div>
    </div>
    ${footer()}
</body>
</html>
