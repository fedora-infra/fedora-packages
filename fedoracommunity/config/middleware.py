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

from fedoracommunity.config.app_cfg import base_config
from fedoracommunity.config.environment import load_environment

import tg
tg_version_tuple = tuple(map(int, tg.__version__.split('.')))

make_base_app = base_config.setup_tg_wsgi_app(load_environment)

def make_app(global_conf, full_stack=True, **app_conf):
    from moksha.middleware import make_moksha_middleware
    from fedoracommunity.connectors.api.mw import FCommConnectorMiddleware

    def make_middleware(app):
        if tg_version_tuple < (2, 1):
            app = base_config.add_tosca2_middleware(app)

        app = FCommConnectorMiddleware(app)
        app = make_moksha_middleware(app, tg.config)
        return app

    app = make_base_app(global_conf,
                        wrap_app=make_middleware,
                        full_stack=full_stack,
                        **app_conf)

    if base_config.squeeze:
        from repoze.squeeze.processor import ResourceSqueezingMiddleware
        app = ResourceSqueezingMiddleware(
                app,
                cache_dir='public/cache',
                url_prefix='/cache/',
                )

    if base_config.profile:
        from repoze.profile.profiler import AccumulatingProfileMiddleware
        app = AccumulatingProfileMiddleware(
                app,
                log_filename='profile.log',
                discard_first_request=True,
                cachegrind_filename='./cachegrind.out',
                flush_at_shutdown=True,
                path='/__profile__'
                )

    return app
