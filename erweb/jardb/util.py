import re
from erweb.jardb import compose

def check_string(_str):
    '''
    A Incomplete Safety Check for filter function.
    '''
    for ii in ['import','print','input','()']:
        if _str.find(ii) != -1:
            return 'False'
    else :
        return re.sub(r'\$(\w*)',lambda m: 'ob.find(\'' + m.group(1) + '\')',_str)

def convert_set(_list,by):
    '''
    It is like the TableQuery.map function but returns a python set.
    '''
    return set([ob.find(by) for ob in _list])

def check_attr(_attr):
    '''
    Check the _attr dictionary when creating a new table.
    Legal properties are ['NotNull','Unique','AutoIncrease'].
    '''
    if not isinstance(_attr,dict):
        return False
    for _,v in _attr.items():
        if not isinstance(v,list):
            return False
        for i in v:
            if i not in ['NotNull','Unique','AutoIncrease']:
                return False
    return True

class Cache(object):
    '''
    This class helps accelerate check "Unique" and generate a new id for "AutoIncrease"
    '''
    _instance = None
    def __init__(self):
        self._auto_dict = {} # cache for "AutoIncrease"
        self._uniq_dict = {} # cache for "Unique"

    def __new__(cls, *args, **kw):
        '''
        Singleton mode
        '''
        if not cls._instance:
            cls._instance = super(Cache, cls).__new__(cls, *args, **kw)  
        return cls._instance  

    def increase(self,table,field,_list):
        '''
        This function will generate a new id number.
        :param table: Table name
        :param field: field name
        :param _list: Dbrecord lists
        :return idx: the generated id

        If table%label is not found in self._auto_dict,
        _list will help to generate the id by max_number + 1

        '''
        label = table + '%'+field
        if label not in self._auto_dict:
            _set = convert_set(_list,field)
            if _set == {None} or len(_set) == 0:
                _set = (0,)
            idx =  max(_set) + 1
            self._auto_dict[label] = idx
        else :
            idx = self._auto_dict[label] + 1
            self._auto_dict[label] = idx
        return idx

    def check_unique(self,table,field,_list,value):
        '''
        This function will check uniqueness.
        :param table: Table name
        :param field: field name
        :param _list: Dbrecord lists,
        :param value: something will be checked.
        :return flag: boolean,Unique or not.

        If table%label is not found in self._auto_dict,
        _list will help to generate the self._unqi_dict.
        '''
        label = table + '%'+field
        if label not in self._uniq_dict:
            self._uniq_dict[label] =  set([ob.find(field) for ob in _list])
        flag = value in self._uniq_dict[label]
        if not flag:
            self._uniq_dict[label].add(value)
        return flag

    def remove_label(self,table,field,value):
        '''
        Remove value from self._unqi_dict.

        :param table: Table name
        :param field: field name
        :param _list: Dbrecord lists,
        :param value: labels which will be remove from _unqi_dict.
        '''
        label = table + '%'+field
        if isinstance(value,list):
            self._uniq_dict[label] =  self._uniq_dict[label].difference(value)
        else:
            self._uniq_dict[label] = self._uniq_dict[label].difference([value])

cache = Cache()