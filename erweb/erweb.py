import re
import importlib


from erweb.__init__ import __version__
from erweb.errequest import Request
from erweb.erconfigure import Configure
from erweb.erexpection import HTTPException
from erweb.erroute import Route
from erweb.jardb import jardb

###############################################################################
####### APP ###################################################################
###############################################################################

class Erweb():

    def __init__(self):
        self.router = Route()
        self.config = Configure()

    def __call__(self,environ,start_response):
        try:
            _env = environ
            _proc = start_response
            req = Request(_env)
            res = self.router(req)
            ret = self.set_response(_proc,res)
            return ret
        except HTTPException as e:
            res = self.router.handle_error(e.status,_env)
            ret = self.set_response(_proc,res)
            return ret
        except Exception :
            res = self.router.handle_error(500,_env)
            ret = self.set_response(_proc,res)
            return ret
    
    def set_response(self,_proc,res):
        _proc(res.status,res.headers)
        return res.body

    def set_config(self,cfg):
        self.config.load(cfg)
        if self.config["use_interal_db"]:
            self.database = jardb(self.config["db_url"])
      
defaultapp = Erweb()