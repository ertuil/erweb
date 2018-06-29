import sys
sys.path.append('../')

from erweb.template import Jinja2Template

a = Jinja2Template()

print(a.render("test.tpl",name = "123456456",age = 17))