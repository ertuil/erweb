import re
import importlib


from erweb.__init__ import __version__
from erweb.errequest import Request
from erweb.erconfigure import Configure
from erweb.erroute import Route
from erweb.jardb import jardb

###############################################################################
####### Response ##############################################################
###############################################################################

class Response():
    def __init__(self):
        pass

###############################################################################
####### Database ##############################################################
###############################################################################

###############################################################################
####### Template ##############################################################
############################################################################### 

###############################################################################
####### APP ###################################################################
###############################################################################

class Erweb():

    def __init__(self):
        self.router = Route()
        self.config = Configure()

    def __call__(self,env, proc):
        self.env = env
        self.proc = proc

        self.proc('200 OK', [('Content-Type', 'text/html')])

        req = Request(self.env)
        a = self.router(req)

        return [bytes(a,'utf-8')]

    def set_config(self,cfg):
        self.config.load(cfg)
        if self.config["use_interal_db"]:
            self.database = jardb(self.config["db_url"])
    

            
defaultapp = Erweb()
