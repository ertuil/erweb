import sys
sys.path.append('../')


from erweb import defaultapp
from erweb.response import HTTPResponse,FILEResponse,RedirectionResponse


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
    file = req.FILE
    print(file)
    if file :
        with open(file['file1'][0],"wb") as f:
            f.write(file['file1'][1])
    return res

def test_download(req,var):
    req = FILEResponse("./11.png")
    return req
    
def test_redict(req,var):
    req = RedirectionResponse("/index/111","301 Moved Permanently")
    return req

route.add_route('/upload',test_upload)
route.add_route('/redirect',test_redict)
route.add_route('/index.html/<int:a>/<str:name>/<re:[a-c][1-9]:bb>',aaa,'main')
route.add_route('/page/<path:file>',aaa)
route.add_route('/index/<int:a>/',aaa)
route.add_route('/',bbb)
route.add_route('/download',test_download)