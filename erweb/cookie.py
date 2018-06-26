'''
session.py
~~~~~~~~~~~

This is handle of sessions.

'''
from erweb import erweb_config as app_config
from erweb.encrypt import en_xor_str,de_xor_str
from erweb.expections import CookieTooLargeException

def get_cookies(_cookies):
    COOKIES = {}
    for k,v in _cookies.items():
        COOKIES[k] = de_xor_str(v,app_config.get("SECRET_KEY"))
    print(COOKIES)
    return COOKIES

def set_cookies(session_id,response):
    headers = response.headers
    cookies = response.cookies
    if session_id < 0:
        cookies.append(("session_id",str(-session_id),app_config.get("SESSION_AGE"),None,'/',None,False,True))
    
    for cookie in cookies:
        (name,value,max_age,expires,path,domain,secure,httponly) = cookie
        if len(value) > 2000:
            raise CookieTooLargeException
        _tmp = name + "=" + en_xor_str(value,app_config.get("SECRET_KEY"))
        if max_age != 0:
            _tmp += ";Max-Age = "+str(max_age)
        elif expires != None:
            _tmp += ";Expires="+expires
        _tmp += ";Path="+path
        if domain:
            _tmp += ";Domain="+domain
        if secure:
            _tmp += ";SECURE"
        if httponly:
            _tmp += ";HTTPONLY"      
        headers.append(("Set-Cookie",_tmp))