
###############################################################################
####### EXPECTION #############################################################
###############################################################################

class ErwebBaseException(Exception):
    pass

class RoutePathIllegalException(ErwebBaseException):
    pass

class RouteAddfailedException(Exception):
    pass

class PageNotFonudError(Exception):
    pass

class HTTPException(ErwebBaseException):
    def __init__(self,err='500 Oops!',status = 500):
        Exception.__init__(self,err)
        self.status = status

class DatabaseTypeNotSupportError(Exception):
    pass

class CookieTooLargeException(Exception):
    pass

class GetSessionException(Exception):
    pass