<% import tg %>
<div id="${id}">
    <div id="container">
       <div class="container_24">
           <!-- START Logo -->
           <div class="grid_8 prefix_9" id="header">
               <a href="/"><h1><span id="logo">Fedora</span> Packages</h1></a>
           </div>
           <!-- END Logo -->
           <div class="clear"></div>
       </div>
       <div id="searchbar">
           <script type="text/javascript">
               $("#toolbar").hide();
           </script>
           <div class="container_24">
               <div class="grid_4">
                   <a href="#" class="active">Search</a>
                   <a href="#">Browse</a>
               </div>
               <form action="${tg.url('/s')}"
                      onSubmit="window.history.pushState({}, '', this.action + '/' + this.search['value']); return False;">
                   <div class="grid_18">
                       <input type="text" name="search" value="${search}" />
                   </div>
                   <div class="grid_2">
                       <input type="submit" value="Search"/>
                   </div>
               </form>
               <div class="clear"></div>
           </div>
       </div>
       <div id="left-content-column" class="container_24">
          ${applist_widget(category = 'content-column', layout = layout)}
       </div>
    </div>
</div>
