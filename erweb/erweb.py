import re
import importlib


from .__init__ import __version__
import erconfig as default_config


###############################################################################
####### EXPECTION #############################################################
###############################################################################

class ErwebBaseException(Exception):
    pass

class RoutePathIllegalException(ErwebBaseException):
    pass

class RouteAddfailedException(Exception):
    pass

class PageNotFonudError(Exception):
    pass

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
# '/users/admin' => [('static','users'),('static','admin')]
# '/users/<int:id>' => [('static','users'),('int','id')]
# <int:num>,<str:name>,<path:filename>,<re:[a-z]:str1> ... 

class Route():
    def __init__(self):
        self._route = {}
        self._post_route = {}
        self._get_route = {}
        self._error_route = {}

    def _parse(self,url):
        _ans = []
        _url = [x for x in re.split("/",url.strip()) if x != '']
        for _ii in _url:
            if _ii[0] == '<' and _ii[-1] == '>':
                _tmp = _ii[1:-1].split(':')
                if _tmp[0] not in ['int','str','path','re']:
                    raise RoutePathIllegalException
                _ans.append(tuple(_tmp))
            else:
                _ans.append(('static',_ii))
        return _ans

    def add_route(self,url,func,name = None,method = None):
        if not hasattr(func, '__call__') :
            raise RouteAddfailedException
        if not name:
            name = url
        if method == 'get':
            self._get_route[name] = (func,self._parse(url))
        elif method == 'post':
            self._post_route[name] = (func,self._parse(url))
        else:
            self._route[name] = (func,self._parse(url))

    def del_route(self,name,method = None):
        if method == 'get':
            self._get_route.pop(name)
        elif method == 'post':
            self._post_route.pop(name)
        else:
            self._route.pop(name)

    def __call__(self,env):
        url = env.URL
        _url = [x for x in re.split("/",url.strip()) if x != '']
        _var = {}
        if env.METHOD == 'GET':
            _tmp_route = dict(self._route,**self._get_route)
        elif env.METHOD == 'POST':
            _tmp_route = dict(self._route,**self._post_route)
        else:
            _tmp_route = self._route

        for _ii in _tmp_route.values():
            _rule = _ii[1]
            if len(_rule) > len(_url):
                continue
            _flag = True
            for jj in range(len(_rule)):
                if _rule[jj][0] == 'static' and _rule[jj][1] == _url[jj]:
                    continue
                elif _rule[jj][0] == 'static' and _rule[jj][1] != _url[jj]:
                    _flag = False
                    break
                if _rule[jj][0] == 'int' and _url[jj].isdigit():
                    _var[_rule[jj][1]] = int(_url[jj])
                    continue
                elif _rule[jj][0] == 'int' and not _url[jj].isdigit():
                    _flag = False
                    break
                if _rule[jj][0] == 'str':
                    _var[_rule[jj][1]] = _url[jj]
                    continue
                if _rule[jj][0] == 're':
                    _reg = _rule[jj][1]
                    if re.fullmatch(_reg,_url[jj]):
                        if len(_rule[jj]) > 2:
                            _var[_rule[jj][2]] = _url[jj]
                        continue
                    else:
                        _flag = False
                        break
                if _rule[jj][0] == 'path':
                    _var[_rule[jj][1]] = '/'.join(_url[jj:])
                    break
            if _flag == True:
                return _ii[0](env,_var)
        return None

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

# load config from a .py file

class Configure(dict):
    def __init__(self, *args, **kwargs):
        super(Configure, self).__init__(*args, **kwargs)
        self._default_mod = importlib.import_module("erconfig")
        self.__dict__ = self
    
    def load(self,path):
        try:
            self.mod = importlib.import_module(path)
        except :
            self.mod = self._default_mod
        self._load_config()

    def _load_config(self):
        self["version"] = __version__
        try:
            self["Database"] = getattr(self.mod,"Database")
        except AttributeError:
            self["Database"] = getattr(self._default_mod,"Database")
        print(self['Database'])
    
        
        



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
        self.config = Configure()

    def __call__(self,env, proc):
        self.env = env
        self.proc = proc

        self.proc('200 OK', [('Content-Type', 'text/html')])

        req = Request(self.env)
        a = self.router(req)

        return [bytes(a,'utf-8')]

defaultapp = Erweb()
