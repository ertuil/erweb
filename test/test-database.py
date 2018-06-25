import sys
sys.path.append('../')

from erweb import erweb_config as app_config
from erweb.database import default_database as dfd

app_config.upload({"DATABASE":'sqlite3'})

dfd.create_table("USERS",{"NAME":"TEXT NOT NUll","PASSWD":"TEST NOT NULL"})

dfd.insert("USERS",{"NAME":"ANDY","PASSWD":"123123123"})

dfd.execute("INSERT INTO USERS (NAME,PASSWD) VALUES ('ertuil','123')")

#dfd.execute("SELECT NAME FROM USERS")

dfd.update("USERS","PASSWD = 'hello'","NAME = 'ertuil'")
data = dfd.select("USERS",["NAME","PASSWD"])
print(data)
#data = dfd.get_all()
dfd.delete("USERS","PASSWD = 'hello'")
data = dfd.select("USERS",["NAME","PASSWD"])
print(data)


