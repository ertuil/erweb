'''
database.py
~~~~~~~~~~~~

This is Database handler and package for erweb.
It is suport for mysql and sqlite3 for now.
It also provide some funcions that may help you write your sql sentenses.
For examples,please move to test/test-database.py

'''

from erweb.expections import DatabaseTypeNotSupportError
from erweb import erweb_config as app_config
import traceback

class database():
    def __init__(self):
        self._database_type = app_config.get("DATABASE")
        app_config.add_callback(self.config_reload)
        if self._database_type == "memory" or self._database_type == "sqlite3":
            import sqlite3
        elif self._database_type == "mysql":
            import pymysql
        else:
            raise DatabaseTypeNotSupportError
        
        if self._database_type == 'memory':
            self.db = sqlite3.connect(':memory:')
        elif self._database_type == "sqlite3":
            self.db = sqlite3.connect(app_config.get("DATABASE_ROOT")+app_config.get("DATABASE_NAME"))
        else:
            self.db = pymysql.connect(app_config.get("DATABASE_URL"),app_config.get("DATABASE_USER"),\
                    app_config.get("DATABASE_PASSWD"),app_config.get("DATABASE_NAME"))
        self.cur = self.db.cursor()
        
    def get_db(self):
        '''
        Get the Database hander
        '''
        return self.db

    def get_con(self):
        '''
        Get a Cursor.
        '''
        return self.cur

    def close(self):
        '''
        Close the database
        '''
        self.db.close()

    def config_reload(self):
        '''
        If change the config this function will be call automatically
        '''
        if self.db:
            self.db.close()
        self.__init__()

    def execute(self,sql):
        '''
        Execute a sql sentense.
        '''
        try:
            self.cur.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(str(e))
            traceback.print_exc()

    def get_one(self):
        '''
        Get one record from selected.
        '''
        data = self.cur.fetchone()
        return data
    
    def get_all(self):
        '''
        Get all records from selected.
        '''
        data = self.cur.fetchall()
        return data

    def drop_table(self,tablename):
        '''
        Drop a table
        '''
        sql = "DROP TABLE IF EXISTS %s" % tablename
        self.execute(sql)
    
    def del_table(self, tablename):
        '''
        Clean a table
        '''
        sql = "DELETE FROM %s" % tablename
        self.execute(sql)

    def create_table(self,tablename,field):
        '''
        Create a table
        tablename: the table name
        field: a dictionary like {"NAME":"TEXT NOT NUll","PASSWD":"TEST NOT NULL"}
        '''
        sql = "CREATE TABLE IF NOT EXISTS "+ tablename+"("
        for k,v in field.items():
            sql += k + " " + v + ","
        sql = sql[0:-1]
        sql += ");"
        self.execute(sql)

    def insert(self,tablename,field):
        '''
        Insert a record into database 
        field is a dictionary like {"NAME":"ANDY","PASSWD":"123123123"}
        '''
        sql = "INSERT INTO "+tablename+"("
        for k in field.keys():
            sql += k+","
        sql = sql[0:-1]
        sql += ") VALUES ("

        for v in field.values():
            if isinstance(v,str):
                sql += "'"+v+"'"+","
            else:
                sql += str(v)+","
        sql = sql[0:-1]
        sql += ")"
        self.execute(sql)

    def select(self,tablename,field,limit = None):
        '''
        Select some records
        field is a list like ["NAME","PASSWD"]
        limit is a part of sql sentense behind the 'WHERE' like "NAME = ANDY"
        '''
        sql = "SELECT "
        for v in field:
            sql += v + ","
        sql = sql[0:-1]
        sql += " FROM "+tablename
        if limit:
            sql += " WHERE " + limit
        print(sql)
        self.execute(sql)
        return self.get_all()
    
    def update(self,tablename,sent,limit = None):
        '''
        Update some records
        sent is a sql sentense like "NAME = ANDY AND PASSWD = '11111'"
        limit is a part of sql sentense behind the 'WHERE'
        '''
        sql = "UPDATE "+tablename+" SET "+sent
        if limit:
            sql += " WHERE "+limit
        print(sql)
        self.execute(sql)
        return self.get_all()
    
    def delete(self,tablename,limit = None):
        '''
        Delete some records
        limit is a part of sql sentense behind the 'WHERE' like "NAME = ANDY"
        '''
        sql ="DELETE FROM "+tablename
        if limit:
            sql += " WHERE " + limit
        print(sql)
        self.execute(sql)
        return self.get_all()

default_database = database()