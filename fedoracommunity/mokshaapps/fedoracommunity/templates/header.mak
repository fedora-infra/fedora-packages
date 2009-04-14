<html>
    <%def name="header()">
        <div id="head">
            ${tmpl_context.moksha_global_resources()}
            <h1><a href="${tg.url('/')}">Fedora Community</a></h1>
            <div id="toolbar">
                % if tmpl_context.auth('not_anonymous()'):
                    <div id="login-toolbar">
                        <form class="login_button" action="${tg.url('/logout')}">
                            Logged In: <span class="username"><a href="${tg.url('/profile')}">${tmpl_context.identity['person']['human_name']}</a></span>
                            <input type="submit"  class="button" value="Log Out" > </input>
                        </form>
                    </div>
                % else:
                    <div id="login-toolbar">
                        <form
                            method="POST"
                            action="${tg.url('/login')}"
                            onSubmit="moksha.add_hidden_form_field(this, 'came_from', document.location, false)">
                            You are not logged in yet  <input type="submit"  value="Login" class="button"></input>
                            % if not came_from is UNDEFINED:
                                <input type="hidden" name="came_from" value="${came_from}"></input>
                            % endif
                        </form>
                    </div>
                % endif
            	<div id="search-toolbar">
                	<form action="${tg.url('/search/')}"
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
