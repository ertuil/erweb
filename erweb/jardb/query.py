from erweb.jardb import compose
from erweb.jardb.util import cache,check_string,convert_set
from erweb.jardb.errors import DbInsertException,DbInsertNotNullExcption,DbInsertUniqueExcption
from erweb.jardb.dblogging import dblog
from erweb.jardb.autosave import auto

class BaseQuery(object):
    '''
    A interface for query object.
    most database operation will be defined below.

    emmmm......
    '''
    def __init__(self,db_elem):
        self._origin = db_elem

    def value(self):
        pass
    def remove(self):
        pass
    def add(self):
        pass    
    def refresh(self):
        pass

class ConfigQuery(BaseQuery):
    '''
    Query and other operations for DbConfig.
    Dbconfig is just like a enclosure for python dictionary.
    '''

    def __init__(self,db_elem):
        '''
        :param db_elem: A DbConfig object.
        '''
        super(ConfigQuery,self).__init__(db_elem)
        self._content = db_elem.get()
    
    def value(self):
        '''
        :return : the contents in the DbConfig
        '''
        return self._content

    @dblog.logs
    def refresh(self):
        '''
        Actually it does nothing...
        lol...
        '''
        self._content = self._origin.get()
    
    @auto.getChange
    @dblog.logs
    def add(self,info):
        '''
        Both insert and update the Dbconfig object.

        :param info: A dictionary.

        Each pair in 'info' will be added or
        change the value in DbConfig

        '''
        if not isinstance(info,dict):
            raise TypeError("Param should be dict.")
        for k,v in info.items():
            self._content[k] = v
        self._origin.set_content(self._content)

    @auto.getChange
    @dblog.logs
    def remove(self,info):
        '''
        Remove attrbutions in the Dbconfig.
        :param info: string or list represent the key(s) in Dbconfig
        '''
        if isinstance(info,list):
            for k in info:
                try:
                    self._content.pop(k)
                except KeyError:
                    pass
        elif isinstance(info,str):
            try:
                self._content.pop(info)
            except KeyError:
                pass
        else:
            raise TypeError("Param should be list or basestring.")
        self._origin.set_content(self._content)

    @dblog.logs
    def has(self,key):
        '''
        Find a key in the Dbconfig.

        :param key: A string for key
        :return :boolean
        '''
        return key in self._content
    
    @dblog.logs
    def get(self,key):
        '''
        Get the value in Dbconfig
        :param key: A string for key
        '''
        try:
            return self._content[key]
        except KeyError:
            return None

