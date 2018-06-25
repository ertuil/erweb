import sys
sys.path.append('../')


from erweb import defaultapp
from erweb.erresponse import HTTPResponse
import test_config as cfg


defaultapp.set_config(cfg)
route = defaultapp.router

db = defaultapp.database

db.create()

db.create_table('Users',{})
db.get_table('Users').add({'user':1,'secure':2})
db.save()

def aaa(req,var):
    db = defaultapp.database
    db.get_table('Users').add({'user':2,'secure':2})
    db.save()
    a= '''<form action="" method="post">
            <p>First name: <input type="text" name="fname" /></p>
            <p>Last name: <input type="text" name="lname" /></p>
            <input type="submit" value="Submit" />
          </form>'''
    return a

def bbb(req,var):
    return HTTPResponse("index.html")

route.add_route('/index.html/<int:a>/<str:name>/<re:[a-c][1-9]:bb>',aaa,'main')
route.add_route('/page/<path:file>',aaa)
route.add_route('/index/<int:a>/',aaa)
route.add_route('/',bbb)