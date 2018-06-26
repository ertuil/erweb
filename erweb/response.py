###############################################################################
####### Response ##############################################################
###############################################################################
import hashlib
import base64
from erweb import erweb_config as app_config

class BaseResponse():
    def __init__(self):
        self.status = "200 OK"
        self.cookies = []
        self.headers = [('Content-type', 'text/plain')]
        self.body = []

    def set_cookies(self,name,value,max_age = 300,expires = None,path='/',domain=None,secure=False,httponly=False):
        _tmp = (name,value,max_age,expires,path,domain,secure,httponly)
        self.cookies.append(_tmp)

    def del_cookies(self,name):
        self.set_cookies(name,' ',max_age=-1)

class RawResponse(BaseResponse):
    def __init__(self,path,enc = 'utf-8'):
        super(RawResponse,self).__init__()
        self.headers = [('Content-type', 'text/html')]
        self.body.append(bytes(path,enc))
    
class HTTPResponse(BaseResponse):
    def __init__(self,path):
        super(HTTPResponse,self).__init__()
        self.headers = [('Content-type', 'text/html')]
        with open(path,'rb') as f:
            self.body.append(f.read())

class ErrorResponse(BaseResponse):
    def __init__(self,status,info,enc = 'utf-8'):
        super(ErrorResponse,self).__init__()
        self.status = status
        self.headers = [('Content-type', 'text/html')]
        self.body.append(info.encode(enc))