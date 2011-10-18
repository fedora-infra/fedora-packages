from tw.api import Widget

class PackageWidget(Widget):
    template = "mako:fedoracommunity/widgets/package/templates/package_chrome.mak"
    params = ['package_name']
    package = None

    def update_params(self, d):
        super(PackageWidget, self).update_params(d)
