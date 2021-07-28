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
This module tests CRUD operations on Keyrock Permission:
    *
"""

import unittest
import uuid

from keyrock import IDMManager, get_auth_token
from utils import random_app_name, random_permission_name
from utils import random_permission_action, random_permission_resource

from requests.exceptions import HTTPError


class TestPermission(unittest.TestCase):
    """
    Tests Keyrock Permission CRUD operations.
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
        _permissions = self._im.list_permissions(self._app.id)

        self.assertNotEqual(len(_permissions), 0, "No permissions found")

    def test_create_permission(self):
        """
        """
        _permission_name = random_permission_name()
        _permission_action = random_permission_action()
        _permission_resource = random_permission_resource()
        _permission = self._im.create_permission(_permission_name,
                                                 _permission_action,
                                                 _permission_resource,
                                                 False, self._app.id)

        self.assertNotEqual(_permission, None, "Permission not created")
        self.assertEqual(_permission.name, _permission_name,
                         "Permission name doesn't match")
        self.assertEqual(_permission.action, _permission_action,
                         "Permission action doesn't match")
        self.assertEqual(_permission.resource, _permission_resource,
                         "Permission resource doesn't match")
        self.assertEqual(_permission.is_regex, False,
                         "Permission is_regex doesn't match")
        self.assertNotEqual(_permission.id, None, "Permission ID is None")
        self.assertNotEqual(_permission.id, "", "Permission ID is empty")

    def test_create_duplicated_role(self):
        """
        """
        _permission_name = random_permission_name()
        _permission_action = random_permission_action()
        _permission_resource = random_permission_resource()
        _permission = self._im.create_permission(_permission_name,
                                                 _permission_action,
                                                 _permission_resource,
                                                 False, self._app.id)
        self.assertNotEqual(_permission, None, "Permission not created")

        _dup_permission = self._im.create_permission(_permission_name,
                                                     _permission_action,
                                                     _permission_resource,
                                                     False, self._app.id)
        self.assertNotEqual(_dup_permission, None, "Permission not created")

        self.assertEqual(_permission.name, _dup_permission.name,
                         "Permission name doesn't match")
        self.assertEqual(_permission.action, _dup_permission.action,
                         "Permission action doesn't match")
        self.assertEqual(_permission.resource, _dup_permission.resource,
                         "Permission resource doesn't match")
        self.assertEqual(_permission.is_regex, False,
                         "Permission is_regex doesn't match")
        self.assertEqual(_permission.app_id, _dup_permission.app_id,
                         "Permission app id doesn't match")
        self.assertNotEqual(_permission.id, _dup_permission.id,
                            "Permission id are the same")

    def test_create_empty_permission(self):
        """
        """
        with self.assertRaises(
                TypeError,
                msg="Not raising error on missing arguments"):
            self._im.create_permission(self._app.id)
        with self.assertRaises(
                HTTPError,
                msg="Not raising error on empty permission name"):
            self._im.create_permission("", "", "")
        with self.assertRaises(
                HTTPError,
                msg="Not raising error on empty action name"):
            self._im.create_permission(random_permission_name(), "", "")
        with self.assertRaises(
                HTTPError,
                msg="Not raising error on empty resource name"):
            self._im.create_permission(random_permission_name(),
                                       random_permission_action(), "")

    def test_get_permission(self):
        """
        """
        _permission = self._im.create_permission(random_permission_name(),
                                                 random_permission_action(),
                                                 random_permission_resource(),
                                                 False, self._app.id)

        _res = self._im.get_permission(self._app.id, _permission.id)
        self.assertEqual(_res.name, _permission.name,
                         "Permission name doesn't match")
        self.assertEqual(_res.action, _permission.action,
                         "Permission action doesn't match")
        self.assertEqual(_res.resource, _permission.resource,
                         "Permission resource doesn't match")
        self.assertEqual(_res.is_regex, False,
                         "Permission is_regex doesn't match")
        self.assertEqual(_res.app_id, _permission.app_id,
                         "Permission app id doesn't match")

    def test_get_not_existing_permission(self):
        _res = self._im.get_permission(self._app.id, uuid.uuid4())
        self.assertEqual(_res, None, "Returns not None object")

    def test_update_permission(self):
        """
        """
        _app_id = uuid.uuid4()
        _permission_id = uuid.uuid4()
        with self.assertRaises(
                NotImplementedError, msg="Not implemented method exists?"):
            self._im.update_permission(_app_id, _permission_id)

    def test_delete_permission(self):
        """
        """
        _permission = self._im.create_permission(random_permission_name(),
                                                 random_permission_action(),
                                                 random_permission_resource(),
                                                 False, self._app.id)

        _res = self._im.get_permission(self._app.id, _permission.id)
        self.assertEqual(_res.name, _permission.name,
                         "Permission name doesn't match")
        self.assertEqual(_res.action, _permission.action,
                         "Permission action doesn't match")
        self.assertEqual(_res.resource, _permission.resource,
                         "Permission resource doesn't match")
        self.assertEqual(_res.is_regex, False,
                         "Permission is_regex doesn't match")
        self.assertEqual(_res.app_id, _permission.app_id,
                         "Permission app id doesn't match")

        self._im.delete_permission(self._app.id, _permission.id)
        _res = self._im.get_permission(self._app.id, _permission.id)
        self.assertEqual(_res, None, 'Permission not deleted')

    def test_delete_not_existing_permission(self):
        """
        """
        _permission_id = uuid.uuid4()
        _res = self._im.get_permission(self._app.id, _permission_id)
        self.assertEqual(_res, None, 'Permission exists')

        with self.assertRaises(
                HTTPError,
                msg="Not raising error on not existing permission"):
            self._im.delete_permission(self._app.id, _permission_id)

    def tearDown(self):
        _apps = self._im.list_applications()
        for _app in _apps:
            if _app.name.startswith('pykeyrock unittest'.capitalize()):
                self._im.delete_application(_app.id)


if __name__ == '__main__':
    unittest.main()
