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

from utils import random_app_name, random_app_description

# from keyrock import IDMApplication
# from keyrock import IDMProxy
from keyrock import IDMManager, get_auth_token

from requests.exceptions import HTTPError


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

    def test_create_application(self):
        """
        """
        _app_name = random_app_name()
        self._im.create_application(_app_name)

        _apps = self._im.get_applications_by_name(_app_name)
        self.assertNotEqual(len(_apps), 0, "Application not created")
        self.assertEqual(len(_apps), 1, "More than one applications created")

    def test_create_application_empty_description(self):
        """
        """
        _app_name = random_app_name()
        _app_desc = f"{_app_name} application protected by Keyrock"
        _app = self._im.create_application(_app_name)

        self.assertEqual(_app.name, _app_name, "Wrong name")
        self.assertEqual(_app.description, _app_desc, "Wrong description")

    def test_create_application_with_description(self):
        """
        """
        _app_name = random_app_name()
        _description = random_app_description()

        _app = self._im.create_application(_app_name, _description)

        self.assertEqual(_app.name, _app_name, "Wrong name")
        self.assertEqual(_app.description, _description, "Wrong description")

    def test_create_duplicated_application(self):
        """
        """
        _app_ids = list()
        _app_name = random_app_name()

        _app = self._im.create_application(_app_name)
        _app_ids.append(_app.id)

        _app = self._im.create_application(_app_name)
        _app_ids.append(_app.id)

        _apps = self._im.get_applications_by_name(_app_name)
        self.assertEqual(len(_apps), 2, "Duplicated application not created")

    def test_get_application(self):
        """
        """
        _app_name = random_app_name()
        _description = random_app_description()

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
        _app_name = random_app_name()
        _description = random_app_description()
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


class TestProxy(unittest.TestCase):
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

    def test_create_proxy(self):
        """
        """
        _app_name = random_app_name()
        _app = self._im.create_application(_app_name)

        _proxy = self._im.create_proxy(_app.id)
        self.assertNotEqual(_proxy, None, "Proxy not created")
        self.assertNotEqual(_proxy.password, None,
                            "Proxy's password not retrieved")
        self.assertNotEqual(_proxy.dict, None, "Proxy's dict is empty")

    def test_create_duplicated_proxy(self):
        """
        """
        _app_name = random_app_name()
        _app = self._im.create_application(_app_name)

        _proxy_1 = self._im.create_proxy(_app.id)
        self.assertNotEqual(_proxy_1, None, "Proxy not created")

        with self.assertRaises(
                HTTPError,
                msg="Not raising error on not existing application"):
            self._im.create_proxy(_app.id)

    def test_get_proxy(self):
        """
        """
        _app_name = random_app_name()
        _app = self._im.create_application(_app_name)

        _proxy = self._im.create_proxy(_app.id)

        _res = self._im.get_proxy(_app.id)

        self.assertNotEqual(_res.id, None, "Proxy not found")
        self.assertNotEqual(_res.oauth_client_id, None,
                            "Proxy's oauth_client_id is empty")
        self.assertNotEqual(_res.dict, None, "Proxy's dict is empty")
        self.assertEqual(_res.password, None,
                         "Should not retrieve the proxy's password")

        self.assertEqual(
            _res.id, _proxy.id,
            "Created and retrieved proxys should have the same id")

    def test_reset_proxy(self):
        """
        """
        _app_name = random_app_name()
        _app = self._im.create_application(_app_name)

        _proxy = self._im.create_proxy(_app.id)
        _res = self._im.reset_proxy(_app.id)

        self.assertNotEqual(_res, None, "Proxy's password not updated")
        self.assertNotEqual(_res.password, _proxy.password,
                            "The new password is the same of the old one")

    def test_delete_proxy(self):
        """
        """
        _app_name = random_app_name()
        _app = self._im.create_application(_app_name)

        _proxy = self._im.create_proxy(_app.id)
        _res = self._im.get_proxy(_app.id)

        self.assertEqual(
            _res.id, _proxy.id,
            "Created and retrieved proxys should have the same id")

        self._im.delete_proxy(_app.id)

        _res = self._im.get_proxy(_app.id)
        self.assertEqual(_res, None, "Proxy not deleted")

    def test_delete_not_existing_proxy(self):
        _app_name = random_app_name()
        _app = self._im.create_application(_app_name)
        _proxy = self._im.get_proxy(_app.id)

        self.assertEqual(_proxy, None, "Proxy exists")

        with self.assertRaises(
                HTTPError,
                msg="Not raising error on not existing application"):
            self._im.delete_proxy(_app.id)

    def tearDown(self):
        _apps = self._im.list_applications()
        for _app in _apps:
            if _app.name.startswith('pykeyrock unittest'.capitalize()):
                self._im.delete_application(_app.id)


if __name__ == '__main__':
    unittest.main()
