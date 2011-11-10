<html>
    <%def name="resources()">
        ${tmpl_context.moksha_global_resources() | n}
    </%def>
    <%def name="header()">
        <div id="head">
            ${resources()}

       <div id="container">
       <div id="searchbar">
           <div class="container_24">
               <script type="text/javascript">
                   function do_search(form) {
                       moksha.goto(form.action + '/' + form.search['value']);
                       return False;
                   }
               </script>
               <form action="${tg.url('/s')}"
                     onSubmit="return do_search(this);">
                   <div class="grid_5" id="header-main">
		      <h1 style="font-size:large;">
                         <a href="/">
			    <span>Fedora</span> Packages
			 </a>
		      </h1>
                   </div>
                   <div class="grid_13">
                       <input type="text" name="search"/>
                   </div>
                   <div class="grid_2">
                       <input type="submit" value="Search"/>
                   </div>
               </form>
               <div class="clear"></div>
           </div>
       </div>
       </div>
    </%def>
</html>
