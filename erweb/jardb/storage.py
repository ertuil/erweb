from erweb.jardb import compose
import json
import pickle
import os

class BaseStorage(object):
    '''
    Storage interface.
    '''
    def read(self):
        '''Read from file'''
        pass
    def write(self):
        '''
        First it writes data to '*.swp' file and then removes the '*.swp'
        If database file exists,it will be renamed to '.bac' as backup.
        '''
        pass

class JsonStorage(BaseStorage):
    '''Json Storage'''
    def read(self,filepath):
        with open(filepath,'r') as f:
            database = compose.Dbbase(filepath)
            database.decode(json.load(f))
            return database

    def write(self,database,filepath = None):
        if not filepath:
            filepath = database.file_path
        with open(filepath,'w') as f:
            json.dump(database.encode(),f)


class BinStorage(BaseStorage):
    '''Pickle binary Storage'''
    def read(self,filepath):
        with open(filepath,'rb') as f:
            database = compose.Dbbase(filepath)
            database.decode(pickle.load(f))
            return database

    def write(self,database,filepath = None):
        if not filepath:
            filepath = database.file_path
        with open(filepath,'wb') as f:
            pickle.dump(database.encode(),f)


class MemeryStorage(BaseStorage):
    '''Memory Storage'''
    def __init__(self):
        self._memery = {}

    def read(self,filepath = 'Memery'):
        database = compose.Dbbase('Memery')
        database.decode(self._memery)
        return database

    def write(self,database):
        self._memery = database.encode()