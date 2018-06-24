import threading
import json
import pickle
import time
import os

from  erweb.jardb import storage
from erweb.jardb.dblogging import dblog

class Autosave(threading.Thread):
    '''
    A thread class for automatical save database file from memery.
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self.need_change = False
        self._is_run = threading.Event()    # Should be Set before Main-Thread quits.
        self._is_run.set()
        self.save_lock = threading.Lock()
        self.daemon = True

    def config(self,jardb):
        ''' A configuration for class autosave.

        :param jardb: A jardb object.
        '''
        self._object = jardb
        self._type = jardb.get_type()
        self._filename = jardb.get_filename()
        self._database = jardb.get_database()
        self._is_run.set()

    def getChange(self,func):
        '''
        A Decorator which notifies the database has been changed.
        '''
        def wrapper(*args, **kwargs):
            self.save_lock.acquire()
            try:
                ans = func(*args, **kwargs)
            except Exception as e:
                self.need_change = True
                self.save_lock.release()
                dblog.write_log("Jardb: Error!")
                dblog.write_log(e.args)

                return None
            self.need_change = True
            self.save_lock.release()
            return ans
        wrapper.__doc__ = func.__doc__
        return wrapper

    def set_is_run(self):
        '''Inform that Main thread is going to quit'''
        self._is_run.clear()

    def run(self):
        while self._is_run.is_set():
            if self.need_change:
                self.save_lock.acquire()
                self._backup = self._object.show()
                self.need_change = False
                self.save_lock.release()
                file_lock.acquire()
                if self._type == 'json':
                    with open(self._filename+'.swp','w') as f:
                        json.dump(self._backup,f)
                elif self._type == 'file':
                    with open(self._filename+'.swp','wb') as f:
                        pickle.dump(self._backup,f)
                if os.path.exists(self._filename+'.bac'):
                    os.remove(self._filename+'.bac')
                if os.path.exists(self._filename):
                    os.rename(self._filename,self._filename+'.bac')
                os.rename(self._filename+'.swp',self._filename)
                file_lock.release()

            for i in range(0,5):
                if self._is_run.is_set():
                    time.sleep(1)
                # else :
                    # break

           
auto = Autosave()

file_lock = threading.Lock()

