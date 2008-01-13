/*
 * Copyright © 2007  Red Hat, Inc.
 *
 * This copyrighted material is made available to anyone wishing to use, modify,
 * copy, or redistribute it subject to the terms and conditions of the GNU
 * General Public License v.2.  This program is distributed in the hope that it
 * will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
 * implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.  You should have
 * received a copy of the GNU General Public License along with this program;
 * if not, write to the Free Software Foundation, Inc., 51 Franklin Street,
 * Fifth Floor, Boston, MA 02110-1301, USA. Any Red Hat trademarks that are
 * incorporated in the source code or documentation are not subject to the GNU
 * General Public License and may only be used or replicated with the express
 * permission of Red Hat, Inc.
 *
 * Red Hat Author(s): Toshio Kuratomi <tkuratom@redhat.com>
 */

/*
 * ================
 * Fedora Namespace
 * ================
 */
if (typeof(fedora) == 'undefined') {
    fedora = {};
} else if (typeof(fedora) != "object") {
    throw new Error("fedora already exists and is not a module");
}

/*
 * -----------
 * OOP Support
 * -----------
 */

/*
 * Function.inherits
 * =================
 *
 * Add an inherits() method to Functions so we can easily specify inheritance
 * between two objects.
 * 
 * Caveats:
 * If a method is defined in the constructor rather than the prototype then
 * no derived objects can override that method in their prototype, only in
 * their constructor.
 *
 * Example:
 *  Drink = function (color, volume) {
 *      this.color = color;
 *      this.volume = volume;
 *  };
 *
 *  Drink.prototype.sip = function () {
 *      this.volume -= 2;
 *      if (this.volume <= 0) {
 *          this.volume = 0;
 *      }
 *  };
 *
 *  Coffee = function(volume, caffeine) {
 *      Coffee.base.call(this, "brown", volume);
 *      this.caffeine = caffeine;
 *  };
 *  Coffee.inherits(Drink);
 * 
 *  Coffee.prototype.sip = function () {
 *      this.caffeine -= (2/this.volume) * this.caffeine;
 *      Coffee.basePrototype.sip.call(this);
 *      if (this.caffeine <= 0 || this.volume == 0) {
 *          this.caffeine = 0;
 *      }
 *  };
 * 
 *  DepthCharge = function(volume, shots){
 *      DepthCharge.base.call(this, volume, shots * 10);
 *      this.shots = shots;
 *      this.consumed_shots = 0;
 *  }
 *  DepthCharge.inherits(Coffee);
 * 
 *  DepthCharge.prototype.sip= function() {
 *      DepthCharge.basePrototype.sip.call(this);
 *      this.consumed_shots =  this.shots - Math.ceil(this.caffeine/10)
 *  }
 * 
 *  print ("Drink a cup of Coffee");
 *  t = new Coffee(8, 4);
 *  print (t.constructor);
 *  print ("Color:", t.color, "Volume:", t.volume,"Caffeine:",  t.caffeine);
 *  for (i = 0; i < 4; i++) {
 *      t.sip();
 *      print ("Volume:", t.volume, "Caffeine:", t.caffeine);
 *  }
 * 
 *  print ("\nDrink a Depth Charge with 10 shots of espresso");
 *  t = new DepthCharge(8, 10);
 *  print (t.constructor);
 *  print ("Color:", t.color, "Volume:", t.volume,"Caffeine:",  t.caffeine, "Shots of Espresso Drunk:", t.consumed_shots);
 *  for (i = 0; i < 4; i++) {
 *      t.sip();
 *  print ("Volume:", t.volume,"Caffeine:",  t.caffeine, "Shots of Espresso Drunk:", t.consumed_shots);
 *  }
 */

Function.prototype.inherits = function(superclass) {
    /* Create an intermediate prototype so additions to the subclass don't
     * modify the superclass's prototype.
     */
    Constructor = function () {};
    Constructor.prototype = superclass.prototype;
    this.prototype = new Constructor();
    this.prototype.constructor = this;
    this.base = superclass;
    this.basePrototype = superclass.prototype;
};

