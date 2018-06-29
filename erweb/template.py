'''
template.py
~~~~~~~~~~~
Adapter to Jinja2 template engine.
'''

from erweb import erweb_config as app_config
from erweb.expections import PackageNotInstalledException

try:
    import jinja2
except ImportError:
    raise PackageNotInstalledException

class baseTemplate(object):
    def __init__(self):
        pass
    def render(self,file,envs):
        pass

class Jinja2Template(baseTemplate):
    def __init__(self):
        self.reload()
        app_config.add_callback(self.reload)
    
    def reload(self):
        self.path = app_config.get("TEMPLATE_ROOT")
        TemplateLoader = jinja2.FileSystemLoader(searchpath=self.path)
        self.TemplateEnv = jinja2.Environment(loader=TemplateLoader)
    
    def render(self,file,**env):
        template = self.TemplateEnv.get_template(file)
        html = template.render(**env)
        return html

default_template = Jinja2Template()



