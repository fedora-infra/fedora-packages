# Copyright (C) 2008  Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program; if
# not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA. Any Red Hat trademarks that are
# incorporated in the source code or documentation are not subject to the GNU
# General Public License and may only be used or replicated with the express
# permission of Red Hat, Inc.
#
# Author(s): Luke Macken <lmacken@redhat.com>

from tw.api import Widget
from myfedora.streams import RSSDataStream

class RSSWidget(Widget):
    """ A generic RSS widget.

    This Widget is able to stream data using comet to the user.  This means,
    that once the widget is rendered, it will automatically open a persistent
    connect back to the server where data will be pushed asynchronously.

    This widget uses jQuery to populate and animate new item creation.
    """
    # TODO: use javascript property
    template = 'myfedora.templates.rsswidget'
    params = ['widgetId', 'title', 'entries']
    title = ''
    url = ''

    def __str__(self):
        return "<%s>" % self.__class__.__name__


class FedoraPeopleData(RSSDataStream):
    url = 'http://planet.fedoraproject.org/rss20.xml'
    title = 'Fedora People' # pull the title from the rss feed?


class FedoraPeopleWidget(RSSWidget):
    name = 'Fedora People'
    authors = ['Luke Macken <lmacken@redhat.com>']
    description = 'A streaming Fedora People widget'
    data = FedoraPeopleData
