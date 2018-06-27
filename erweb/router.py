import re
import os.path
from erweb import erweb_config as app_config
from erweb.expections import RoutePathIllegalException,RouteAddfailedException,HTTPException
from erweb.response import ErrorResponse,STATICResponse

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
        self._error_route[404] = http_404_handle
        self._error_route[403] = http_403_handle
        self._error_route[500] = http_500_handle
        self.add_static_route()
        app_config.add_callback(self.add_static_route)
        
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

    def add_static_route(self):
        url = os.path.join(app_config.get('STATIC_URL'),"<path:filename>")
        self._route["ERWEB_STATIC"] = (static_handle,self._parse(url))

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
        
    def add_error_route(self,status,func):
        self._error_route[status] = func

    def del_route(self,name,method = None):
        if method == 'get':
            self._get_route.pop(name)
        elif method == 'post':
            self._post_route.pop(name)
        else:
            self._route.pop(name)

    def handle_error(self,status,env):
        return self._error_route[status](env)


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
            _url_len = len(_url)
            _rule_len = len(_rule)

            if _rule_len == 0:
                if  _url_len == 0:
                    return _ii[0](env,[])
                else:
                    continue                

            if _rule_len >  _url_len:
                continue

            if _rule_len < _url_len and _rule_len > 0 and _rule[-1][0] != 'path':
                continue

            _flag = True
            for jj in range(_rule_len):
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
        raise HTTPException(404)

###############################################################################
####### Error Handles #########################################################
###############################################################################

# This is the default handle for HTTP ERRORS

def http_404_handle(env,var = None):
    _info = """
    <h1> 404 Not Found!</h1>
    <p>The server is powered by erweb</p>
    """
    return ErrorResponse(_info,type = 404)

def http_403_handle(env,var = None):
    _info = """
    <h1> 403 Forbidden!</h1>
    <p>The server is powered by erweb</p>
    """
    return ErrorResponse(_info,type = 403)

def http_500_handle(env,var = None):
    _info = """
    <h1> 500 Oops!</h1>
    <p>Server crashed!</p>
    <p>The server is powered by erweb</p>
    """
    return ErrorResponse(_info,type = 405)

###############################################################################
####### STATIC_HANDLES ########################################################
###############################################################################

def static_handle(env,var = None):
    try:
        path = var['filename']
        return STATICResponse(path)

    except:
        raise HTTPException(404)