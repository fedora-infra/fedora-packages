# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
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

from fedoracommunity.lib import app_globals
import fedoracommunity
import fedoracommunity.lib

from tg.configuration import AppConfig
from paste.deploy.converters import asbool
try:
    # TG-2.3
    from tg.i18n import ugettext
except ImportError:
    # Earlier TG2
    from pylons.i18n import ugettext


class FedoraCommunityConfig(AppConfig):
    tw2_initialized = False

    def add_tosca2_middleware(self, app):
        if self.tw2_initialized:
            return app

        from tg import config
        from tw2.core.middleware import TwMiddleware
        default_tw2_config = dict(
            default_engine=self.default_renderer,
            translator=ugettext,
            auto_reload_templates=asbool(
                self.get('templating.mako.reloadfromdisk', 'false'))
        )
        res_prefix = config.get('fedoracommunity.resource_path_prefix')
        if res_prefix:
            default_tw2_config['res_prefix'] = res_prefix
        script_name = config.get('fedoracommunity.script_name')
        if script_name:
            default_tw2_config['script_name'] = script_name
        if getattr(self, 'custom_tw2_config', None):
            default_tw2_config.update(self.custom_tw2_config)
        app = TwMiddleware(app, **default_tw2_config)
        self.tw2_initialized = True
        return app


base_config = FedoraCommunityConfig()
base_config.renderers = []
base_config.use_dotted_templatenames = True

base_config.use_toscawidgets = False
base_config.use_toscawidgets2 = True

base_config.package = fedoracommunity

# Set the default renderer
base_config.default_renderer = 'mako'
base_config.renderers.append('mako')
base_config.renderers.append('genshi')
base_config.auto_reload_templates = True
base_config.use_legacy_renderer = False

# Configure the base SQLALchemy Setup
# fix this later
base_config.use_sqlalchemy = False

# Enable profiling middleware.
base_config.profile = False

# Enable squeeze middlware
base_config.squeeze = False

base_config.disable_request_extensions = True

