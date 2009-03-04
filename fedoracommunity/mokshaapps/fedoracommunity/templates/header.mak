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
                            <input type="submit"  class="button" value="Log Out" />
                        </form>
                    </div>
                % else:
                    <div id="login-toolbar">
                        <form onSubmit="document.location='/login?came_from=' + document.location; return false;">
                            You are not logged in yet  <input type="submit"  value="Login" class="button"/>
                        </form>
                    </div>
                % endif
            	<div id="search-toolbar">
                	<form action="/search/">
                	    Search:
                	    <input type="text" name="data_key"
                	        onFocus="this.select();"
	               	        value="Type search terms here." />

	                    <input class="button" type="submit" value="Search" />
        	        </form>
            	</div>
            </div>
        </div>
    </%def>
</html>
