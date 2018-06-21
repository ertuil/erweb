from erweb import defaultapp,Route

route = defaultapp.router
#route.add_route('/baidu.com/<int:123>/<str:name>/<re:time:[1|2|3]>',str,'main')

def aaa(req,var):
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