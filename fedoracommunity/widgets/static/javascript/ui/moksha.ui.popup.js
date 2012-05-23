// This file is part of Moksha.
// Copyright (C) 2008-2010  Red Hat, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/*
 * Moksha UI Popup - Popup a block on user interactions such as mouse hover and click.
 *                   Can be used to create popup menus
 *
 * Copyright (c) 2009 Red Hat, Inc.
 * Dual licensed under the MIT
 * and GPLv2 licenses.
 *
 *
 * Depends:
 *      jQuery - ui.core.js
 */
(function ($) {
$.widget("ui.moksha_popup", {
	options: {
	    popupClass: 'ui-moksha-popup',
	    popupItemsClass: 'ui-moksha-popup-items',
	    selectedClass: 'ui-moksha-selected',
	    panelClass: 'ui-moksha-popup-panel',
	    hoverTimeout: 500,
	    triggerEvent: 'hover',
	    fx: null // e.g. { height: 'toggle', opacity: 'toggle', duration: 200 }
    },

	_create: function() {
		// create popup
		this._createpopup();
	},

	destroy: function() {

	},

	_popupId: function(e) {
	        var title = e.attr('panel');
                return title && title.replace(/\s/g, '_').replace(/[^A-Za-z0-9\-_:\.]/g, '')
                        || this.options.idPrefix + $.data(e);
        },

	showPopup: function() {
		var $e = this.element;
		var o = this.options;
		this.timer = null;

		$e.children(':first').addClass(o.selectedClass);
        if (this.showFx) {
			this.$panel.animate(this.showFx, this.showFx.duration || this.baseFx.duration);
		} else {
			this.$panel.show();
		}

		// fire off a show event
		$e.trigger('show');

	},

	hidePopup: function() {
		var $e = this.element;
		var o = this.options;
		$e.children(':first').removeClass(o.selectedClass);
		if (this.hideFx) {
			this.$panel.animate(this.hideFx, this.hideFx.duration || this.baseFx.duration);
                } else {
			this.$panel.hide();
		}

		$e.trigger('hide');
	},

	_startHover: function() {
		var self = this;
		var o = this.options;
		moksha.debug('Hover Started');
		this.timer = setTimeout(function () {self.showPopup.apply(self)}, o.hoverTimeout);
	},

	_endHover: function() {
		if (this.timer)
			clearTimeout(this.timer);

		this.timer = null;
		this.hidePopup();
	},
	_createpopup: function() {
		var o = this.options;
		var $e = this.element;

		this.hover_timer = null;

		if (o.popupClass) {
			$e.addClass(o.popupClass);
		}

		var popup_id = this._popupId($e);
		var $panel = $e.find('#' + popup_id);
		if (!$panel.length) {
			$panel = $('<div />').attr('id', popup_id).addClass(o.popupItemsClass);
                	$e.append($panel);
		}

		this.$panel = $panel.addClass(o.panelClass);
		this.$panel.hide()

		// set up animations
		var hideFx, showFx, baseFx = { 'min-height': 0, duration: 1 }, baseDuration = 'normal';
		if (o.fx && o.fx.constructor == Array)
			hideFx = o.fx[0] || baseFx, showFx = o.fx[1] || baseFx;
		else
			hideFx = showFx = o.fx

		this.hideFx = hideFx;
		this.showFx = showFx;
		this.baseFx = baseFx;

		if (o.triggerEvent == 'click') {
			// FIXME: getting click right is hard
		} else {
		        var self = this;
			$e.hover(function () {self._startHover.apply(self)}, function () {self._endHover.apply(self)});
		}

	}
});

$.extend($.ui.moksha_popup, {
	version: '@VERSION'
});


})(jQuery);
