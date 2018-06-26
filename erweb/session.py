'''
session.py
~~~~~~~~~~~

This is handle of sessions.

'''

from erweb import erweb_config as app_config
from erweb import erweb_database


class Session():
    def __init__(self,session_id,db_class = erweb_database):
        self._session_id = session_id
        self.db = db_class

