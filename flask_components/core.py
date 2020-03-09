import importlib, sys
from markupsafe import Markup, escape

def message(*args, **kwargs):
    """Wrapper around print() to only print if COMPONENTS_LOG_MESSAGES is set to true"""
    from .components import config
    if config.messages == True:
        print(*args, **kwargs)
    pass

class _Namespaceing():
    """Internal class for namespacing in templates"""
    def __init__(self):
        self.registry = {}
    def add(self, module):
        self.registry[str(module.__packname__)] = module
    def __getattr__(self, name):
        if name == "registry":
            return object.__getattribute__(self, 'registry')
        return self.registry[name]
    def listAdded(self):
        result = [self.registry[key].__packname__ for key in self.registry]
        return result

class Component():
    """The Base Component that all Components inherit from"""
    registry = {}
    def __init__(self, *args, **kwargs):
        self.args = args or []
        self.kwargs = kwargs or {}
    def __init_subclass__(cls, **kwargs): #registry
        super().__init_subclass__(**kwargs)
        module = sys.modules[cls.__module__]
        if module.__packtype__ == 'Component Pack':
            packversion = module.__packversion__
            packname = module.__packname__
            if packname not in Component.registry:
                Component.registry[packname] = []
                message('Registered Component Package: ' + packname  + " v" + packversion)
                module.__components__ = []
            if cls not in Component.registry[packname]:
                Component.registry[packname].append(cls)
                module.__components__.append(cls)
                message('Registered Component from package \''+ packname +'\': ' + cls.__name__)
        
    def render(self, *args, **kwargs):
        """Render The Component"""
        if self.__html__(*args, **kwargs) is not None:
            html = self.__html__(*args, **kwargs)
        else:
            html = '<!-- Component ' + self.__class__.__name__ + ' has failed rendering -->'
        
        return html
    def __html__(self):
        """Return the HTML as a string for the component to be rendered"""
        return NotImplemented
    def __css__(self):
        """Return the CSS as a string for the component to be rendered. Used by CssComponent from the base Component Pack"""
        return ''
    def __call__(self, *args, **kwargs):
        from .components import config
        if config.repre == True:
            return self.render(*args, **kwargs)
        else:
            return Markup(self.render(*args, **kwargs))
    def __repr__(self):
        return '<Component ' + str(self.__class__.__name__) + '>'
class Namespace():
    def __init__(self, name):
        self._name = name