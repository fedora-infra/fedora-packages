<div id="${id}">
    <div id="container">
       <div class="content-searchbox">
        <form action="/search">
            <span class="label">Search </span>
            <div class="content-searchinput">
                <input class="searchinput" type="text" name="search" value="${search}" />
            </div>
            <input class="button" type="submit" value="Search"/>
        </form>
      </div>

      <div id="content-column">
          ${applist_widget(category = 'content-column', layout = layout)}
      </div>
    </div>

    <div id="overlay">
        <div id="preloader"><img src="/toscawidgets/resources/moksha.widgets.layout.layout/static/loader.gif" alt="" /></div>
    </div>
</div>