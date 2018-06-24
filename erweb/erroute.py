import re
from erweb.erexpection import RoutePathIllegalException,RouteAddfailedException

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