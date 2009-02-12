from moksha.api.widgets.containers import TabbedContainer

class SubTabbedContainer(TabbedContainer):
    template = 'mako:fedoracommunity.widgets.templates.subtabbedcontainer'

    passPathRemainder = True