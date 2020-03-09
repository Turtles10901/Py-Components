from flask import current_app, _app_ctx_stack
from .core import _Namespaceing
class Config():
    """Object to store config for internal use"""
    pass
config = Config()
config.messages = True #set to COMPONENTS_LOG_MESSAGES in init
config.repre = False #set to COMPONENTS_RENDER_AS_REPRESENTATION in init
class FlaskComponents():
    """Add Components To App. 
    initialize with `components=FlaskComponents(app)` or with init app. Simply pass the instance  into your views as `components=components` or 'components=YourFlaskComponentsInstance`.
    """
    def __init__(self, app=None):
        """Regular init"""
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Factory init. Called by `__init__`"""
        self.use = _Namespaceing()
        app.config.setdefault('COMPONENTS_INCLUDE_BASE_COMPONENTS', True)
        app.config.setdefault('COMPONENTS_LOG_MESSAGES', True)
        app.config.setdefault('COMPONENTS_RENDER_AS_REPRESENTATION', True)
        if app.config['COMPONENTS_LOG_MESSAGES']:
            config.messages = True
        else:
            config.messages = False
        if app.config['COMPONENTS_RENDER_AS_REPRESENTATION']:
            config.repre = True
        else:
            config.repre = False
        if app.config['COMPONENTS_INCLUDE_BASE_COMPONENTS']:
            from . import base
            self.use.add(base)
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
    
    def include(self, module):
        """include a Component Pack by passing the module for the pack into the function"""
        self.use.add(module)
    def listAdded(self):
        """List all packs added using `include`"""
        return self.use.listAdded()
    

