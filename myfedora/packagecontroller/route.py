class Route(object):
    def __init__(self, default_template):
        self._default_template = default_template

    def get_default_template(self):
        return self._default_template

    def default(self, dict, *args, **kw):
        dict['tg_template'] = self.get_default_template()
        
        return dict