/*
 * ------------------
 * String Enhancement
 * ------------------
 */

/*
 * String.strip
 * ============
 * Javascript doesn't provide a strip function so implement one
 */
String.prototype.strip = String.prototype.strip || function(chars) {
    chars = chars ? chars : "\\s";
    return this.replace(new RegExp("^["+chars+"]*|["+chars+"]*$", "g"), "");
}

/*
 * ---------------------------
 * Functional Programming Aids
 * ---------------------------
 */
if (!fedora.functools) {
    fedora.functools = {};
} else if (typeof(fedora.functools) != "object") {
    throw new Error("fedora.functools already exists and is not a module");
}

/*
 * functools.partial
 * ==================
 * Return a partially applied function
 *
 * Example::
 *  function color_text (text, newcolor) { [...] }
 *  warning = partial(color_text("#FF000");
 *  warning('Color me red');
 */
fedora.functools.partial = function (fn) {
    var args = Array.prototype.slice.call(arguments, 1);
    return function(){
        args.push.apply( args, arguments );
        return fn.apply( fn, args );
    };
}

/*
 * ----------
 * Exceptions
 * ----------
 */

/*
 * NotImplementedError
 * ===================
 * Throw when a method is merely a placeholder.
 */
fedora.NotImplementedError = function(msg) {
    NotImplementedError.base.call(this, msg);
    this.message = msg;
    this.name = "NotImplementedError";
}
fedora.NotImplementedError.inherits(Error);

/*
 * -------
 * Widgets
 * -------
 *
 * Widgets have several pieces.  Part of it resides on the server in the
 * controller and template classes.  When a widget requires javascript,
 * however, it is best if we can place it in a statically served file.
 *
 * To make things with as little confusion as possible we've adopted a
 * convention of naming the object that names the widget in the
 * template/controller the same as the javascript code.  In the template, we
 * use the widget from the template to write out an initial piece of html and
 * the javascript function to define an object that can interact with the
 * widget later.
 *
 * We could create the whole widget with javascript to avoid duplicating code
 * but that fails to display anything on browsers without javascript enabled.
 */
if (!fedora.widgets) {
    fedora.widgets = {};
} else if (typeof(fedora.widgets) != "object") {
    throw new Error("fedora.widgets already exists and is not a module");
}

/* 
 * Widget
 * ======
 * Base class for all Fedora created Widgets.
 *
 * All Fedora created widgets should inherit from FedoraWidget and have the
 * base functionality expressed here.
 *
 * Arguments:
 * :widgetId: A unique identifier for this instance of the widget.
 */
fedora.widgets.Widget = function (widgetId) {
    if (!widgetId) {
        throw new TypeError("Widget constructor must be sent an ID");
    }
    this.widgetId = widgetId;
}

/* 
 * Widget.busy
 * -----------
 * Show that a widget is doing something.
 *
 * Widgets can choose to display a spinner on themselves, disable their
 * action areas, send a message to the toplevel of the app to
 * display a spinner, or perform other actions to show that they are doing
 * something.
 *
 * The default action is to signal that the widget is processing.  Widgets
 * that want to do more should override this method like this::
 *  fedora.widgets.Example.prototype.busy = function() {
 *    fedora.widgets.Example.basePrototype.busy.call();
 *    jQuery("#" + this.widgetId + " #throbber").show();
 *    this.throbber.start();
 */
fedora.widgets.Widget.prototype.busy = function () {
    /* Signal that the widget is processing */
    w=jQuery('#' + this.widgetId).trigger("busy");
}

/*
 * Widget.unbusy
 * -------------
 * Widgets should reverse the effects of busy here.
 *
 * This is a virtual function and must be implemented by the subclass.
 */
