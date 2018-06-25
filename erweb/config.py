'''
config.py
~~~~~~~~~~~

This is the configuration manager.

'''

###############################################################################
####### Default Config ########################################################
###############################################################################

default_config_dev = {
    'DATABASE_URL'  :   './',
    'DATABASE_USER' :   'admin',
    'DATABASE_PASSWD':  'admin',
    'DATABASE_PORT' :   3306,
    'DATABASE'      :   'sqlite3',
    'DATABASE_NAME' :   'admin',

    'STATIC_URL'    :   '/static/',
    'STATIC_ROOT'   :   './static',

    'SECRET_KEY'    :   'erweb',

    'SESSION_NAME'  :   'sessionid',
    'SESSION_POS'   :   'DATABASE',     # 'MEMERY' or 'FILE'

    'CHARSET'       :   'utf-8'
}


###############################################################################
####### Configure #############################################################
############################################################################### 

class config():
    def __init__(self):
        self._config = default_config_dev
        self._callback = []

    def upload(self,dicts):
        for k,v in dicts.items():
            self._config[k] = v
        for func in self._callback:
            func()
        
    def get(self,key,default = None):
        try:
            return self._config[key]
        except KeyError:
            return default
    
    def add_callback(self,func):
        if hasattr(func,'__call__'):
            self._callback.append(func)

default_config = config()

