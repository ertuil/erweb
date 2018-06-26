'''
session.py
~~~~~~~~~~~

This is handle of sessions.

'''
import json
import datetime
import re
import time

from erweb import erweb_config as app_config
from erweb import erweb_database
from erweb.expections import GetSessionException


class Session():
    def __init__(self,session_id):
        self._dicts = {}
        self.session_id = session_id
        self.db = erweb_database
        self.db.create_table("ERWEB_SESSION",{"SESSION_ID":"INTEGER PRIMARY KEY AUTOINCREMENT","DATA":"TEXT NOT NUll","EXPIRE":"INTEGER NOT NULL"})

        if self.session_id == 0:
            self.db.insert("ERWEB_SESSION",{"DATA":"{\"123\":123}","EXPIRE":int(time.time())+ app_config.get("SESSION_AGE")})
            self.session_id = self.db.select("ERWEB_SESSION",["MAX(SESSION_ID)"])[0][0]
        
        try:
            self._record = self.db.select("ERWEB_SESSION",["*"],"SESSION_ID = "+str(self.session_id))[0]
            self._dicts = json.loads(self._record[1])
            self._expire = self._record[2]

        except:
            raise GetSessionException
        
    def __getitem__(self,key):
        if self._dicts == None:
            self._record = self.db.select("ERWEB_SESSION",["*"],"SESSION_ID = "+str(self.session_id))[0]
            self._dicts = json.loads(self._record[1])
        return self._dicts[key]

    def __setitem__(self,key,value):
        self._dicts[key] = value
        _tmp = json.dumps(self._dicts)
        _tmp = re.sub(r"['\"]","\"",_tmp)
        self.db.update("ERWEB_SESSION","DATA = '"+_tmp+"'","SESSION_ID = "+str(self.session_id))
    
    def clean_session(self):
        self.db.delete("ERWEB_SESSION","EXPIRE < "+ str(int(time.time())))