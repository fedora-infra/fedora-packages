# This file is part of Fedora Community.
# Copyright (C) 2008-2009  Red Hat, Inc.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from tg import expose, tmpl_context
from tw.api import Widget
from tw.forms import SingleSelectField
from webhelpers.rails.number import number_to_human_size

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, defaultdict
from moksha.api.connectors import get_connector
from helpers import PackagesDashboardContainer

log = logging.getLogger(__name__)

class ReleaseDownloadsFilter(SingleSelectField):
    options = []
    attrs = {'onchange': """
        moksha.html_load(moksha.url('/apps/fedoracommunity.packages/package/downloads/downloads'), {'package': package_name, 'release': $('#downloads_widget_releases').val()}, function(r) {
                    var $stripped = moksha.filter_resources(r);
                    $('div.package_downloads').html($stripped);
            }, $("#" + uid + " .overlay"));"""}


class DownloadsDashboard(PackagesDashboardContainer):
    layout = [Category('content-col-apps',[
                MokshaApp(None,
                    'fedoracommunity.packages/package/downloads/downloads',
                    params={'package': '', 'release': 'dist-rawhide'},
                    css_class='package_downloads'),
                ])]

downloads_dashboard = DownloadsDashboard('downloads_dashboard')


class SourceDashboard(PackagesDashboardContainer):
    layout = [Category('content-col-apps',[
                MokshaApp(None,
                     'fedoracommunity.packages/package/downloads/source',
                     params={'package': ''}),
                ])]

source_dashboard = SourceDashboard('source_dashboard')


class DownloadsWidget(Widget):
    template = "mako:fedoracommunity.mokshaapps.packages.templates.downloads_widget"
    params = ['id', 'package', 'release', 'latest_spec', 'latest_srpm',
              'arches', 'releases']
    children = [ReleaseDownloadsFilter('releases')]

    def update_params(self, d):
        super(DownloadsWidget, self).update_params(d)
        koji = get_connector('koji')
        rpms = koji._koji_client.getLatestRPMS(d.release, package=d.package)

        arches = defaultdict(list)
        for download in rpms[0]:
            download['size'] = number_to_human_size(download['size'])
            download['nvr'] = '%s-%s-%s.%s.rpm' % (download['name'],
                    download['version'], download['release'],
                    download['arch'])
            download['url'] = \
                'http://kojipkgs.fedoraproject.org/packages/%s/%s/%s/%s/%s' % (
                    d.package, download['version'], download['release'],
                    download['arch'], download['nvr'])
            arches[download['arch']].append(download)

        if len(arches['src']):
            d.latest_srpm = arches['src'][0]
        del(arches['src'])

        # Determine the branch name from the release.
        pkgdb = get_connector('pkgdb')
        collections = pkgdb.get_collection_table(active_only=True)
        branch = None
        for id, collection in collections.items():
            if collection['koji_name'] == d.release:
                branch = collection['branchname']
                break
        if not branch:
            raise Exception("Cannot find branchname for %s" % d.release)

        d.latest_spec = 'http://cvs.fedoraproject.org/viewvc/rpms/%s/%s/%s.spec?view=markup' % (d.package, branch, d.package)
        d.arches = arches
        d.releases = pkgdb.get_fedora_releases()

downloads_widget = DownloadsWidget('downloads_widget')


class SourceDownloadsWidget(Widget):
    template = "mako:fedoracommunity.mokshaapps.packages.templates.source_downloads_widget"
    params = ['id', 'package', 'sources']

    def update_params(self, d):
        super(SourceDownloadsWidget, self).update_params(d)
        sources = []
        releases = []
        dist_tags = {}

        koji = get_connector('koji')._koji_client
        koji.multicall = True

        pkgdb = get_connector('pkgdb')
        collections = pkgdb.get_collection_table(active_only=True)
        for id, collection in collections.items():
            if collection['name'] == 'Fedora':
                tag = collection['koji_name']
                releases.append(tag)
                dist_tags[tag] = '%s %s' % (collection['name'],
                                            collection['version'])
                if 'rawhide' not in tag:
                    tag += '-updates'
                koji.getLatestRPMS(tag, package=d.package, arch='src')

        results = koji.multiCall()
        koji.multicall = False

        for i, result in enumerate(results):
            if 'faultCode' in result:
                log.warning('Skipping koji result: %s' % result['faultString'])
                continue
            if not result[0][0]:
                log.warning('Skipping koji result for %s' % releases[i])
                continue
            build = result[0][0][0]
            build['nvr'] = '%s-%s-%s.%s.rpm' % (build['name'],
                    build['version'], build['release'], build['arch'])
            sources.append({
                'release': dist_tags[releases[i]],
                'released_version': '%s-%s' % (build['version'],
                                               build['release']),
                'size': number_to_human_size(build['size']),
                'nvr': build['nvr'],
                'url': 'http://kojipkgs.fedoraproject.org/packages/%s/%s/%s/%s/%s' % (build['name'], build['version'], build['release'], build['arch'], build['nvr']),
                })
        d.sources = sources

source_downloads_widget = SourceDownloadsWidget('source_downloads_widget')


class DownloadsController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, package):
        tmpl_context.widget = downloads_dashboard
        return dict(options={'package': package})

    @expose('mako:moksha.templates.widget')
    def downloads(self, package, release, *args, **kw):
        tmpl_context.widget = downloads_widget
        return dict(options={'package': package, 'release': release})

    @expose('mako:moksha.templates.widget')
    def source(self, package, *args, **kw):
        tmpl_context.widget = source_downloads_widget
        return dict(options={'package': package})
