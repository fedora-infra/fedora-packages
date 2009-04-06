from tw.api import Widget
from webhelpers.rails.number import number_to_human_size

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget, defaultdict
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget
from moksha.api.connectors import get_connector
from helpers import PackagesDashboardContainer

from tg import expose, tmpl_context, require, request

class DownloadsDashboard(PackagesDashboardContainer):
    layout = [Category('content-col-apps',[
                MokshaApp(None,
                         'fedoracommunity.packages/package/downloads/downloads',
                         params={'package': '', 'release': 'rawhide'}),
                ])]

class SourceDashboard(PackagesDashboardContainer):
    layout = [Category('content-col-apps',[
                MokshaApp(None,
                     'fedoracommunity.packages/package/downloads/source',
                     params={'package': ''}),
                ])]

downloads_dashboard = DownloadsDashboard('downloads_dashboard')
source_dashboard = SourceDashboard('source_dashboard')

class DownloadsWidget(Widget):
    template = "mako:fedoracommunity.mokshaapps.packages.templates.downloads_widget"
    params = ['id', 'package', 'release', 'latest_spec', 'latest_srpm', 'arches']
    def update_params(self, d):
        super(DownloadsWidget, self).update_params(d)
        koji = get_connector('koji')
        rpms = koji._koji_client.getLatestRPMS('dist-%s' % d.release,
                                               package=d.package)

        arches = defaultdict(list)
        for download in rpms[0]:
            download['size'] = number_to_human_size(download['size'])
            download['nvr'] = '%s-%s-%s.%s.rpm' % (download['name'],
                    download['version'], download['release'],
                    download['arch'])
            download['url'] = \
                'http://kojipkgs.fedoraproject.org/packages/%s/%s/%s/%s/%s' % (
                    download['name'], download['version'], download['release'],
                    download['arch'], download['nvr'])
            arches[download['arch']].append(download)

        d.latest_srpm = arches['src'][0]
        del(arches['src'])

        # FIXME: This will break for things like EPEL.
        # We should get this data from somewhere else.. bodhi?
        if d.release == 'rawhide':
            branch = 'devel'
        else:
            branch = '%s-%s' % (d.release[0], d.release[1:])
            branch = branch.upper()

        d.latest_spec = 'http://cvs.fedoraproject.org/viewvc/rpms/%s/%s/%s.spec?view=markup' % (d.package, branch, d.package)
        d.arches = arches

downloads_widget = DownloadsWidget('downloads_widget')


class SourceDownloadsWidget(Widget):
    template = "mako:fedoracommunity.mokshaapps.packages.templates.source_downloads_widget"
    params = ['id', 'package', 'sources']

    def update_params(self, d):
        super(SourceDownloadsWidget, self).update_params(d)
        sources = []
        releases = []
        bodhi = get_connector('bodhi')
        dist_tags = bodhi.get_releases()
        koji = get_connector('koji')._koji_client
        koji.multicall = True
        for tag in dist_tags:
            releases.append(tag)
            if 'rawhide' not in tag:
                tag = '%s-updates' % tag
            koji.getLatestRPMS(tag, package=d.package, arch='src')

        results = koji.multiCall()
        koji.multicall = False
        for i, result in enumerate(results):
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
        ## TODO: releases dropdown
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
