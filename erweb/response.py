###############################################################################
####### Response ##############################################################
###############################################################################
import hashlib
import base64
import os.path
from erweb.expections import HTTPException
from erweb import erweb_config as app_config

class BaseResponse():
    def __init__(self):
        self.status = response_type[200]
        self.cookies = []
        self.headers = [('Content-type', 'text/plain')]
        self.body = []

    def set_cookies(self,name,value,max_age = 300,expires = None,path='/',domain=None,secure=False,httponly=False):
        _tmp = (name,value,max_age,expires,path,domain,secure,httponly)
        self.cookies.append(_tmp)

    def del_cookies(self,name):
        self.set_cookies(name,' ',max_age=-1)

class RawResponse(BaseResponse):
    def __init__(self,path,enc = 'utf-8',type = 200):
        super(RawResponse,self).__init__()
        self.status = response_type[type]
        self.headers = [('Content-type', 'text/html')]
        self.body.append(bytes(path,enc))
    
class HTTPResponse(BaseResponse):
    def __init__(self,path,type = 200):
        path = os.path.join(app_config.get("HTML_ROOT"),path)
        super(HTTPResponse,self).__init__()
        self.status = response_type[type]
        self.headers = [('Content-type', 'text/html')]
        with open(path,'rb') as f:
            self.body.append(f.read())

class STATICResponse(BaseResponse):
    def __init__(self,path,type = 200):
        super(STATICResponse,self).__init__()
        path = os.path.join(app_config.get("STATIC_ROOT"),path)
        pax = os.path.splitext(path)[1]
        self.status = response_type[type]
        if pax in file_type.keys():
            self.headers = [('Content-type', file_type[pax])]
        else:
            self.headers = [('Content-type', 'application/octet-stream')]
        with open(path,'rb') as f:
            self.body.append(f.read())
        
class FILEResponse(BaseResponse):
    def __init__(self,path,type = 200):
        super(FILEResponse,self).__init__()
        filename = os.path.split(path)
        self.status = response_type[type]
        self.headers = [('Content-type', 'application/octet-stream'),("Content-disposition","attachment;filename="+filename[1])]
        try:
            with open(path,'rb') as f:
                self.body.append(f.read())
        except :
            raise HTTPException('404 NOT FOUND',404)

class RedirectionResponse(BaseResponse):
    def __init__(self,url,type = 301):
        super(RedirectionResponse,self).__init__()
        self.status = response_type[type]
        self.headers = [('Content-type', 'text/html'),("Location",url)]

class ErrorResponse(BaseResponse):
    def __init__(self,info,enc = 'utf-8',type = 500):
        super(ErrorResponse,self).__init__()
        self.status = response_type[type]
        self.headers = [('Content-type', 'text/html')]
        self.body.append(info.encode(enc))


###############################################################################
####### FILE TYPE #############################################################
###############################################################################

file_type = {
    ".html" :  "text/html",
    ".xhtml"  :  "text/html",
    ".htm"  :  "text/html",
    ".htx"  :  "text/html",
    ".jsp"  :  "text/html",

    ".js"   :   "application/x-javascript",
    ".css"  :   "text/css",
    "json"  :   "text/plain",

    ".svg"  :   "text/xml",
    ".xml"  :   "text/xml",
    ".math"  :   "text/xml",

    ".tif"  :   "image/tiff",
    ".tiff"  :   "image/tiff",
    ".asp"  :   "text/asp",
    ".bmp"  :	'application/x-bmp',
    ".png"	:   "image/png",
    ".jpe"	:   "image/jpeg",
    ".jpeg"	:   "image/jpeg",
    ".jpg"	:   "image/jpeg",
    ".gif"	:   "image/gif",
    ".ico"	:   "image/x-icon",

    ".java" :   "java/*",
    ".class" :   "java/*",

    ".avi"  :   "video/avi",
    ".m4e"  :	"video/mpeg4",
    ".movie":	"video/x-sgi-movie",
    ".mp4"  :	"video/mpeg4",
    ".mpeg" :	"video/mpg",
    ".wmv"	:   "video/x-ms-wmv",

    ".m3u"  :   "audio/mpegurl",
    ".mp3"  :  	"audio/mp3",
    ".mpga" :	"audio/rn-mpeg",
    ".snd"  :	"audio/basic",
    ".wav"  :	"audio/wav",

    ".exe"  :	"application/x-msdownload",
    ".pdf"	:   "application/pdf"
}

response_type = {
    100 :   "100 Continue",
    101 :   "101 Switching Protocols",
    102 :   "102 Processing",

    200 :   "200 OK",
    201 :   "201 Created",
    202 :   "202 Accepted",
    203 :   "203 Non-Authoritative Information",
    204 :   "204 No Content",
    205 :   "205 Reset Content",
    206 :   "206 Partial Content",
    207 :   "207 Multi-Status",

    300 :   "300 Multiple Choices",
    301 :   "301 Moved Permanently",
    302 :   "302 Move temporarily",
    303 :   "303 See Other",
    304 :   "304 Not Modified",
    305 :   "305 Use Proxy",
    306 :   "306 Switch Proxy",
    307 :   "307 Temporary Redirect",

    400 :   "400 Bad Request",
    401 :   "401 Unauthorized",
    402 :   "402 Payment Required",
    403 :   "403 Forbidden",
    404 :   "404 Not Found",
    405 :   "405 Method Not Allowed",
    406 :   "406 Not Acceptable",
    407 :   "407 Proxy Authentication Required",
    408 :   "408 Request Timeout",
    409 :   "409 Conflict",
    410 :   "410 Gone",
    411 :   "411 Length Required",
    412 :   "412 Precondition Failed",
    413 :   "413 Request Entity Too Large",
    414 :   "414 Request-URI Too Long",
    415 :   "415 Unsupported Media Type",
    416 :   "416 Requested Range Not Satisfiable",
    417 :   "417 Expectation Failed",
    421 :   "421 too many connections",
    422 :   "422 Unprocessable Entity",
    423 :   "423 Locked",
    424 :   "424 Failed Dependency",
    425 :   "425 Unordered Collection",
    426 :   "426 Upgrade Required",
    449 :   "449 Retry With",
    451 :   "451 Unavailable For Legal Reasons",

    500 :   "500 Internal Server Error",
    501 :   "501 Not Implemented",
    502 :   "502 Bad Gateway",
    503 :   "503 Service Unavailable",
    504 :   "504 Gateway Timeout",
    505 :   "505 HTTP Version Not Supported",
    506 :   "506 Variant Also Negotiates",
    507 :   "507 Insufficient Storage",
    508 :   "509 Bandwidth Limit Exceeded",
    510 :   "510 Not Extended",
    600 :   "600 Unparseable Response Headers",
}