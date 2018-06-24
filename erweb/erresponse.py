###############################################################################
####### Response ##############################################################
###############################################################################
import hashlib

class BaseResponse():
    def __init__(self):
        self.status = "200 OK"
        self.cookies = []
        self.headers = [('Content-type', 'text/plain')]
        self.body = []

    def set_cookies(self,name,value,max_age = 0,expires = None,path='/',domain=None,secure=False,httponly=False):
        sha = hashlib.sha256()
        sha.update(value.encode())
        _tmp = name+"="+sha.hexdigest()
        if max_age != 0:
            _tmp += ";max_age="+str(max_age)
        elif expires == None:
            _tmp += ";expires="+expires
        _tmp += ";path="+path
        if domain:
            _tmp += ";domain="+domain
        if secure:
            _tmp += ";secure"
        if httponly:
            _tmp += ";httponly"        

        self.headers.append(("Set-Cookie",_tmp))

    def del_cookies(self,name):
        self.set_cookies(name,' ',max_age=-1)

class RawResponse(BaseResponse):
    def __init__(self,path):
        super(RawResponse,self).__init__()
        self.headers = [('Content-type', 'text/html')]
        self.body.append(bytes(path,'utf-8'))
    
class HTTPResponse(BaseResponse):
    def __init__(self,path):
        super(HTTPResponse,self).__init__()
        self.headers = [('Content-type', 'text/html')]
        with open(path,'rb') as f:
            self.body.append(f.read())

class ErrorResponse(BaseResponse):
    def __init__(self,status,info):
        super(ErrorResponse,self).__init__()
        self.status = status
        self.headers = [('Content-type', 'text/html')]
        self.body.append(info.encode())

