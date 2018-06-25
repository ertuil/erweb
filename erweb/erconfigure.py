import erweb.default_config as default_config
from erweb.__init__ import __version__

###############################################################################
####### Configure #############################################################
############################################################################### 

# load config from a .py file

class Configure(dict):
    def __init__(self, *args, **kwargs):
        super(Configure, self).__init__(*args, **kwargs)
        self.__dict__ = self
        self._default_config = default_config
    
    def load(self,mod):
        try:
            self.mod = mod
        except :
            self.mod = self._default_config
        self._load_config()

    def _get_settings(self,key):
        try:
            self[key] = getattr(self.mod,key)
        except AttributeError:
            self[key] = getattr(self._default_config,key)

    def _load_config(self):
        self["version"] = __version__
        config_list = ["URLs","salt","db_url","use_interal_db"]
        for tt in config_list:
            self._get_settings(tt)
    
    def reload(self,cfg = None):
        self.__dict__ = {}
        if cfg:
            self.load(cfg)
        
    
    