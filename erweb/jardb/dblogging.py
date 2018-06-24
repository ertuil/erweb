class dblogging(object):
    '''
    logging part for database
    '''
    def __init__(self,debug = True,log = ''):
        '''
        :param debug: boolean
        :param log: file path for log file.
        '''
        self.log = log
        self.debug = debug

    def close(self):
        if self.log != '':
            self.file.close()
        
    def set_debug(self,debug):
        self.debug = debug

    def set_log(self,log):
        self.log = log
        if self.log != '':
            self.file = open(self.log,'w')

    def write_log(self,info):
        if self.log != '':
            self.file.write(info)
        elif self.debug:
            print(info)       

    def logs(self,func):
        '''
        A decorator

        If self.log is a file path,logs will be write into it.
        Otherwise if self.debug is on, logs will be printed in the terminal.

        You should know that both of them will cause the performance loss,
        especially when logs are shown in the terminal.
        '''
        def wrapper(*args, **kwargs):
            if self.log != '':
                self.file.write("Jardb: function [ %s ] \targs:\t" % func.__name__)
                self.file.write(str(args)+'\n')
            elif self.debug:
                print("Jardb: function [ %s ] \targs:" % func.__name__)
                print(args)
            return func(*args, **kwargs)
        wrapper.__doc__ = func.__doc__
        return wrapper
        

dblog = dblogging()