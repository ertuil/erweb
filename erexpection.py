###############################################################################
####### EXPECTION #############################################################
###############################################################################

class ErwebBaseException(Exception):
    pass

class RoutePathIllegalException(ErwebBaseException):
    pass

class RouteAddfailedException(Exception):
    pass