fedora.widgets.Widget.prototype.unbusy = function () {
    /* Signal that the widget is done processing */
    w=jQuery('#' + this.widgetId).trigger("unbusy");
}

/*
 * Widget.show
 * -----------
 * Display a created and rendered widget.
 */
fedora.widgets.Widget.prototype.show = function () {
    jQuery('#' + this.widgetId).show();
}

/*
 * Widget.hide
 * -----------
 * Hide a created and rendered widget.
 */
fedora.widgets.Widget.prototype.hide = function () {
    jQuery('#' + this.widgetId).hide();
}

/*
 * Widget.render
 * -------------
 * Create the DOM to displays the widget.
 *
 * The render() function creates the DOM to display the widget.  It returns
 * the DOM object to the caller.  If the target argument is given, then the
 * DOM node with that id is replaced with the new widget as well.
 *
 * This is a virtual function and must be implemented by the subclass.
 * Example::
 *  fedora.widgets.Example.prototype.render = function(target) {
 *      var html = '<div id= '<div id="' + this.widgetId + '">\n'
 *          + 'Example Widget.</div>\n';
 *      if (target) {
 *          jQuery('#' + target).replaceWith(html);
 *      }
 *      return jQuery(html);
 *
 * Arguments:
 * :target: Target DOM id to replace with the widget
 *
 * Returns: DOM object displaying the widget
 */
fedora.widgets.Widget.prototype.render = function (target) {
    throw new fedora.NotImplementedError(
            'Widget needs to define a render() method.');
}

/*
 * Throbber
 * ========
 * A widget to display a busy throbber
 * 
 * This is your typical widget to show that the page is busy doing something.
 * Useful in AJAX applications to show that there is something going on.
 *
 * There are two ways of using the throbber.
 *
 * 1) You can create and destroy it on demand.   This is useful when you want
 * to show that an individual UI element (like an entry box) is presently busy
 * and cannot take more information.
 *
 * 2) You can create it and display it at a single place in your page.  When
 * something is busy, you tell it to spin and then tell it to stop when the
 * event stops.  This is useful for telling someone that the app is busy
 * working on something but they can still enter data.
 *
 * Example for usage 1::
 *  widget.prototype.busy = function () {
 *      this.throbber = new fedora.widgets.Throbber('throbber1',
 *          'INACTIVEIMGURL', ['IMGURL1', 'IMGURL2']);
 *      var entry = jQuery('input#entry_to_busy')
 *          .setAttribute('disabled',
 *          'true').appendChild(this.throbber.render());
 *      var pos = elementPosition(elem);
 *      this.throbber.style.position = 'absolute';
 *      setElementPosition(this.throbber, pos);
 *      this.throbber.show();
 *      this.throbber.start();
 *  }
 *  widget.prototype.unbusy = function () {
 *      this.throbber.hide();
 *      this.throbber.stop();
 *      var throbber = jQuery('#' + this.throbber.widgetId);
 *      removeElement(throbber);
 *      delete(throbber);
 *  }
 *
 * Example for usage 2::
 *  widget = function(widgetId) {
 *      this.widgetId = widgetId;
 *      this.throbber = new fedora.widgets.Throbber('globalThrobber',
 *          'INACTIVEIMGURL', [IMGURL1, IMGURL2]);
 *      jQuery('#' + widgetId).bind('busy', function() {this.throbber.start();})
 *          .bind('unbusy', function() {this.throbber.stop();} );
 *  }
 *      
 *  widget.prototype.render = function (target) {
 *      var html = '<div class="FedoraWidget widget" id="generic">\n'
 *          + this.throbber.render() + '</div>';
 *  }
 *
 * Arguments:
 * :widgetId: Id of the widget
 * :inactiveImage: URL to an image for the throbber when inactive
 * :frames: List of URL's to use to animate the throbber
 * :timeout: Delay between displaying frames of the throbber
 */
