# This file is part of Moksha.
# Copyright (C) 2008-2010  Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: John (J5) Palmieri <johnp@redhat.com>

import time
import bisect
import warnings

from datetime import datetime
from UserDict import DictMixin

try:
    from collections import OrderedDict as odict
except ImportError:
    from ordereddict import OrderedDict as odcit

class DateTimeDisplay(object):
    """DateTimeDisplay is an object which takes any number of datetime objects
    and process them for display.
    """
    def __init__(self, *datetime_args):
        warnings.warn("fedoracommunity.connectors.api.utils.DateTimeDisplay has been "
                      "deprecated, use moksha.common.lib.helpers.DateTimeDisplay "
                      "instead.", DeprecationWarning)

        # All dates are sorted from latest to earliest
        self._datetime_ordered_list = []
        for dt in datetime_args:
            # convert if not a datetime object
            insert_dt = None
            if isinstance(dt, datetime):
                insert_dt = dt
            elif isinstance(dt, basestring):
                insert_dt = datetime(*time.strptime(dt.rsplit('.', 1)[0],
                                                    '%Y-%m-%d %H:%M:%S')[:-2])

            bisect.insort(self._datetime_ordered_list, insert_dt)

    def __len__(self):
        return len(self._date_time_ordered_list)

    def time_elapsed(self, start_time_index, finish_time_index=None):
        startt = self._datetime_ordered_list[start_time_index]
        finisht = datetime.utcnow()
        if finish_time_index != None:
            finisht = self._datetime_ordered_list[finish_time_index]

        deltat = finisht - startt

        days = deltat.days
        hours = int(deltat.seconds / 3600)
        minutes = int((deltat.seconds - hours * 3600) / 60)
        seconds = deltat.seconds - minutes * 60
        display = ''
        if days:
            display = '%d d %d h %d m' % (days, hours, minutes)
        elif hours:
            display = '%d h %d m' % (hours, minutes)
        elif minutes:
            display = '%d m' % minutes
        else:
            display = '%d s' % seconds


        return ({'days': days, 'minutes': minutes,
                 'seconds': seconds, 'display': display})

    def when(self, index, time_format="%I:%M %p", date_format="%d %b %Y"):
        dt = self._datetime_ordered_list[index]
        time = dt.time().strftime(time_format)
        date = dt.date().strftime(date_format)

        el = self.time_elapsed(index)
        when = None
        should_hide_time = False
        if el['days'] == 0:
            when = 'Today'
        elif el['days'] == 1:
            when = 'Yesterday'
        else:
            should_hide_time = True

            def plural(i, singular, plural):
                word = (i == 1) and singular or plural
                return (i, word)

            if el['days'] < 7:
                when = "%d %s ago" % plural(el['days'], 'day', 'days')
            elif el['days'] < 365:
                when = "%d %s ago" % plural(int(el['days'] / 7), 'week', 'weeks')
            else:
                when = "%d %s ago" % plural(int(el['days'] / 365), 'year', 'years')

        return {'time':time, 'date':date , 'when':when, 'should_hide_time':should_hide_time}

class QueryCol(dict):
    def __init__(self,
                 column,
                 default_visible,
                 can_sort,
                 can_filter_wildcards):
        super(QueryCol, self).__init__(column = column,
                                       default_visible = default_visible,
                                       can_sort = can_sort,
                                       can_filter_wildcards = can_filter_wildcards)

class QueryPath(dict):
    def __init__(self,
                 path,
                 query_func,
                 primary_key_col,
                 default_sort_col,
                 default_sort_order,
                 can_paginate):
        super(QueryPath, self).__init__(
                         path = path,
                         query_func = query_func,
                         primary_key_col = primary_key_col,
                         default_sort_col = default_sort_col,
                         default_sort_order = default_sort_order,
                         can_paginate = can_paginate,
                         columns=odict())

    def register_column(self,
                        column,
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False):

        self["columns"][column] = QueryCol(
                column = column,
                default_visible = default_visible,
                can_sort = can_sort,
                can_filter_wildcards = can_filter_wildcards
              )

    def get_query(self):
        return self['query_func']

