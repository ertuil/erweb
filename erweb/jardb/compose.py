import json
from erweb.jardb.errors import DbEncodeException,DbDecodeException

class DbBaseObject(object):
    '''
    DbBaseObject is the basic interface for all elements in database
    '''
    def __init__(self):
        self.object_name = ''
        self._child_list = []

    def insert(self,db_object):
        '''
        Insert a table, config and record.

        :param db_object: a DbBaseObject object.
        '''
        self._child_list.append(db_object)

    def encode(self):
        '''
        Change the objects into python-dictionary
        '''
        pass

    def decode(self):
        '''
        Create a database from a python dictionary
        '''
        pass

    def get(self):
        pass

class Dbbase(DbBaseObject):
    '''
    Dbbase is the object for database itself.
    Tow kinds of object can be insert:
        1. DbConfig: A configuration python dictionary.It is like a record without
                     table and it is directly inserted into database
        2. DbTable: Tables in database which contains records
    '''
    def __init__(self,filepath):
        super(Dbbase,self).__init__()
        self.object_name = 'Database'
        self.file_path = filepath

    def encode(self):
        try:
            return {ob.object_name:ob.encode() for ob in self._child_list} 
        except Exception():
            raise DbEncodeException()

    def get(self):
        return self._child_list

    def find(self,name):
        '''
        Find the DbConfig or Dbtable by name.
        :param name: table or config name
        :return :return the DbConfig, Dbtable object or None 
        '''
        for ob in self._child_list:
            if ob.object_name == name:
                return ob
        return None

    def decode(self,content):
        self._child_list = []

        for k,v in content.items():
            if isinstance(v,list):
                table = DbTable(k)
                table.decode(v)
                self._child_list.append(table)
            elif isinstance(v,dict):
                config = DbConfig(k,v)
                self._child_list.append(config)
            else:
                raise DbDecodeException
    
    def remove(self,name):
        self._child_list.remove(self.find(name))
            
class DbConfig(DbBaseObject):
    '''DbConfig

    Something like application configurations, settings can be restored as a DbConfig.
    It is like a database record without table and should be unique.
    '''
    def __init__(self,name,content):
        super(DbConfig,self).__init__()
        self.object_name = name
        self._content = content # A python dictionary like {'App_name':'jardb','Version':'0.0.1'}

    def get(self):
        return self._content

    def set_content(self,content):
        self._content = content

    def encode(self):
        return self._content

class DbTable(DbBaseObject):
    '''DbTable

    The database table class in jardb.
    Fields in a table can be described by some properties in 'Unique','NotNull','AutoIncrease'

    "Unique": jardb will check the Uniqueness of certain field.
    "NotNull": jardb will check before insert.
    "AutoIncrease" : If the field is not be specified,jardb will automatical appoint one.
     
    '''
    def __init__(self,tablename,field = {}):
        super(DbTable,self).__init__()
        self.object_name = tablename
        self.field = field  # a dictionary contains the field properties like :
                            #   {'id':[AutoIncrease],'Userbane':['Unique','NotNull']}

    def get(self):
        return self._child_list # data records list 

    def encode(self):
        return [self.field,[ob.encode() for ob in self._child_list]]

    def decode(self,content):
        self.field = content[0]
        self._child_list = [DbRecord(ob) for ob in content[1]]
    
    def size(self):
        '''return the number of records'''
        return len(self._child_list)

    def set_child_list(self,content):
        '''set record list by a list
        :param content: A python list contains DbRecord objects.
        '''
        self._child_list = [ob for ob in content]

    def insert(self,db_elem):
        self._child_list.append(db_elem)

class DbRecord(DbBaseObject):
    '''
    A class represent for a database record.
    '''
    def __init__(self,content):
        super(DbRecord,self).__init__()
        self.object_name = 'Record'
        self._content = content # A python dictionary like {'User':"Chen","Password":"123456",'is_admin':True}

    def encode(self):
        return self._content
        
    def get(self):
        return self._content
    
    def set_(self,key,value):
        self._content[key] = value

    def reset(self,content):
        self._content = content
    
    def find(self,info):

        try:
            return self._content[info]
        except KeyError:
            return None
