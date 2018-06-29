
###############################################################################
####### EXPECTION #############################################################
###############################################################################
from erweb.response_type import response_type

class ErwebBaseException(Exception):
    def __init__(self,err="Erweb is Crashed!"):
        Exception.__init__(self,err)

class RoutePathIllegalException(ErwebBaseException):
    def __init__(self,err="Route Error!"):
        Exception.__init__(self,err)

class RouteAddfailedException(ErwebBaseException):
    def __init__(self,err="Insert Route URL Failed!"):
        Exception.__init__(self,err)

class PageNotFonudError(ErwebBaseException):
    def __init__(self,err="Page Not Found"):
        Exception.__init__(self,err)

class HTTPException(ErwebBaseException):
    def __init__(self,status = 500):
        err = response_type[status]
        Exception.__init__(self,err)
        self.status = status

class DatabaseTypeNotSupportError(ErwebBaseException):
    def __init__(self,err="Database is not support!"):
        Exception.__init__(self,err)

class CookieTooLargeException(ErwebBaseException):
    def __init__(self,err="Cookie is too large"):
        Exception.__init__(self,err)

class GetSessionException(ErwebBaseException):
    def __init__(self,err="Session error"):
        Exception.__init__(self,err)

class PackageNotInstalledException(ErwebBaseException):
    def __init__(self,err="Jinja2 is not installed."):
        Exception.__init__(self,err)