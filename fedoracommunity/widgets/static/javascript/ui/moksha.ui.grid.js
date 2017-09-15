// This file is part of Moksha.
// Copyright (C) 2008-2009  Red Hat, Inc.
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

(function($) {
  $.widget("ui.mokshagrid",{
    controls: function(){},
    /* methods */
    options: {
        event: 'click',
        rows_per_page: 10,
        page_num: 1,
        total_rows: 0,
        start_row: 0,
        first_visible_row: 1, // 1 based index
        last_visible_row: 1, // 1 based index
        visible_rows: 0,
        filters: {},
        unique_key: undefined,
        sort_key: undefined,
        sort_order: -1,
        row_template: null,
        resource: null,
        resource_path: null,
        blankRowClass: 'moksha-grid-blank-row',
        rowClass: 'moksha-grid-row',
        pagerPageLimit: 5,
        more_link: null,
        loadOnCreate: true,
        loading_throbber: ["Loading",    // list of img urls or text
                           "Loading.",
                           "Loading..",
                           "Loading..."]
    },

    _create: function() {
      var self = this;
      var o = self.options;

      if (typeof(o.filters) != 'object') {
          try {
            self.options.filters = $.secureEvalJSON(o.filters);
          } catch(e) {
            self.options.filters = {};
            moksha.error(e);
          }
      }

      // add placeholder for row appends
      self.$rowplaceholder = jQuery('<span />').addClass('moksha_rowplaceholder');
      self.$rowplaceholder.hide();

      self._init_controls();

      if (!self.element.is('table')) {
          var t = self._generate_table();

          self.element.append(t);
      } else {
          self._setup_template();
      }

      self.clear();
    },

    _destroy: function() {
        this.$headers.unbind('.mokshagrid');
        this.element.unbind('.mokshagrid');
    },

    clear: function() {
       var self = this;
       var o = self.options;
       var $ph = self.$rowplaceholder;

       $('.' + o.rowClass, self.element).replaceWith('');
       o.visible_rows = 0;
       o.last_visible_row = 0;
    },

    insert_row: function(i, row_data) {
        var self = this;
        var o = self.options
        var row_count = o.visible_rows

        // store the widget for this element
        jQuery.data(self.element, 'mokshagrid', self);

        var $new_row = jQuery(jQuery.tmpl(o.row_template, row_data));
        moksha.update_marked_anchors($new_row);

        var $ph = self.$rowplaceholder;
        if (i == -1 || row_count == i) {
            var row_class = o.rowClass + '_' + row_count.toString();
            $ph.parent().append($new_row);
            $new_row.addClass(row_class).addClass(o.rowClass);
            o.visible_rows++;
            o.last_visible_row = o.start_row + o.visible_rows;
        } else {
            // insert before i element and update all row numbers
            var row_class = o.rowClass + '_' + i.toString();
            var $row = $('.' + row_class, $ph.parent());
            $new_row.addClass(row_class).addClass(o.rowClass);

            var $current_rows = $('.' + o.rowClass, $ph.parent());
            for (j = i; j < $current_rows.length; j++) {
                var k = j + 1;
                var old_class = o.rowClass + '_' + j.toString();
                var new_class = o.rowClass + '_' + k.toString();
                var $cur_row = $($current_rows[j]);
                if ($cur_row) {
                    $cur_row.removeClass(old_class);
                    $cur_row.addClass(new_class);
                }
            }

            $row.before($new_row);

            o.visible_rows++;
            if (row_count == o.rows_per_page) {
                o.visible_rows = o.rows_per_page;
                self.remove_row(o.rows_per_page);
            }

            o.last_visible_row = o.start_row + o.visible_rows;
        }

        $new_row.show();

        // run any included extension points
        if (moksha.extensions)
            moksha.extensions.grep_extensions($new_row);
    },

    append_row: function(row_data) {
        var self = this;
        self.insert_row(-1, row_data);
    },

    remove_row: function(i) {
        var self = this;
        var o = self.options;
        var $ph = self.$rowplaceholder;
        var $rows = $('.' + o.rowClass, $ph.parent());
        var r = $rows[i];

        if (r) {
            $(r).replaceWith('');
            if (i < o.rows_per_page)
                o.visible_rows--;
        }

        //FIXME: We need to relabel rows if this is not the
        //       end of the rows
    },

    connector_query_model: function(connector, path, callback) {
        path = '/query_model/' + path;
        fcomm.connector_load(connector, path, {}, callback, this.$overlay_div);
    },

    connector_query: function(connector, path, dispatch_data, callback) {
        path = '/query/' + path;
        if (dispatch_data)
            path = path + '/' + JSON.stringify(dispatch_data);

        fcomm.connector_load(connector, path, {}, callback, this.$overlay_div);
    },

    request_data_refresh: function(event) {
        // TODO: allow an optional rows_requested parameter
        var self = this;
        var o = self.options;

        // figure out which row to start with
        var rpp = o.rows_per_page;
        var start_row = (o.page_num - 1) * rpp;

        // setup the search criteria
        var search_criteria = {
            filters: jQuery.extend(true, {}, o.filters),
            start_row: start_row,
            rows_per_page: rpp,
            sort_key: o.sort_key,
            sort_order: o.sort_order
        }

        // TODO: Only trigger refresh signal if we have a cache miss
        self.refresh_data(event, search_criteria);
    },

    goto_page: function(page) {
        this.options.page_num = page;
        this.request_data_refresh();
    },

    goto_alpha_page: function(prefix) {
        if (typeof(prefix) == 'undefined')
            prefix = '';

        if (typeof(this.options.filters) != 'object')
            this.options.filters = {}

        this.options.filters.prefix = prefix;
        this.options.page_num = 1;

        this.request_data_refresh();
    },

    request_update: function(search_criteria) {
        var self = this;

        var sc = search_criteria;

        if (typeof(sc.rows_per_page) != 'undefined')
            self.options.rows_per_page = sc.rows_per_page;

        if (typeof(sc.page_num) != 'undefined')
            self.options.page_num = sc.page_num;

        if (typeof(sc.filters) != 'undefined')
            self.options.filters = jQuery.extend(true, self.options.filters, sc.filters);

        if (typeof(sc.sort_key) != 'undefined')
            self.options.sort_key = sc.sort_key;

        if (typeof(sc.sort_order) != 'undefined')
            self.options.sort_order = sc.sort_order;

        self.request_data_refresh();
    },

    _foreach_controls: function(callback, eval_conditional) {
        var options = this.options;

        // get our controls if conditional is true
        var _filter_conditional = function(i) {
            var if_attr = $(this).attr('if');
            // always return true for elements without a conditional
            var result = true;
            if (if_attr) {

                // contain this in a function block to contain variables
                // which is executed immediately
                (function() {
                    // turn the dictionary members into variable local to this
                    // function block
                    for(key in options) {
                        var eval_line = 'var ' + key + '=';
                        var value = options[key];

                        try {
                            eval_line += JSON.stringify(value);
                        } catch(err) {
                            continue;
                        }
                        eval(eval_line);
                        value = ''
                        eval_line = '';
                    }

                    // return the results of the conditional
                    result = eval(if_attr);
                })();
            }

           if (!result)
               $(this).hide();
           else
               $(this).show();

           return result;
        }

        var self = this;
        var $contols = self.$_control_list;
        if (eval_conditional)
            $controls = self.$_control_list.filter(_filter_conditional);

        // iterate through all of our control plugins
        // and get any id that matches
        for(var key in self.controls) {
            var $matched_controls = $("#" + key, $controls);
            $.each($matched_controls, function(i, c) {
                                          callback(self.controls[key], i, c);
                                      });
        }
    },

    _init_controls: function() {
        var self = this;

        $controls = $('#grid-controls', this.element.parent()).hide();
        self.$_control_list = $controls;

        $.each($controls, function(i, c) {
            var $c = $(c);
            var attach = $c.attr('attach');
            if (attach) {
                // attach is a jQuery selector relative to the ancestor
                // ancestor is specified by an integer indicating how many
                // levels we should traverse up the parent tree
                parent_nest = $c.attr('ancestor');

                $parent = $(document);
                if (typeof(parent_nest) != 'undefined') {
                    $parent = $c;
                    for (var i=0; i<parent_nest; i++) {
                        $parent = $parent.parent();
                    }
                }

                var $attach_node = $(attach, $parent);
                $attach_node.append($c);
            }
        });

        var f = function(plugin, i, c) {
            // for each matched control call the
            // _init method of the plugin if it has one
            $c = $(c);
            $c.data('grid.moksha_grid', self);

            if (plugin._init)
                plugin._init.call(plugin,
                                  self,
                                  $c);
        }

        this._foreach_controls(f);
    },

    _process_controls: function() {
         var self = this;
         var f = function(plugin, i, c) {
            // for each matched control call the
            // processElement method of the plugin
            results = plugin.processElement.call(plugin,
                                                 $(c));

            // place the results inside the element
            $(c).html(results);
            $(c).show();
          }

        this._foreach_controls(f, true);
    },

    refresh_data: function(event, search_criteria) {
        var self = this;
        var o = self.options;

        if (!o.resource || !o.resource_path)
            return;

        var results = function(json) {
            self.clear();
            if (json.error) {

            }

            // reset based on returned values
            o.total_rows = json.total_rows;
            o.start_row = json.start_row;
            o.first_visible_row = o.start_row + 1; // user visible index always starts with 1 not 0
            o.rows_per_pager = json.rows_per_page;

            for (var i in json.rows) {
                var row = json.rows[i];
                self.append_row(row);
            }

            moksha.defer(self, function() {
                                            self._process_controls();
                                          });
        }

        var dispatch_data = {}

        var filters = search_criteria.filters
        if (typeof(filters) != 'undefined')
            dispatch_data['filters'] = filters

        var rows_per_page = search_criteria.rows_per_page
        if (typeof(rows_per_page) != 'undefined')
            dispatch_data['rows_per_page'] = rows_per_page

        var start_row = search_criteria.start_row
        if (typeof(start_row) != 'undefined')
            dispatch_data['start_row'] = start_row

        if (search_criteria.sort_key) {
            dispatch_data["sort_col"] = search_criteria.sort_key;
            dispatch_data["sort_order"] = search_criteria.sort_order;
        }

        self.connector_query(
                      o.resource,
                      o.resource_path,
                      dispatch_data,
                      results);
    },

    load_more_results: function(last_row, rows_per_page) {
        var self = this;
        var o = self.options;

        if (!o.resource || !o.resource_path)
            return;

        var results = function(json) {
            for (var i in json.rows) {
                var row = json.rows[i];
                self.append_row(row);
            }

            // reset based on returned values
            o.total_rows = json.total_rows;
            moksha.defer(self, function() {
                                            self._process_controls();
                                          });
        }

        var dispatch_data = {}

        var filters = o.filters
        if (typeof(filters) != 'undefined')
            dispatch_data['filters'] = filters

        var rows_per_page = o.rows_per_page
        if (typeof(rows_per_page) != 'undefined')
            dispatch_data['rows_per_page'] = rows_per_page

        var start_row = last_row + 1;
        dispatch_data['start_row'] = start_row

        if (o.sort_key) {
            dispatch_data["sort_col"] = o.sort_key;
            dispatch_data["sort_order"] = o.sort_order;
        }

        self.connector_query(
                      o.resource,
                      o.resource_path,
                      dispatch_data,
                      results);
    },

    /* Signals */
    ready: function(event, user_data) {

    },

    /* Getter/Setters */

    visible_row_count: function() {
        var self = this;
        var o = self.options;
        return o.visible_rows;
    },

    /* Private */
    _setup_template: function() {
      var self = this;
      var o = self.options;

      var rowtemplate = jQuery('.rowtemplate', self.element);
      rowtemplate.removeClass('rowtemplate')
      if (rowtemplate.length)
          rowtemplate.after(self.$rowplaceholder);

      // hack to get the full html of the template including the root tag
      // this also removes the template from the document
      var container_div = jQuery('<div />');
      var html = unescape(container_div.append(rowtemplate).html());

      o.row_template = jQuery.template(html);

      // create a blank row by taking the template HTML and replacing
      // the data inside the td's with a non breaking space
      $_blank_row = $(html).addClass(o.blankRowClass).addClass(o.rowClass);
      var $clear_td = $('td', $_blank_row)
      $clear_td.html('&nbsp;');
      self._blank_row = $('<div />').append($_blank_row).html();

      self.$headers =  $('th:has(a[href])', this.element);
      //self.$headers = this.$ths.map(function() { return $('a', this)[0]; });
      self.$headers.unbind(o.event + '.mokshagrid').bind(o.event + '.mokshagrid', function(event) {
        var ckey = o.sort_key;
        var corder = o.sort_order;
        var key = event.originalTarget.hash.substr(1);

        if (key == ckey) {
            if (corder == -1) {
                corder = 1;
            } else {
                corder = -1;
            }
        } else {
            corder = 'decending';
        }

        self.options['sort_key'] = key;
        self.options['sort_order'] = corder;

        self.request_data_refresh();

        return false;
      })

      var $overlay = $('.overlay', self.element)
      if ($overlay.length == 0) {
          $overlay = $('<div />').addClass('overlay')
          $overlay.css({'opacity': 1,
                        'z-index': 99,
                        'background-color': 'white',
                        'position': 'absolute'
                       }
                      )

          $overlay.append($('<div />').addClass('message'));
          $overlay.hide();

      }

      self.element.parent().prepend($overlay);
      self.$overlay_div = $overlay;

      var $pager_top_placeholder = $('<div></div>').addClass(o.pagerTopClass).hide();
      $pager_top_placeholder.append($("<div></div>").addClass('pager'));
      $pager_top_placeholder.insertBefore(self.element);
      self.$pager_top_placeholder = $pager_top_placeholder;

      var $pager_bottom_placeholder = $('<div></div>').addClass(o.pagerBottomClass).hide();
      $pager_bottom_placeholder.append($("<div />").addClass('message'));
      $pager_bottom_placeholder.append($("<div></div>").addClass('pager'));
      $pager_bottom_placeholder.insertAfter(self.element);
      self.$pager_bottom_placeholder = $pager_bottom_placeholder;

      self._process_controls();
      if (o.loadOnCreate)
          self.request_data_refresh();
    },

    _generate_table: function() {
        var self = this;
        var t = $('<table />');
        var o = self.options;
        // get the model if there is a resource and path
        if (!o.resource || !o.resource_path)
            return t;

        var results = function(json) {
            o.sort_key = json.default_sort_col;
            o.sort_order = json.default_sort_order;

            var headers = $('<thead />');
            var header_tr = $('<tr />');
            headers.append(header_tr);
            t.append(headers);

            var template =  $('<tbody />').addClass("rowtemplate");
            var template_tr = $('<tr />');
            template.append(template_tr);
            t.append(template);

            for (var c in json.columns) {
                var c_data = json.columns[c];
                if (!c_data.default_visible)
                    continue;

                if (c_data.can_sort) {
                    var a = $('<a />').attr('href', '#' + c).text(c);
                    var th = $('<th />').append(a);
                    header_tr.append(th);
                } else {
                    var td = $('<th />').text(c);
                    header_tr.append(td);
                }

                template_tr.append('<td>@{' + c + '}</td>');
            }

            self._setup_template();
        }

        self.connector_query_model(
                      o.resource,
                      o.resource_path,
                      results);

        return t;
    }
  })

  $.extend($.ui.mokshagrid, {
          version: '@VERSION',
          getters: 'visible_row_count'
  });

  $.ui.mokshagrid.prototype.controls.filter = {
      _init: function($grid, $el) {
          var filters = this.getFilters($el);
          var self = this;
          var o = $grid.options;

          var onChange = function(e) {
              var filters = e.data;
              var o = $grid.options;
              filters[this.name] = this.value;
              o.filters = filters;

              // reset pagination
              o.page_num = 1;
              o.total_rows = 0;
              o.start_row = 0;
              o.first_visible_row = 1; // 1 based index
              o.last_visible_row = 1; // 1 based index
              o.visible_rows = 0;

              $grid.request_data_refresh();
          }

          filters.change(o.filters, onChange);

          // set the defaults
          $.each(filters, function (i, f) {
                              o.filters[f.name] = f.value;
                          });
      },

      getFilters: function($el) {
          var filters = $el.find('select,input');

          return filters;
      },

      processElement: function($el) {
          // we don't do anything here as it is all handled by the event handler
      }
  }

  $.ui.mokshagrid.prototype.controls.info_display = {
      _init: function($grid, $el) {
          var template_html = '<span>' + unescape($el.html()) + '<span>';
          var $template = jQuery.template(template_html);

          // place in a data slot inside the element
          $el.data('info_display_template.moksha_grid', $template);

          $el.html(this.processElement($el));

          // remove the template marker from the element
          $el.removeClass('template');
      },

      processElement: function($el) {
          var $grid = $el.data('grid.moksha_grid');

          var $template = $el.data('info_display_template.moksha_grid');
          return this._generate_info_display($template, $grid.options);
      },

      _generate_info_display: function($template, o) {
          var $display = jQuery(jQuery.tmpl($template, o));
          moksha.update_marked_anchors($display);

          return $display;
      }
  }

  $.ui.mokshagrid.prototype.controls.pager = {
      pager_types: {},
      _init: function($grid, $el) {
          var type = $el.attr('type');

          var pager_obj = this.pager_types[type];
          if (!pager_obj) {
              moksha.warn('Pager type ' + type + ' requested but does not have a plugin');
              return '';
          }


          if (typeof(pager_obj._init) == "function") {
              pager_obj._init.call(pager_obj,
                                   $grid,
                                   $el);
          }
      },

      processElement: function($el) {
          var type = $el.attr('type');

          var pager_obj = this.pager_types[type];

          if (!pager_obj) {
              moksha.warn('Pager type ' + type + ' requested but does not have a plugin');
              return '';
          }

          return pager_obj.processElement.call(this.pager_types[type],
                                               $el);
      }
  }

  $.ui.mokshagrid.prototype.controls.pager.pager_types.more_link = {

      _init: function($grid, $el) {
          var template_html = unescape($el.html());
          var $template = jQuery.template(template_html);

          // place in a data slot inside the element
          $el.data('more_link_template.moksha_grid', $template);

          // remove the template marker from the element
          $el.removeClass('template');

          $el.html(this.processElement($el));
      },

      processElement: function($el) {
          var $grid = $el.data('grid.moksha_grid');
          if (!$grid.options.more_link)
              return "";

          var $template = $el.data('more_link_template.moksha_grid');
          return this._generate_more_pager($template, $grid.options);
      },

      _generate_more_pager: function($template, o) {
          var $pager = jQuery(jQuery.tmpl($template, o));
          moksha.update_marked_anchors($pager);

          return $pager;
      }
  }

  $.ui.mokshagrid.prototype.controls.pager.pager_types.alpha = {
      processElement: function($el) {
          var $grid = $el.data('grid.moksha_grid');

          return this._generate_alpha_pager($grid);
      },

      _generate_alpha_pager: function ($grid) {
          var o = $grid.options;
          var curr_alpha = o.filters.prefix;
          if (typeof(curr_alpha) == 'undefined')
              current_alpha = '';

          var pager = $('<ul />');
          var goto_page = function() {
              var page_jump = $(this).data('alpha_page.moksha_grid');
              $grid.goto_alpha_page(page_jump);
          }

          var alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
          for (i in alph) {
              var a = alph[i];

              var page = $('<li />').html(a).addClass('page-button').addClass('current-page');
              if (a!=curr_alpha) {
                  page.removeClass('current-page');

                  var page_link = $('<a href="javascript:void(0)"></a>').html(a);
                  page_link.data('alpha_page.moksha_grid', a);
                  page_link.click(goto_page);

                  page.html(page_link);
              }

              pager.append(page);
          }

          var page = $('<li>All</li>').addClass('page-button').addClass('current-button');
          if (curr_alpha != '') {
             var page_link = $('<a href="javascript:void(0)"></a>').html('All');

             page_link.data('alpha_page.moksha_grid', '');
             page_link.click(goto_page);

             page.html(page_link);
          }

          pager.append(page);

          return pager;
      }
  }

  $.ui.mokshagrid.prototype.controls.pager.pager_types.numeric = {
      processElement: function($el) {
          var $grid = $el.data('grid.moksha_grid');
          var o = $grid.options;

          return this._generate_numerical_pager($grid,
                                                o.total_rows,
                                                o.start_row,
                                                o.rows_per_page);
      },

      _generate_numerical_pager: function ($grid, total_rows, start_row, rows_per_page) {
          var o = $grid.options;
          var total_pages = parseInt(total_rows / rows_per_page);
          if (total_rows != total_pages * rows_per_page)
              total_pages += 1;

          if (total_pages == 1)
              return "";

          var curr_page = parseInt((start_row + 0.5) / rows_per_page) + 1;
          var next_page = curr_page + 1;
          var prev_page = curr_page -1;
          var next_elipse = curr_page + o.pagerPageLimit;
          var prev_elipse = curr_page - o.pagerPageLimit;

          var pager = $('<ul />');

          var goto_page = function() {
              var page_jump = $(this).data('page.moksha_grid');
              $grid.goto_page(page_jump);
          }

          var show_prev = parseInt((o.pagerPageLimit + 0.5) / 2) + 1;
          var show_next = o.pagerPageLimit - show_prev;
          var num_next_left = total_pages - curr_page;
          if (num_next_left < show_next)
              show_prev += (show_next - num_next_left)

          // previous link
          var page = $("<li>Prev</li>").addClass('page-button').addClass('prev-page').addClass('no-link');
          if (curr_page != 1) {
              page.removeClass('no-link');
              var page_link = $('<a href="javascript:void(0)"></a>').html('Prev');
              page_link.data('page.moksha_grid', prev_page);
              page_link.click(goto_page);
              page.html(page_link);
          }

          pager.append(page);

          // elipsised page jumper
          if (curr_page - show_prev > 0) {
              // first page link
              var page = $('<li></li>').addClass('page-button');
              page_link = $('<a href="javascript:void(0)"></a>').html('1');
              page_link.data('page.moksha_grid', 1);
              page_link.click(goto_page);
              page.html(page_link);
              pager.append(page);

              // elipse link
              var page = $('<li>...</li>').addClass('page-button');
              if (prev_elipse > 1) {
                  page_link = $('<a href="javascript:void(0)"></a>').html('...');
                  page_link.data('page.moksha_grid', prev_elipse);
                  page_link.click(goto_page);
                  page.html(page_link);
              }
              pager.append(page);
          }

          var page_list = [];
          var i, j;
          for (i = curr_page, j = 0; i > 0 && j < show_prev; i--, j++)
              page_list.push(i);

          page_list.reverse();
          if (page_list.length < show_prev)
              show_next += (show_prev - page_list.length)

          for (i = curr_page + 1, j = 0; i <= total_pages && j < show_next; i++, j++)
              page_list.push(i);

          for (i in page_list) {
              var page_num = page_list[i];
              var page = $('<li></li>').html(page_num).addClass('page-button').addClass('current-page');
              if (page_num != curr_page) {
                  page.removeClass('current-page');
                  var page_link = $('<a href="javascript:void(0)"></a>').html(page_num);

                  page_link.data('page.moksha_grid', page_num);
                  page_link.click(goto_page);
                  page.html(page_link);
              }

              pager.append(page);
          }

          // elipsised page jumper
          if (curr_page + show_next < total_pages) {
              // elipse link
              var page = $('<li>...</li>').addClass('page-button');
              if (next_elipse < total_pages) {
                  page_link = $('<a href="javascript:void(0)"></a>').html('...');
                  page_link.data('page.moksha_grid', next_elipse);
                  page_link.click(goto_page);
                  page.html(page_link);
              }
              pager.append(page);

              // last page link
              var page = $('<li></li>').addClass('page-button');
              page_link = $('<a href="javascript:void(0)"></a>').html(total_pages);
              page_link.data('page.moksha_grid', total_pages);
              page_link.click(goto_page);
              page.html(page_link);
              pager.append(page);

          }

          var page = $("<li>Next</li>").addClass('page-button').addClass('next-page').addClass('no-link');
          if (curr_page < total_pages) {
              page.removeClass('no-link');
              var page_link = $('<a href="javascript:void(0)"></a>').html('Next');
              page_link.data('page.moksha_grid', next_page);
              page_link.click(goto_page);
              page.html(page_link);
          }
          pager.append(page);

          var page = $("<li>All</li>").addClass('page-button').addClass('all-pages').addClass('no-link');
          if (total_pages != 1) {
              page.removeClass('no-link');
              var page_link = $('<a href="javascript:void(0)"></a>').html('All');
              page_link.data('start_row.moksha_grid', 1);
              page_link.data('rows_per_page.moksha_grid', total_rows);
              var show_all = function() {
                  $grid.options.page_num = $(this).data('start_row.moksha_grid');
                  $grid.options.rows_per_page = $(this).data('rows_per_page.moksha_grid');
                  $grid.request_data_refresh();
              }
              page_link.click(show_all);
              page.html(page_link);
              pager.append(page);
          }

          return(pager);
      }
  }

  $.ui.mokshagrid.prototype.controls.pager.pager_types.more = {
      processElement: function($el) {
          var $grid = $el.data('grid.moksha_grid');
          var o = $grid.options;

          return this._generate_more_pager ($grid,
                                            o.total_rows,
                                            o.start_row,
                                            o.rows_per_page,
                                            o.visible_rows);
      },

      _generate_more_pager: function ($grid, total_rows, start_row, rows_per_page, visible_rows) {
          var o = $grid.options;

          var last_row = visible_rows + start_row;
          if (last_row == total_rows)
              return "";

          var pager = $('<span>');

          var load_more = function() {
              $grid.load_more_results(last_row-1, rows_per_page);
          }

          var more = $('<a href="javascript:void(0)"></a>').html('More');
          more.click(load_more);

          pager.append(more);

          return(pager);
      }
  }

})(jQuery);
