"""
pykeyrock.

An example python library.
"""


from .idm import IDMManager, get_auth_token
from .models import IDMApplication
from .version import version

import logging


__version__ = version
__author__ = "Massimo Gaggero"
__credits__ = (
    "CRS4, Center for Advanced Studies, Research and Development in Sardinia")


module_logger = logging.getLogger(__name__)
module_handlr = logging.StreamHandler()
module_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
module_handlr.setFormatter(module_format)
module_logger.addHandler(module_handlr)
module_logger.setLevel(logging.CRITICAL)

logging.getLogger('keyrock.IDMManager').addHandler(module_handlr)
logging.getLogger('keyrock.IDMManager').setLevel(logging.CRITICAL)
