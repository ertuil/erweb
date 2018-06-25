import sys
sys.path.append('../')


from erweb import defaultapp
from erweb.erresponse import HTTPResponse
import test_config as cfg


defaultapp.set_config(cfg)
route = defaultapp.router


def aaa(req,var):

    a= '''<form action="" method="post">
            <p>First name: <input type="text" name="fname" /></p>
            <p>Last name: <input type="text" name="lname" /></p>
            <input type="submit" value="Submit" />
          </form>'''
    return a

def bbb(req,var):
    res = HTTPResponse("index.html")
    res.set_cookies('name','ertuilertuilertuil')
    return res

route.add_route('/index.html/<int:a>/<str:name>/<re:[a-c][1-9]:bb>',aaa,'main')
route.add_route('/page/<path:file>',aaa)
route.add_route('/index/<int:a>/',aaa)
route.add_route('/',bbb)