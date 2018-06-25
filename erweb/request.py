import re
import base64

from erweb import erweb_config as app_config
from erweb.encrypt import de_xor_str

###############################################################################
####### Request ###############################################################
###############################################################################

# Read information from the environ of WSGI and convert it.

class Request():

    def __init__(self,env):

        self.salt = app_config.get("SECRET_KEY")
        self.METHOD = env.get('REQUEST_METHOD',"")
        self.SERVER_PROTOCOL = env.get('SERVER_PROTOCOL',"")
        self.ACCEPT = env.get('HTTP_ACCEPT',"")
        self.ACCEPT_ENCODING = env.get('HTTP_ACCEPT_ENCODING',"")
        self.ACCEPT_LANGUAGE = env.get('HTTP_ACCEPT_LANGUAGE',"")
        self.USER_AGENT = env.get('HTTP_USER_AGENT','')
        self.URL = env.get('RAW_URI',"")
        self.REMOTE_IP = str(env.get('REMOTE_ADDR',""))+':'+str(env.get('REMOTE_PORT',""))

        tmp = re.split("[&=]",env.get('QUERY_STRING','').strip()) or []
        self.GET = dict(zip(tmp[::2],tmp[1::2]))

        tmp = re.split("[;=]",env.get('HTTP_COOKIE',"").strip())
        self._COOKIES = dict(zip(tmp[::2],tmp[1::2]))
        self.COOKIES = {}
        for k,v in self._COOKIES.items():
            self.COOKIES[k] = de_xor_str(v,self.salt)
        try:
            self.SESSION_ID = int(self.COOKIES["session_id"] or -1)
        except :
            self.SESSION_ID = -1

        try:
            _request_body_size = int(env.get('CONTENT_LENGTH',"") or 0)
        except (ValueError):
            _request_body_size = 0
        try:
            tmp = str(env.get('wsgi.input',None).read(_request_body_size))
            tmp = re.split("[&=]",tmp[2:-1].strip()) or []
            self.POST = dict(zip(tmp[::2],tmp[1::2]))
        except :
            self.POST = {}