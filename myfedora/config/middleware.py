from myfedora.config.app_cfg import base_config
from myfedora.config.environment import load_environment

make_base_app = base_config.setup_tg_wsgi_app(load_environment)

def make_app(global_conf, full_stack=True, **app_conf):

    from moksha.middleware import MokshaMiddleware

    app = make_base_app(global_conf, full_stack=full_stack, 
                        wrap_app=MokshaMiddleware, **app_conf)

    if base_config.squeeze:
        from repoze.squeeze.processor import ResourceSqueezingMiddleware
        app = ResourceSqueezingMiddleware(
                app,
                cache_dir='public/cache',
                url_prefix='/cache/',
                )

    ## Profiler
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
