from fedoracommunity.config.app_cfg import base_config
from fedoracommunity.config.environment import load_environment
from moksha.middleware import (MokshaMiddleware, MokshaConnectorMiddleware,
                              MokshaExtensionPointMiddleware)

from paste.cascade import Cascade

make_base_app = base_config.setup_tg_wsgi_app(load_environment)

def fc_middleware_wrapper(app):
    app = MokshaMiddleware(app)
    app = MokshaConnectorMiddleware(app)
    app = MokshaExtensionPointMiddleware(app)

    return app

def make_app(global_conf, full_stack=True, **app_conf):
    app = make_base_app(global_conf, wrap_app=fc_middleware_wrapper,
                        full_stack=True,
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
                flush_at_shutdown=True,
                path='/__profile__'
                )

    return app