class ParamFilter(object):
    """Helper class for filtering query arguments"""

    def __init__(self):
        self._translation_table = {}
        self._param_table = {}

    def add_filter(self, param, args=None, cast=None, allow_none=True, filter_func=None):
        if args == None:
            args = []

        pf = {}
        if cast:
            assert(isinstance(cast, type),
                   "cast should be of type <type> not cast %s" % str(type(cast)))

            pf['cast'] = cast

        pf['allow_none'] = allow_none
        pf['filter_func'] = filter_func

        self._param_table[param] = pf

        args.append(param)
        for a in args:
            assert(not(a in self._translation_table),
                   '''The argument %s has been registered for more than
                   one parameter translation''' % (a)
                   )

            self._translation_table[a] = param

    def filter(self, d, conn=None):
        results = {}
        for k, v in d.iteritems():
            if k in self._translation_table:
                param = self._translation_table[k]
                allow_none = True
                assign = True
                if param in self._param_table:
                    pf = self._param_table[param]
                    cast = pf.get('cast')
                    if cast == bool:
                        if isinstance(v, basestring):
                            lv = v.lower()
                            if lv in ('t', 'y', 'true', 'yes'):
                                v = True
                            else:
                                v = False
                        elif not isinstance(v, bool):
                            v = False
                    elif cast:
                        v = cast(v)

                    allow_none = pf['allow_none']

                    ff = pf['filter_func']
                    if ff:
                        ff(conn, results, k, v, allow_none)
                        assign = False

                    if (allow_none or (v != None)) and assign:
                        results[param] = v

        return results

class WeightedSearch(object):
    # FIXME: Need to dial in the weighting algorithm
    CACHE_EXPIRE_TIME = 30 * 60
    LIGHT_WEIGHT = 10
    MEDIUM_WEIGHT = 30
    HEAVY_WEIGHT = 100

    def __init__(self, search_func, cols, cache=None):
        self.search_func = search_func
        self.cache = cache
        self.cols = cols

    def weigh(self, search_term, weighted_item):
        search_term_len = len(search_term)
        col_count = len(self.cols)

        # each field gets a decelerating percentage of it's calculated weight
        # e.g. each consecutive field is an order of magnatude less important
        # than the previous field
        factor = 1.0/float(sum(xrange(1, col_count+1)))

        item = weighted_item[0]
        for i, col_label in enumerate(self.cols):
            x = col_count - i
            weight_factor = float(x) * factor 

            col_value = item.get(col_label,'')
            
            if not isinstance(col_value, basestring):
                col_value = ''
            else:
                if not isinstance(col_value, unicode):
                    col_value = unicode(col_value, 'utf-8')
                    
                col_value = col_value.lower()
                
            index = col_value.find(search_term)

            while(index != -1):
                weighted_item[1] += self.LIGHT_WEIGHT * weight_factor
                if index == 0:
                    # in front
                    weighted_item[1] += self.MEDIUM_WEIGHT * weight_factor
                    if search_term_len == len(col_value):
                        weighted_item[1] += self.HEAVY_WEIGHT

                if index + search_term_len == len(col_value):
                    # in back
                    weighted_item[1] += self.MEDIUM_WEIGHT * weight_factor

                index = col_value.find(search_term, index + 1)

    def weighted_sort(self, a, b):
        result = 0
        (a_val, a_weight) = a
        (b_val, b_weight) = b

        result = -cmp(a_weight, b_weight)
        if result == 0:
            result = cmp(a_val[self.cols.key_index(0)], b_val[self.cols.key_index(0)])
        return result

    def search(self, search_string, primary_key_col, start_row, rows_per_page):
        if not search_string:
            return []

        search = search_string.lower().replace(',', ' ').split()

        if not primary_key_col:
            primary_key_col = self.cols.key_index(0)

        weighted_results = {}
        raw_search = []
        for s in search:
            results = self.cache.get_value(key = s,
                               createfunc=lambda : self.search_func(s),
                               type="memory",
                               expiretime=self.CACHE_EXPIRE_TIME)
            if results:
                raw_search.extend(results)

        for s in search:
            for r in raw_search:
                id = r[primary_key_col]
                # if we have already weighted this result get the
                # weighted hash to add weight to
                # else we create a new weighted hash
                if id in weighted_results:
                    weighted_item = weighted_results[id]
                else:
                    weighted_item = [r, 0]

                self.weigh(s, weighted_item)
                weighted_results[id] = weighted_item

        sorted_list = weighted_results.values()
        sorted_list.sort(self.weighted_sort)

        for i, v in enumerate(sorted_list):
            if v[0] > 0:
                sorted_list[i] = v[0]

        return (len(sorted_list), sorted_list[start_row:start_row + rows_per_page])






