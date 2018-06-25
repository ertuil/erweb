import re
import importlib
import base64
import hashlib
import traceback


from erweb.utils import en_xor_str
from erweb.__init__ import __version__
from erweb.errequest import Request
from erweb.erconfigure import Configure
from erweb.erexpection import HTTPException
from erweb.erroute import Route
from erweb.erresponse import RawResponse
from erweb.jardb import jardb

###############################################################################
####### APP ###################################################################
###############################################################################

class Erweb():

    def __init__(self):
        self.config = Configure()
        self.router = Route(self.config)

    def __call__(self,environ,start_response):
        try:
            _env = environ
            _proc = start_response
            req = Request(_env,self.config["salt"])
            res = self.router(req)
            if isinstance(res,str):
                res = RawResponse(res)
            ret = self.set_response(_proc,res)
            return ret
        except HTTPException as e:
            print(str(e))
            traceback.print_exc()
            res = self.router.handle_error(e.status,_env)
            ret = self.set_response(_proc,res)
            return ret
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            res = self.router.handle_error(500,_env)
            if isinstance(res,str):
                res = RawResponse(res)
            ret = self.set_response(_proc,res)
            return ret
    
    def set_response(self,_proc,res):
        self.trans_cookies(res.cookies,res.headers)
        _proc(res.status,res.headers)
        return res.body

    def trans_cookies(self,cookies,headers):
        for cookie in cookies:
            (name,value,max_age,expires,path,domain,secure,httponly) = cookie
            _tmp = name + "=" + en_xor_str(value,self.config["salt"])
            if max_age != 0:
                _tmp += ";max_age="+str(max_age)
            elif expires != None:
                _tmp += ";expires="+expires
            _tmp += ";path="+path
            if domain:
                _tmp += ";domain="+domain
            if secure:
                _tmp += ";secure"
            if httponly:
                _tmp += ";httponly"      
            headers.append(("Set-Cookie",_tmp))


    def set_config(self,cfg):
        self.config.load(cfg)
        if self.config["use_interal_db"]:
            self.database = jardb(self.config["db_url"])
      
defaultapp = Erweb()