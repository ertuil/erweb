

import re

from __init__ import *


###############################################################################
####### Request ###############################################################
###############################################################################

class Request():

    def __init__(self,env):

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
        self.COOKIES = dict(zip(tmp[::2],tmp[1::2]))
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

###############################################################################
####### Route #################################################################
###############################################################################

# '/' => [('/',-1)]
# '/users/admin' => [('users','static'),('admin','static')]
# '/users/<int:id>' => [('users','static'),('id','int')]




class Route():
    def __init__(self):
        self._route = {}

    def _parse(self,url):
        _ans = []
        _url = [x for x in re.split("/",url.strip()) if x != '']
        for _ii in _url:
            if _ii[0] == '<' and _ii[-1] == '>':
                _tmp = _ii[1:-1].split(':')
                if _tmp[0] not in ['int','str','path','file','re']:
                    raise RoutePathIllegalException
                _ans.append(tuple(_tmp))
            else:
                _ans.append((_ii,'static'))
        return _ans

    def add_route(self,url,func,name = None):
        if not hasattr(func, '__call__') :
            raise RouteAddfailedException
        if not name:
            name = url
        self._route[name] = (func,self._parse(url))
        print(self._route)

    def del_route(self,name):
        self._route.pop(name)
        print(self._route)

    def get_func(self,url):
        pass




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
####### Configure #############################################################
############################################################################### 


###############################################################################
####### Session & Cookies #####################################################
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

    def __call__(self,env, proc):
        self.env = env
        self.proc = proc
        self.proc('200 OK', [('Content-Type', 'text/html')])
        req = Request(self.env)
        print(req.POST)
        print(req.SESSION_ID)
        a = '''
          <form action="" method="post">
        <p>First name: <input type="text" name="fname" /></p>
        <p>Last name: <input type="text" name="lname" /></p>
        <input type="submit" value="Submit" />
          </form>
          '''

        return [bytes(a,'utf-8')]

defaultapp = Erweb()
