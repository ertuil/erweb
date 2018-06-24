import re
import importlib


from erweb.__init__ import __version__
from erweb.errequest import Request
from erweb.erconfigure import Configure
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
        _env = environ
        _proc = start_response

        req = Request(_env)
        res = self.router(req)

        return self.set_response(_proc,res)
    
    def set_response(self,_proc,res):
        _proc(res.status,res.headers)
        return res.body

    def set_config(self,cfg):
        self.config.load(cfg)
        if self.config["use_interal_db"]:
            self.database = jardb(self.config["db_url"])
      
defaultapp = Erweb()