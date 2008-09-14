"""Definitions for the MyFedora quickstart templates"""
from paste.script.templates import Template, var
from tempita import paste_script_template_renderer

class MokshaAppTemplate(Template):
    _template_dir = 'templates/moksha-app'
    template_renderer = staticmethod(paste_script_template_renderer)
    summary = 'Moksha Hello World Application Template'
    #egg_plugins = ['PasteScript', 'TurboGears2']

    def pre(self, command, output_dir, vars):
        """Called before template is applied."""
        package_logger = vars['package']
        print vars
        if package_logger == 'root':
            # Rename the app logger in the rare case a project is named 'root'
            package_logger = 'app'
        vars['package_logger'] = package_logger

        template_engine = vars.setdefault('template_engine', 'genshi')

        if template_engine == 'mako':
            # Support a Babel extractor default for Mako
            vars['babel_templates_extractor'] = \
                "('templates/**.mako', 'mako', None),\n%s#%s" % (' ' * 4,
                                                                 ' ' * 8)
        else:
            vars['babel_templates_extractor'] = ''
