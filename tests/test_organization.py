#!/usr/bin/env python
#
#  Copyright 2021 CRS4 - Center for Advanced Studies, Research and Development
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
#

"""
This module tests CRUD operations on Keyrock Application:
    *
"""

# import logging
import uuid
import unittest
from lorem_text import lorem

from keyrock import IDMManager, get_auth_token
from requests.exceptions import HTTPError


KEYROCK_ORG = "Test Org"
KEYROCK_APP = "Test App"


class TestOrganization(unittest.TestCase):
    """
    Tests Keyrock Organizations CRUD operations.
    """
    def setUp(self):
        self.keyrock_host = "localhost"
        self.keyrock_port = 3005
        self.keyrock_admin = "admin@test.com"
        self.keyrock_passw = "1234"
        self.auth_token, _ = get_auth_token(
            self.keyrock_host, self.keyrock_port, self.keyrock_admin,
            self.keyrock_passw)

        # logging.getLogger('keyrock.IDMManager').setLevel(logging.DEBUG)

        self._im = IDMManager(
            self.keyrock_host, self.keyrock_port, self.auth_token)

    def random_org_name(self, prefix='pykeyrock unittest', words=2):
        return f"{prefix} {lorem.words(words)}".capitalize()

    def test_create_organization(self):
        """
        """
        _org_name = self.random_org_name()
        self._im.create_organization(_org_name)

        _orgs = self._im.get_organizations_by_name(_org_name)
        self.assertNotEqual(len(_orgs), 0, "Organization not created")
        self.assertEqual(len(_orgs), 1, "More than one organizations created")

    def test_create_organization_empty_description(self):
        """
        """
        _org_name = self.random_org_name()
        _org_desc = f"This is the {_org_name} organization"
        _org = self._im.create_organization(_org_name)

        self.assertEqual(_org.name, _org_name, "Wrong name")
        self.assertEqual(_org.description, _org_desc, "Wrong description")

    def test_create_organization_with_description(self):
        """
        """
        _org_name = self.random_org_name()
        _description = lorem.words(5).capitalize() + '.'

        _org = self._im.create_organization(_org_name, _description)

        self.assertEqual(_org.name, _org_name, "Wrong name")
        self.assertEqual(_org.description, _description, "Wrong description")

    def test_create_duplicated_organization(self):
        """
        """
        _org_ids = list()
        _org_name = self.random_org_name()

        _org = self._im.create_organization(_org_name)
        _org_ids.append(_org.id)

        _org = self._im.create_organization(_org_name)
        _org_ids.append(_org.id)

        _orgs = self._im.get_organizations_by_name(_org_name)
        self.assertEqual(len(_orgs), 2, "Duplicated organizations not created")

    def test_get_organization(self):
        """
        """
        _org_name = self.random_org_name()
        _description = lorem.words(5).capitalize() + '.'

        _org = self._im.create_organization(_org_name, _description)

        _res = self._im.get_organization(_org.id)

        self.assertEqual(_org.name, _res.name, "Wrong name")
        self.assertEqual(_org.description, _res.description,
                         "Wrong description")

        _res = self._im.get_organization(uuid.uuid4())
        self.assertEqual(_res, None, "Returns not None object")

    def test_delete_organization(self):
        _org_name = self.random_org_name()
        _description = lorem.words(5).capitalize() + '.'
        _org = self._im.create_organization(_org_name, _description)

        _res = self._im.get_organization(_org.id)

        self.assertEqual(_org.name, _res.name, "Wrong name")
        self.assertEqual(_org.description, _res.description,
                         "Wrong description")

        _res = self._im.delete_organization(_org.id)
        _res = self._im.get_organization(_org.id)
        self.assertEqual(_res, None, 'Organization not deleted')

    def test_delete_not_existing_organization(self):
        """
        """
        _org_id = uuid.uuid4()
        with self.assertRaises(
                HTTPError,
                msg="Not raising error on not existing organization"):
            self._im.delete_organization(_org_id)

    def test_update_organization(self):
        """
        """
        _org_id = uuid.uuid4()
        with self.assertRaises(
                NotImplementedError, msg="Not implemented method exists?"):
            self._im.update_organization(_org_id)

    def tearDown(self):
        _orgs = self._im.list_organizations()
        for _org in _orgs:
            if _org.name.startswith('pykeyrock unittest'.capitalize()):
                self._im.delete_organization(_org.id)


if __name__ == '__main__':
    unittest.main()