fedora.widgets.Throbber = function(widgetId, inactiveImage, frames, timeout) {
    fedora.widgets.Throbber.base.call(this, widgetId);
    this.inactiveImage = inactiveImage;
    this.frames = frames ||
        ['https://admin.fedoraproject.org/pkgdb/static/images/spinner/01.png',
        'https://admin.fedoraproject.org/pkgdb/static/images/spinner/02.png',
        'https://admin.fedoraproject.org/pkgdb/static/images/spinner/03.png',
        'https://admin.fedoraproject.org/pkgdb/static/images/spinner/04.png',
        'https://admin.fedoraproject.org/pkgdb/static/images/spinner/05.png',
        'https://admin.fedoraproject.org/pkgdb/static/images/spinner/06.png',
        'https://admin.fedoraproject.org/pkgdb/static/images/spinner/07.png',
        'https://admin.fedoraproject.org/pkgdb/static/images/spinner/08.png',
        'http://admin.fedoraproject.org/pkgdb/static/images/spinner/09.png',
        'https://admin.fedoraproject.org/pkgdb/static/images/spinner/10.png',
        'https://admin.fedoraproject.org/pkgdb/static/images/spinner/11.png',
        'https://admin.fedoraproject.org/pkgdb/static/images/spinner/12.png'
            ];
    this._currenttFrame = 0;
    this.timeout = timeout || 0.1;
    this._intervalId = null;
}

fedora.widgets.Throbber.inherits(fedora.widgets.Widget);

/*
 * Throbber.render
 * ---------------
 * Display the throbber widget.
 *
 * Arguments:
 * :target: If given, replace the DOM node with this ID with the Throbber
 *
 * Returns: DOM node of the Throbber Widget
 */
fedora.widgets.Throbber.prototype.render = function (target) {
    var html = '<span class="widget FedoraThrobberWidget"'
        // Eventually, move this into fedorawidgets.css and include that in
        // our web page
        + ' style="position: absolute"'
        + ' id="' + this.widgetId + '">\n'
        + '<img src="' + this.inactiveImage
        + '" class="FedoraThrobberImage" />\n' + '</span>\n';
    if (target) {
        jQuery('#' + target).replaceWith(html);
    }
    return jQuery(html);
}

/*
 * Throbber._animate
 * ----------------
 * Change to the next frame of the throbber animation.
 */
fedora.widgets.Throbber.prototype._animate = function () {
    /* Only one image so we don't need to run over and over */
    if (this.frames.length <= 1) {
        return;
    }

    /* Check that we're not beyond the given frames */
    if (this._currentFrame >= this.frames.length) {
        this._currentFrame = 0;
    }

    /* Display the next frame */
    var html = '<img src="' + this.frames[this._currentFrame]
        + '" class="FedoraThrobberImage" />\n';
    jQuery('#' + this.widgetId + ' > .FedoraThrobberImage').replaceWith(html);
    this._currentFrame++;
}

/*
 * Throbber.start
 * ----------------
 * Start the throbber animation.
 */
fedora.widgets.Throbber.prototype.start = function () {
    if (this._intervalId) {
        window.clearInterval(this._intervalId);
    }
    /* Set an interval to animate the widget */
    var animate = fedora.functools.partial(function(self) {self._animate()}, this);
    this._intervalId = window.setInterval(animate, this.timeout * 1000);
}

/*
 * Throbber.stop
 * -------------
 * Stop the throbber animation.
 */
fedora.widgets.Throbber.prototype.stop = function () {
    /* Cancel the timeout that animates the throbber */
    window.clearInterval(this._intervalId);
    this._intervalId = null;

    /* Set animation back to the beginning of the loop */
    this._currentFrame = 0;

    /* Set back to the inactive image */
    console.debug('Setting image to ', this.inactiveImage);
    var html = '<img src="' + this.inactiveImage
        + '" class="FedoraThrobberImage" />\n';
    jQuery('#' + this.widgetId + ' > .FedoraThrobberImage').replaceWith(html);
    console.debug('Leaving Throbber.stop');
}

