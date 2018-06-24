
class DbBaseException(Exception):
    '''
    Basic Exception in jardb.
    '''
    def __init__(self,err = ''):
        Exception.__init__(self,err)

class DbFilePathError(DbBaseException):
    '''
    Raise when unable to get type and filename in jardb.__init__()
    '''
    def __init__(self,err = ''):
        Exception.__init__(self,err)

class DbBuildError(DbBaseException):
    '''
    Raise when unable to build database models by files.
    '''
    def __init__(self,err = ''):
        Exception.__init__(self,err)

class DbIOException(DbBaseException):
    '''
    Raise when fail in write or read a file.
    '''
    def __init__(self,err = ''):
        Exception.__init__(self,err)

class DbDecodeException(DbBaseException):
    '''
    Decode Exception.
    '''
    def __init__(self,err=''):
        Exception.__init__(self,err)

class DbEncodeException(DbBaseException):
    '''
    Encode Exception.
    '''
    def __init__(self,err=''):
        Exception.__init__(self,err)

class DbFilterException(DbBaseException):
    '''
    Filter is a very flexible way to query.
    23333 Exceptions may occur
    '''
    def __init__(self,err=''):
        Exception.__init__(self,err)

class DbInsertException(DbBaseException):
    '''
    Basic Exception in insert a record.
    '''
    def __init__(self,err=''):
        Exception.__init__(self,err)

class DbInsertNotNullExcption(DbBaseException):
    '''
    Check Not NUll failed.
    '''
    def __init__(self,err=''):
        Exception.__init__(self,err)

class DbInsertUniqueExcption(DbBaseException):
    '''
    Check Unique failed.
    '''
    def __init__(self,err=''):
        Exception.__init__(self,err)