from myfedora.config.app_cfg import base_config
from myfedora.config.environment import load_environment

make_base_app = base_config.setup_tg_wsgi_app(load_environment)

def make_app(global_conf, full_stack=True, **app_conf):
    app = make_base_app(global_conf, full_stack=full_stack, **app_conf)

    # Wrap your base turbogears app with custom middleware here

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
