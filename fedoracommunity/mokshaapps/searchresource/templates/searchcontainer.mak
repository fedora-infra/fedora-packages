<% import tg %>
<div id="${id}">
    <div id="container">
       <div class="content-searchbox">
        <form action="${tg.url('/search')}"
              onSubmit="moksha.csrf_add_form_field(this);">
            <span class="label">Search </span>
            <div class="content-searchinput">
                <input class="searchinput" type="text" name="search" value="${search}" />
                % if tmpl_context.auth('not_anonymous()'):
                    <br />
                    <span><input type="checkbox" name="st" value="packages"  ${packages_checked}/>Packages</span>
                    <span><input type="checkbox" name="st" value="people"  ${people_checked}/>People</span>
                % endif
            </div>
            <input class="button" type="submit" value="Search"/>
        </form>

       </div>

       <div id="left-content-column">
        % if not search:
          % if tmpl_context.auth('not_anonymous()'):
            <p>Search results will appear below, package results listed first and people results listed second. You may also use the search bar at top of the screen to perform similar searches at any time.</p>
            <hr />
            <p><strong>Hint:</strong> The people search only searches usernames right now. A full-featured search indexer is currently in the works to improve this.</p>
            <p><strong>Hint:</strong> If you can't find a person you are looking for, try searching for a package they maintain or searching a portion of their irc nick which may be closer to their user name.</p>

          % else:
            <p>Search results will appear below, package results listed first and people results listed second. You may also use the search bar at top of the screen to perform similar searches at any time.</p>
          % endif
        % endif
          ${applist_widget(category = 'content-column', layout = layout)}
       </div>
    </div>
</div>
