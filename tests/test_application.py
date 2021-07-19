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

import uuid
import unittest
from lorem_text import lorem

# from keyrock import IDMApplication
# from keyrock import IDMProxy
from keyrock import IDMManager, get_auth_token
from requests.exceptions import HTTPError


KEYROCK_ORG = "Test Org"
KEYROCK_APP = "Test App"


class TestApplication(unittest.TestCase):
    """
    Tests Keyrock Application CRUD operations.
    """
    def setUp(self):
        self.keyrock_host = "localhost"
        self.keyrock_port = 3005
        self.keyrock_admin = "admin@test.com"
        self.keyrock_passw = "1234"
        self.auth_token, _ = get_auth_token(
            self.keyrock_host, self.keyrock_port, self.keyrock_admin,
            self.keyrock_passw)

        self._im = IDMManager(
            self.keyrock_host, self.keyrock_port, self.auth_token)

        _orgs = self._im.get_organizations_by_name(KEYROCK_ORG)
        if not _orgs:
            self._im.create_organization(KEYROCK_ORG)

    def random_app_name(self, prefix='pykeyrock unittest', words=2):
        return f"{prefix} {lorem.words(words)}".capitalize()

    def test_create_application(self):
        """
        """
        _app_name = self.random_app_name()
        self._im.create_application(_app_name)

        _apps = self._im.get_applications_by_name(_app_name)
        self.assertNotEqual(len(_apps), 0, "Application not created")
        self.assertEqual(len(_apps), 1, "More than one applications created")

    def test_create_application_empty_description(self):
        """
        """
        _app_name = self.random_app_name()
        _app_desc = f"{_app_name} application protected by Keyrock"
        _app = self._im.create_application(_app_name)

        self.assertEqual(_app.name, _app_name, "Wrong name")
        self.assertEqual(_app.description, _app_desc, "Wrong description")

    def test_create_application_with_description(self):
        """
        """
        _app_name = self.random_app_name()
        _description = lorem.words(5).capitalize() + '.'

        _app = self._im.create_application(_app_name, _description)

        self.assertEqual(_app.name, _app_name, "Wrong name")
        self.assertEqual(_app.description, _description, "Wrong description")

    def test_create_duplicated_application(self):
        """
        """
        _app_ids = list()
        _app_name = self.random_app_name()

        _app = self._im.create_application(_app_name)
        _app_ids.append(_app.id)

        _app = self._im.create_application(_app_name)
        _app_ids.append(_app.id)

        _apps = self._im.get_applications_by_name(_app_name)
        self.assertEqual(len(_apps), 2, "Duplicated application not created")

    def test_get_application(self):
        """
        """
        _app_name = self.random_app_name()
        _description = lorem.words(5).capitalize() + '.'

        _app = self._im.create_application(_app_name, _description)

        _res = self._im.get_application(_app.id)

        self.assertEqual(_app.name, _res.name, "Wrong name")
        self.assertEqual(_app.description, _res.description,
                         "Wrong description")

        _res = self._im.get_application(uuid.uuid4())
        self.assertEqual(_res, None, "Returns not None object")

    def test_delete_application(self):
        """
        """
        _app_name = self.random_app_name()
        _description = lorem.words(5).capitalize() + '.'
        _app = self._im.create_application(_app_name, _description)

        _res = self._im.get_application(_app.id)

        self.assertEqual(_app.name, _res.name, "Wrong name")
        self.assertEqual(_app.description, _res.description,
                         "Wrong description")

        _res = self._im.delete_application(_app.id)
        _res = self._im.get_application(_app.id)
        self.assertEqual(_res, None, 'Application not deleted')

    def test_delete_not_existing_application(self):
        """
        """
        _app_id = uuid.uuid4()
        with self.assertRaises(
                HTTPError,
                msg="Not raising error on not existing application"):
            self._im.delete_application(_app_id)

    def test_update_application(self):
        """
        """
        _app_id = uuid.uuid4()
        with self.assertRaises(
                NotImplementedError, msg="Not implemented method exists?"):
            self._im.update_application(_app_id)

    def tearDown(self):
        _apps = self._im.list_applications()
        for _app in _apps:
            if _app.name.startswith('pykeyrock unittest'.capitalize()):
                self._im.delete_application(_app.id)


if __name__ == '__main__':
    unittest.main()
