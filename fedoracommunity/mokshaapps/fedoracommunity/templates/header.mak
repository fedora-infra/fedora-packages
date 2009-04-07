<html>

    <%def name="header()">
        <div id="head">
            ${tmpl_context.moksha_global_resources()}
            <h1><a href="/">Fedora Community</a></h1>
            <div id="toolbar">
                % if tmpl_context.auth('not_anonymous()'):
                    <div id="login-toolbar">
                        <form class="login_button" action="/logout">
                            Logged In: <span class="username"><a href="/profile">${tmpl_context.identity['person']['human_name']}</a></span>
                            <input type="submit"  class="button" value="Log Out" > </input>
                        </form>
                    </div>
                % else:
                    <div id="login-toolbar">
                        <form onSubmit="document.location='/login?came_from=' + document.location; return false;">
                            You are not logged in yet  <input type="submit"  value="Login" class="button"></input>
                        </form>
                    </div>
                % endif
            	<div id="search-toolbar">
                	<form action="/search/"
                	      onSubmit="moksha.csrf_add_form_field(this)">
                	    Search:
                	    <input type="text" name="search"
                	        onFocus="_fedora_community_on_search_focus(this)"
                	        onBlur="_fedora_community_on_search_blur(this)"
	               	        value="Type search terms here." ></input>

	                    <input class="button"
	                           type="submit"
	                           value="Search"
	                           ></input>
	                    <script type="text/javascript">
	                       function _fedora_community_on_search_focus(el) {

	                          if (el.value === "Type search terms here.")
	                              el.select();

	                          $(el).addClass("search-active");
	                       }

	                       function _fedora_community_on_search_blur(el) {
	                          $(el).removeClass("search-active");
	                       }

	                    </script>
        	        </form>
            	</div>
            </div>
        </div>
    </%def>
</html>
