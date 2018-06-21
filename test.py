from erweb import defaultapp,Route

route = Route()

route.add_route('/baidu.com/<int:123>/<str:name>/<re:time:[1|2|3]>',str,'main')

route.add_route('/baidu.com/',str,'main')
route.del_route('main')