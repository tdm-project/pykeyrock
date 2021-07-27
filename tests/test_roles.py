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
This module tests CRUD operations on Keyrock Roles:
    *
"""

import unittest
import uuid

from keyrock import IDMManager, get_auth_token
from utils import random_role_name, random_app_name

from requests.exceptions import HTTPError


class TestRole(unittest.TestCase):
    """
    Tests Keyrock Role CRUD operations.
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
        self._app = self._im.create_application(random_app_name())

    def test_list_roles(self):
        """
        """
        _roles = self._im.list_roles(self._app.id)

        self.assertNotEqual(len(_roles), 0, "No roles found")

    def test_create_role(self):
        """
        """
        _role_name = random_role_name()
        _new_role = self._im.create_role(self._app.id, _role_name)

        self.assertNotEqual(_new_role, None, "Role not created")
        self.assertEqual(_new_role.name, _role_name,
                         "Role name doesn't matche")
        self.assertNotEqual(_new_role.id, None, "Role ID is None")
        self.assertNotEqual(_new_role.id, "", "Role ID is empty")

    def test_create_duplicated_role(self):
        """
        """
        _role_name = random_role_name()
        _new_role = self._im.create_role(self._app.id, _role_name)
        self.assertNotEqual(_new_role, None, "Role not created")

        _dup_role = self._im.create_role(self._app.id, _role_name)
        self.assertNotEqual(_dup_role, None, "Role not created")

        self.assertEqual(_new_role.name, _dup_role.name,
                         "Role name doesn't matche")
        self.assertEqual(_new_role.app_id, _dup_role.app_id,
                         "Role app id doesn't matche")
        self.assertNotEqual(_new_role.id, _dup_role.id,
                            "Role id are the same")

    def test_create_empty_role(self):
        """
        """
        with self.assertRaises(
                TypeError,
                msg="Not raising error on missing arguments"):
            self._im.create_role(self._app.id)
        with self.assertRaises(
                HTTPError,
                msg="Not raising error on empty role name"):
            self._im.create_role(self._app.id, "")

    def test_get_role(self):
        """
        """
        _role_name = random_role_name()

        _role = self._im.create_role(self._app.id, _role_name)

        _res = self._im.get_role(self._app.id, _role.id)

        self.assertEqual(_role.name, _res.name, "Wrong name")
        self.assertEqual(_role.app_id, _res.app_id, "Wrong application id")

    def test_get_not_existing_role(self):
        _res = self._im.get_role(self._app.id, uuid.uuid4())
        self.assertEqual(_res, None, "Returns not None object")

    def test_update_role(self):
        """
        """
        _app_id = uuid.uuid4()
        _role_id = uuid.uuid4()
        with self.assertRaises(
                NotImplementedError, msg="Not implemented method exists?"):
            self._im.update_role(_app_id, _role_id)

    def test_delete_role(self):
        """
        """
        _role_name = random_role_name()
        _role = self._im.create_role(self._app.id, _role_name)

        _res = self._im.get_role(self._app.id, _role.id)

        self.assertEqual(_role.name, _res.name, "Wrong name")
        self.assertEqual(_role.id, _res.id, "Wrong name")

        self._im.delete_role(self._app.id, _role.id)
        _res = self._im.get_role(self._app.id, _role.id)
        self.assertEqual(_res, None, 'Role not deleted')

    def test_delete_not_existing_role(self):
        """
        """
        _role_id = uuid.uuid4()
        _res = self._im.get_role(self._app.id, _role_id)
        self.assertEqual(_res, None, 'Role exists')

        with self.assertRaises(
                HTTPError,
                msg="Not raising error on not existing application"):
            self._im.delete_role(self._app.id, _role_id)

    def tearDown(self):
        _apps = self._im.list_applications()
        for _app in _apps:
            if _app.name.startswith('pykeyrock unittest'.capitalize()):
                self._im.delete_application(_app.id)


if __name__ == '__main__':
    unittest.main()
