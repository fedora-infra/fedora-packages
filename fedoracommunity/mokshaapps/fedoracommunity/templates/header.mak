<html>
    <%def name="resources()">
        ${tmpl_context.moksha_global_resources() | n}
    </%def>
    <%def name="header()">
        <div id="head">
            ${resources()}
            <div id="toolbar">
            	<div id="search-toolbar">
                	<form action="${tg.url('/search/')}"
                	      onSubmit="moksha.csrf_add_form_field(this)">
                	    Search:
                	    <input type="text" name="search"
                	        onFocus="_fedora_community_on_search_focus(this)"
                	        onBlur="_fedora_community_on_search_blur(this)"
	               	        value="Type search terms here." tabindex="1"></input>

	                    <input class="button"
	                           type="submit"
	                           value="Search"
	                           ></input>
	                    <script type="text/javascript">
	                       function _fedora_community_on_search_focus(el) {

	                          if (el.value === "Type search terms here.")
	                              el.value = "";

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
        <script type="text/javascript">
            moksha.update_marked_anchors($('a'));
        </script>
    </%def>
</html>
