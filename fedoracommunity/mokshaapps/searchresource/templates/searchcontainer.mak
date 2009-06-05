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
            Enter a search to search for Fedora packages and people.  Results will
            appear bellow with the package search first and people search second.
            You may also use the search bar at top to perform similar searches
            at any time.

            Hint: The people search can only search on user names right now.  It does
            not take into account full names except for ranking purposes so it may
            be hard to find someone if their user name bears no similarity to
            their actual name.  A full featured search indexer is being worked on
            which will greatly expand the relevance of the results.  If you
            can't find a person you are looking for try searching for a package
            they maintain or searching a portion of their irc nick which may be
            closer to their user name.

          % else:
            Enter a search to search for Fedora packages. You must be logged in to
            search for people.  Results will appear bellow ranked by relevance.
            You may also use the search bar at top to perform similar searches
            at any time.
          % endif
        % endif
          ${applist_widget(category = 'content-column', layout = layout)}
       </div>
    </div>
</div>
