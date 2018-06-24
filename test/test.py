import sys
sys.path.append('../')


from erweb import defaultapp,Route,Configure
import test_config as cfg
from erweb.jardb import jardb

route = defaultapp.router

con = defaultapp.config

con.load(cfg)

db = jardb("json://database.db")
db.create()

db.create_table('Users',{})
db.get_table('Users').add({'user':1,'secure':2})
db.save()

def aaa(req,var):
    db.get_table('Users').add({'user':1,'secure':2})
    db.save()
    return '''
          <form action="" method="post">
            <p>First name: <input type="text" name="fname" /></p>
            <p>Last name: <input type="text" name="lname" /></p>
            <input type="submit" value="Submit" />
          </form>
          '''
        

route.add_route('/index.html/<int:a>/<str:name>/<re:[a-c][1-9]:bb>',aaa,'main')
route.add_route('/page/<path:file>',aaa)
route.add_route('/index/<int:a>',aaa)