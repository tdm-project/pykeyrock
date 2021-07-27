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
This module tests CRUD operations on Keyrock User Management:
    *
"""

import uuid
import unittest

from utils import random_user_name, random_user_email, random_user_password

from keyrock import IDMManager, get_auth_token
from requests.exceptions import HTTPError


class TestUser(unittest.TestCase):
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

    def test_create_user(self):
        """
        """
        _user_email = random_user_email()
        _user_password = random_user_password()
        _user_name = random_user_name()
        _new_user = self._im.create_user(_user_email, _user_password,
                                         _user_name)
        self.assertNotEqual(_new_user, None, "User not created")
        self.assertEqual(_new_user.email, _user_email,
                         "Email/Login doesn't match")

        _user = self._im.get_user(_new_user.id)
        self.assertEqual(_user.email, _user_email,
                         "Email/Login doesn't match")

    def test_get_user(self):
        """
        """
        _user_email = random_user_email()
        _user_password = random_user_password()
        _user_name = random_user_name()
        _user = self._im.create_user(_user_email, _user_password,
                                     _user_name)

        _res = self._im.get_user(_user.id)
        self.assertEqual(_user.email, _res.email, "Wrong name")
        self.assertEqual(_user.name, _res.name, "Wrong name")
        self.assertEqual(_user.description, _res.description,
                         "Wrong description")

    def test_get_not_existing_user(self):
        _res = self._im.get_application(uuid.uuid4())
        self.assertEqual(_res, None,
                         "Not returning None object for not existing user")

    def test_update_user(self):
        """
        """
        _user_id = uuid.uuid4()
        with self.assertRaises(
                NotImplementedError, msg="Not implemented method exists?"):
            self._im.update_user(_user_id)

    def test_delete_user(self):
        """
        """
        _user_email = random_user_email()
        _user_password = random_user_password()
        _user_name = random_user_name()
        _user = self._im.create_user(_user_email, _user_password,
                                     _user_name)

        _res = self._im.get_user(_user.id)
        self.assertEqual(_user.email, _res.email, "Wrong name")
        self.assertEqual(_user.name, _res.name, "Wrong name")
        self.assertEqual(_user.description, _res.description,
                         "Wrong description")

        _res = self._im.delete_user(_user.id)
        _res = self._im.get_user(_user.id)
        self.assertEqual(_res, None, 'User not deleted')

    def test_delete_not_existing_user(self):
        """
        """
        _user_id = uuid.uuid4()
        with self.assertRaises(
                HTTPError,
                msg="Not raising error on not existing application"):
            self._im.delete_user(_user_id)

    def tearDown(self):
        _users = self._im.list_users()
        for _user in _users:
            if _user.email.startswith('pykeyrock_unittest'):
                self._im.delete_user(_user.id)
