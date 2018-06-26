import sys
sys.path.append('../')


from erweb import defaultapp
from erweb.response import HTTPResponse


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
    print(req.USER_AGENT)
    a = req.session['123']
    print(a)
    req.session['123'] = a+1
    req.session['hello'] = 'world'
    res.set_cookies('name','ertuilertuilertuil')
    return res

def test_upload(req,var):
    res = HTTPResponse("upload.html")
    return res

route.add_route('/upload',test_upload)
route.add_route('/index.html/<int:a>/<str:name>/<re:[a-c][1-9]:bb>',aaa,'main')
route.add_route('/page/<path:file>',aaa)
route.add_route('/index/<int:a>/',aaa)
route.add_route('/',bbb)