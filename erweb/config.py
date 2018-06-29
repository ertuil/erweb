'''
config.py
~~~~~~~~~~~

This is the configuration manager.

'''

###############################################################################
####### Default Config ########################################################
###############################################################################

default_config_dev = {
    'DATABASE_URL'  :   'localhost',
    'DATABASE_ROOT' :   './',
    'DATABASE_USER' :   'admin',
    'DATABASE_PASSWD':  'admin',
    'DATABASE_PORT' :   3306,
    'DATABASE'      :   'sqlite3',  # sqlite3 or mysql or memery
    'DATABASE_NAME' :   'database.db',    #

    'STATIC_URL'    :   '/static/',
    'STATIC_ROOT'   :   './static',
    'HTML_ROOT'     :   './static/html',
    "TEMPLATE_ROOT" :   './static/template',

    'SECRET_KEY'    :   'erweb',

    'SESSION_NAME'  :   'session',
    'SESSION_AGE'   :   1209600,

    'CHARSET'       :   'utf-8',
    'DEBUG'         :   True
}

###############################################################################
####### Configure #############################################################
############################################################################### 

class config():
    def __init__(self):
        self._config = default_config_dev
        self._callback = {}

    def upload(self,dicts):
        for k,v in dicts.items():
            self._config[k] = v
        for func in self._callback.values():
            func()
        
    def get(self,key,default = None):
        try:
            return self._config[key]
        except KeyError:
            return default
    
    def add_callback(self,func):
        if hasattr(func,'__call__') and func.__name__ not in self._callback.keys():
            self._callback[func.__name__] = func

default_config = config()

