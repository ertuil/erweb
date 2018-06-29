__author__ = "ertuil"
__date__ = "2018.06.21"
__version__ = "0.0.0"

from erweb.config import default_config as erweb_config
from erweb.database import default_database as erweb_database
from erweb.template import default_template as erweb_template
from erweb.erweb import *

__all__ = ['erweb','defaultapp','erweb_config','erweb_database','erweb_template']