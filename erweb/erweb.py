import re
import importlib
import base64
import hashlib
import traceback

from erweb import erweb_config as app_config
from erweb.encrypt import en_xor_str
from erweb.__init__ import __version__
from erweb.request import Request
from erweb.expections import HTTPException
from erweb.router import Route
from erweb.response import RawResponse
from erweb.cookie import set_cookies

###############################################################################
####### APP ###################################################################
###############################################################################

class Erweb():

    def __init__(self):
        self.router = Route()

    def __call__(self,environ,start_response):
        try:
            _env = environ
            _proc = start_response
            req = Request(_env)
            res = self.router(req)
            if isinstance(res,str):
                res = RawResponse(res)
            ret = self.set_response(_proc,res,req)
            return ret
        except HTTPException as e:
            print(str(e))
            traceback.print_exc()
            res = self.router.handle_error(e.status,_env)
            ret = self.set_response(_proc,res,req)
            return ret
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            res = self.router.handle_error(500,_env)
            if isinstance(res,str):
                res = RawResponse(res)
            ret = self.set_response(_proc,res,req)
            return ret
    
    def set_response(self,_proc,res,req):
        set_cookies(req.SESSION_ID,res)
        _proc(res.status,res.headers)
        return res.body

    def trans_cookies(self,cookies,headers):
        for cookie in cookies:
            (name,value,max_age,expires,path,domain,secure,httponly) = cookie
            _tmp = name + "=" + en_xor_str(value,app_config.get("SECRET_KEY"))
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
      
defaultapp = Erweb()