/* 
 * ---
 * RSS
 * ---
 * A widget to display RSS Feeds
 *
 * Example Template Code:
 * <script type="text/javascript">
 *   jQuery(document).ready(function() {
 *     people1 = new fedora.widgets.RSS('${tg.url(thisurl) + "?tg_format=json"}', 3, 'people1');
 *     jQuery(':button.refresh').filter('.people1').click(function () { people1.refresh();})
 *   });
 * </script>
 * ${RSSWidget(peopleData, 3, 'people1')}
 */

fedora.widgets.RSS = function(widgetId, widgetUrl, title, entries,
        displayedEntries) {
    fedora.widgets.RSS.base.call(this, widgetId);
    this.widgetUrl = widgetUrl;
    this.title = title;
    this.entries = entries;
    this.numEntries = displayedEntries;
    this.timeout = 5 *60;
}

fedora.widgets.RSS.inherits(fedora.widgets.Widget);

fedora.widgets.RSS.prototype.render = function (target) {
    var count = 0;
    var html = '<div class="widget RSSWidget"'
        + ' id="' + this.widgetId + '">\n'
        + '<h2>' + this.title + '</h2>\n<ul>';
    for (entryNum in this.entries) {
        if (count >= this.numEntries) {
            break;
        }
        html += '<li>\n'
        if ('image' in this.entries[entryNum]) {
            html += '<img src="' + this.entries[entryNum]['image']
                + '" height="32" width="32"/>\n'
        }
        html += '<a href="' + this.entries[entryNum]['link'] + '">'
            + this.entries[entryNum]['title'] + '</a>\n'
            + '</li>\n';
        count++;
    }
    html += '</ul>\n</div>\n';
    if (target) {
        /* If we were given a target, replace it */
        jQuery('#' + target).replaceWith(html);
    }
    return jQuery(html);
}

fedora.widgets.RSS.prototype.refresh_on  = function (timeout) {
    var timeout = timeout || 5;
    console.debug('In rss.refresh_on')
    if (this._intervalId) {
        window.clearInterval(this._intervalId);
    }
    this.refresh();
    /* Set the refresh rate */
    var refreshFunc = fedora.functools.partial(function(self) {self.refresh()}, this);
    this._intervalId = window.setInterval(refreshFunc, timeout * 1000);
}

fedora.widgets.RSS.prototype.refresh_off = function() {
    console.debug('In rss.refresh_off')
    window.clearInterval(this._intervalId);
    this._intervalId = null;
}

fedora.widgets.RSS.prototype.refresh = function () {
    console.debug('In rss.refresh')
    /* Busy the widget */
    this.busy();

    /* Use this local variable in our callback closures to assure we use the
     * correct values.
     */
    var widget = this;

    jQuery.ajax({
        /* FIXME: Hack for now; generalise later: */
        url: 'http://localhost:8080/widgets/RSS/?tg_format=json'
            + '&widgetId=' + escape(widget.widgetId)
            + '&title=' + escape(widget.title)
            + '&url=' + escape(widget.widgetUrl)
            + '&maxEntries=' + escape(widget.numEntries),
            /*
        url: 'http://localhost:8080/widgets/FedoraPeople/?tg_format=json'
            + '&widgetId=' + escape(widget.widgetId),
            */
        type: 'GET',
        dataType: 'jsonp',
        timeout: 5000,
        complete: function () {widget.unbusy();},
        error: function(data, message, error) {
            alert('Error refreshing the feeds', message);
            console.debug('data:',data);
            console.dir('inside data:',data);
            console.debug('status message:',message);
            console.debug('error:',error);
            console.dir('inside error:',error);
        },
        success: function(data, message) {
            /* Get the new feed data */
            console.debug('successful query');
            widget.entries = data.peopleData;
            widget.render(jQuery('table#' + widget.widgetId));
        }
    });
}
