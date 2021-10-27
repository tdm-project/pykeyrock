#  Copyright 2021, CRS4 - Center for Advanced Studies, Research and Development
#  in Sardinia
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
.. module:: keyrock
"""

from .idm import IDMManager, IDMQuery
from .idm import get_auth_token, check_auth_token
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