class TableQuery(BaseQuery):
    '''
    Operations for DbTable!
    '''
    def __init__(self,db_elem):
        '''
        :param db_elem: A DbTable object.

        self._content is lists for the selected records.
        '''
        super(TableQuery,self).__init__(db_elem)
        self._attr = db_elem.field
        self._content = [ob for ob in db_elem.get()]
        self._cache = cache 

    @dblog.logs
    def refresh(self):
        '''
        Now select every records in this table.
        '''
        self._content = [ob for ob in self._origin.get()]

    def value(self):
        '''
        :return : all data that is selected.
        '''

        return [ob.get() for ob in self._content]

    @dblog.logs
    def map(self,field):
        """
        Given a field name, and return all values of this field.
        It is like a sql sentense:'select $field from $currect.table;'

        :param field: A field name
        :return : A list for result.
        """
        if not isinstance(field,str):
            raise TypeError("Param should be string.")
        else:
            return [ob.find(field) for ob in self._content]

    @dblog.logs
    def find(self,info):
        """
        Select some records by a dict.

        :param info: a dictionary contains conditions,
                    such as {'User_id':1533,'User_name':'ertuil'} 
                    or {'Math':100,'English':80}

        :return : TableQuery object itself

        Example: 
            sql : 'select * from table_name where a = 1 and b = 2;' 
            jardb: col = db.get_table(table_name).find({'a':1,'b':2}).value()
        """
        if not isinstance(info,dict):
            raise TypeError("Param should be dict.")
        else:
            for k,v in info.items():
                self._content = [ob for ob in self._content if ob.find(k) == v]
            return self

    @dblog.logs
    def filter(self,info):
        """
        filter is the most useful method to select records for it support 
        python-like query sentenses.

        :param info: A string with command. 
                    Such as"$User == 'robot' and $age == 13",
                    or "$Math > 90 and $Chinese > 90"

        :return : TableQuery object itself

        Example:
            sel: 'select * from table_name where Math > 90 and Chinese > 90;'
            jardb: col = db.get_table(table_name).filter("$Math > 90 and $Chinese > 90").value()

        Tips for security:
            Never expose this function to your clients.
            Remember to check the commands.
            Because It is dangerous and can cause something unexpected.
        """
        if not isinstance(info,str):
            raise TypeError("Param should be string.")
        else:
            info = check_string(info)
            self._content = [ob for ob in self._content if eval(info) ]
            return self

    @dblog.logs
    def size(self):
        """
        :return : number of currectly selected recoreds.
        """
        return len(self._content)
    
    @dblog.logs
    def sort(self,by,res = False):
        """ 
        
        :param by: A field which will be used to sort.
        :param res: reverse the result
        :return : TableQuery object itself
        """
        self._content = sorted(self._content,key = lambda x: x.find(by),reverse=res)
        return self

    @dblog.logs
    def get(self,num = 1):
        '''
        Select the top K records.

        :param num: A number
        :return : TableQuery object itself
        '''
        if num < self.size():
            self._content = self._content[0:num]
        return self

    @auto.getChange
    @dblog.logs
    def add(self,_dict):
        '''
        Insert a new record into table.

        :param _dict: A record dict like {'Username':"123",'ps':'123','admin':False}
        :return : TableQuery object itself
        :error DbInsertNotNullExcption: Doesn't specialize the "NotNull" field.
        :error DbInsertUniqueExcption: "Unique" field is duplicate.

        Before insert,the new record will be check for "Unique", "NotNull" and "AutoIncrease"

        A new Exception will be raised if it doesn't pass the examination.

        '''
        for attr_key,attr_val in self._attr.items():
            if 'NotNull' in attr_val and attr_key not in _dict:
                raise DbInsertNotNullExcption(attr_key+' field is None')
            if 'AutoIncrease' in attr_val and attr_key not in _dict:
                _dict[attr_key] = self._cache.increase(self._origin.object_name,attr_key,self._origin.get())
            if 'Unique' in attr_val and attr_key in _dict :
                if self._cache.check_unique(self._origin.object_name,attr_key,self._origin.get(),_dict[attr_key]):
                    raise DbInsertUniqueExcption('Unique Field is not Unique')

        rd = compose.DbRecord(_dict)
        self._origin.insert(rd)
        self._content.append(rd)
        return self

    @auto.getChange
    @dblog.logs
    def remove(self):
        '''
        Remove selected records.
        
        :return : TableQuery object itself
        '''
        for k,v in self._attr.items():
            if 'Unique' in v:
                self._cache.remove_label(self._origin.object_name,k,[ob.find(k) for ob in self._content])

        self._content = list(set(self._origin.get()).difference(set(self._content)))
        self._origin.set_child_list(self._content)
        return self

    @auto.getChange
    @dblog.logs
    def update(self,dicts):
        '''
        Update selected records.

        :param dicts: A dictionary
        :return : TableQuery object itself

        Example:
            db.get_table(table_name).find({'UserName':Robot}).update({{'Birthday':'1970.01.01'}})
        '''
        for k,v in dicts.items():
            if k in self._attr and 'Unique' in self._attr[k]:
                if self.size() > 1 or v in convert_set(self._origin.get(),k):
                    raise DbInsertUniqueExcption('Unique Field is not Unique.')
            for ob in self._content:
                ob.set_(k,v)
        return self  