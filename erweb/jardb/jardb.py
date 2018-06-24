from erweb.jardb import compose
from erweb.jardb import storage
from erweb.jardb.util import check_attr
from erweb.jardb.errors import DbFilePathError,DbBuildError
from erweb.jardb.dblogging import dblog
from erweb.jardb.autosave import auto,file_lock
from erweb.jardb import query
import atexit

class jardb(object):
    '''jardb,the core part of this tiny database'''

    def __init__(self,filepath,autosave = False,debug = False,log = ''):
        '''
        Usage:

        :param filepath: the file path of data, It should like "json://database.db", 
                            "file://users.db",or "memery://mydatabase.db"

        :param autosave: boolean, use autosave or not.

        :param debug: echo logs in the terminal.

        :param log: A log file path.If defined,logs will be written into it.

        More details for filepath:

        Jardb support three types of storage:Json,binary file and memery.
        "json://": A json file would be create, all information can be seen.
        "file://": A binary file by pickle.dump
        "memery://": All data will not be saved as a file and would disappear after jardb quits.

        More details for autosave:

        You should understand that if you turn it on, it may cause performance 
        loss(though a little).If you turn it off,you should save your database 
        from time to time, because it will only write datas into file only once 
        before it quits.
        '''
        self._close = False
        dblog.set_debug(debug)
        dblog.set_log(log)
        self._autosave = autosave
        self._query_list = {}
        atexit.register(self.close)

        path = filepath.split('://')
        if len(path) < 2 or path[0] not in ['memery','json','file']:
            raise DbFilePathError('filepath is not correct.')
        self._type = path[0]
        self._filepath = path[1]

        if self._type == 'memery':
            self._storage = storage.MemeryStorage()
        elif self._type == 'json':
            self._storage = storage.JsonStorage()
        elif self._type == 'file':
            self._storage = storage.BinStorage()

    @dblog.logs
    def open(self):
        '''
        Initialize database by reading existed file.
        '''
        self._database = self._storage.read(self._filepath)
        auto.config(self)
        if self._autosave:
            auto.start()

    @auto.getChange
    @dblog.logs
    def create(self,_dict = {}):
        '''
        :param _dict: a python dictionary

        Initialize database by a dictionary like:
        {
            "Users":[{},[{"Name": "123", "ps": "123"}, {"Name": "1234", "ps": "1234"}]], 
            "Article":[{}, [{"Name": "xxx", "Author": "123"}]],
            "config": {"user": 1, "secure": 2}
        }

        if _dict is empty, an empty database will be create.(In most situations)
        '''
        self._database = compose.Dbbase(self._filepath)
        self._database.decode(_dict)

        auto.config(self)
        if self._autosave:
            auto.start()

    def show(self):
        '''
        A python dictionary which contains data. You can save it in any type you want,
        Or print it in terminal.
        '''
        return self._database.encode()

    def _get_query(self,name,_type):
        '''
        get DbConfig or DbTable object by name.

        :param name: name of DbConfig or DbTable.
        :param _type:"Dbconfig" or "DbTable"

        Important Information:
            Query_Object for a DbConfig or DbTable will be CREATE ONLY ONCE!
        If you try to get the second one, the first one will refresh and 
        return itself.
        '''
        try:
            ob = self._database.find(name)
            if _type == 'DbConfig' and isinstance(ob,compose.DbConfig):
                if name in self._query_list:
                    self._query_list[name].refresh()
                else:
                    self._query_list[name] = query.ConfigQuery(ob)
            elif _type == 'DbTable' and isinstance(ob,compose.DbTable):
                if name in self._query_list:
                    self._query_list[name].refresh()
                else:
                    self._query_list[name] = query.TableQuery(ob)
            else:
                raise ValueError("Can not find "+_type+" <"+name+">.")
        except ValueError as e:
            print(e)
            return None
        return self._query_list[name]

    @dblog.logs
    def get_config(self,name):
        '''
        Get a DbConfig or None
        '''
        return self._get_query(name,'DbConfig')

    @auto.getChange
    @dblog.logs
    def get_table(self,name):
        '''
        Get a DbTable or None
        '''
        return self._get_query(name,'DbTable')

    @dblog.logs
    def create_table(self,table_name,table_attr = {}):
        '''Create a new table.

        :param table_name: You know what it means.
        :param table_attr: properties for fields in this table.

        More details for table_attr:
            It is expected as a dictionary.Dictionary Key should be field name,such as
            'Users','email'. Dictionary Value should be a list contains its properties,
            such as ["AutoIncrease","Unique","NotNull"]

            You don't have to all fields.You can ignore one if it doesn't contain such 
            properties.
        
        example:
            {'id':['AutoIncrease','Unique'],'data':['NotNull','Unique']}

        Important:
            table_name will not check uniqueness. Please be careful with it.
        '''
        if len(table_attr) > 0 and check_attr(table_attr) == False:
            raise DbBuildError('Table attribute illegal.')
        if self._database == None:
            raise DbBuildError('Database is not defined.')
        table = compose.DbTable(table_name,table_attr)
        self._database.insert(table)

    @dblog.logs
    def create_config(self,config_name,config_dict):
        '''
        A Dbconfig Can be considered as a dictionary.

        :param config_name: name.
        :param config_dict: a python dictionary.

        Important:
            config_name will not check uniqueness. Please be careful with it.
        '''
        if self._database == None:
            raise DbBuildError('Database is not defined.')
        if not isinstance(config_dict,dict):
            raise DbBuildError('Config is should be a dict.')
        config = compose.DbConfig(config_name,config_dict)
        self._database.insert(config)

    @auto.getChange
    @dblog.logs
    def remove(self,name):
        if self._database.find(name):
            self._database.remove(name)
            if name in self._query_list.keys():
                self._query_list[name] = None


    @dblog.logs
    def save(self):
        '''
        Manual save data into the file.
        '''
        file_lock.acquire()
        self._storage.write(self._database)
        file_lock.release()

    @dblog.logs
    def backup(self,filepath):
        '''
        You can save the database to another name, for backup.
        Yes, it is "Save As" function.
        '''
        file_lock.acquire()
        self._storage.write(self._database,filepath)
        file_lock.release()

    def close(self):
        '''
        It notifies the auto-save thread that the main thread will quit.
        Also, it save database for the last time.

        Notice that, when jardb quit, this function will automatically 
        start thanks to 'atexit'.
        '''
        auto.set_is_run()
        if hasattr(self,'_database'):
            self.save()
        if self._close == False:
            dblog.write_log('Jardb: function [ close ]')
            dblog.close()
        self._close = True

    def get_filename(self):
        '''
        Intersting functions No.1
        '''
        return self._filepath

    def get_type(self):
        '''
        Intersting functions No.2
        '''
        return self._type

    def get_database(self):
        '''
        Intersting functions No.3
        '''
        return self._database




    