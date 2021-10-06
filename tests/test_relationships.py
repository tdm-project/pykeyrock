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
This module tests operations on Keyrock entities' relationships
    *
"""

import uuid
import unittest

from utils import random_org_name, random_org_description
from utils import random_user_name, random_user_email, random_user_password

from keyrock import IDMManager, get_auth_token
from requests.exceptions import HTTPError


class TestOrganizationRelationships(unittest.TestCase):
    """
    Tests Keyrock Organizations relationships operations.
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

    def test_add_user_to_organization(self):
        """
        """
        _user_email = random_user_email()
        _user_password = random_user_password()
        _user_name = random_user_name()
        _user = self._im.create_user(_user_email, _user_password,
                                     _user_name)

        _org = self._im.create_organization(random_org_name(),
                                            random_org_description())

        self._im.add_user_to_organization(_org.id, _user.id)

        _users = self._im.list_organization_members(_org.id)
        self.assertIn(_user.id, map(lambda x: x['user_id'], _users),
                      "The user has not been associated with the organization")

    def test_add_not_existing_user_to_organization(self):
        """
        """
        _user_id = uuid.uuid4()
        _org = self._im.create_organization(random_org_name(),
                                            random_org_description())

        with self.assertRaises(
                HTTPError,
                msg="Not raising error on wrong user's role"):
            self._im.add_user_to_organization(_org.id, _user_id)

    def test_list_organization_users(self):
        """
        """
        _org = self._im.create_organization(random_org_name(),
                                            random_org_description())

        _user_email = random_user_email()
        _user_password = random_user_password()
        _user_name = random_user_name()
        _user = self._im.create_user(_user_email, _user_password,
                                     _user_name)

        self._im.add_user_to_organization(_org.id, _user.id)
        _users = self._im.list_organization_members(_org.id)
        self.assertIn(_user.id, map(lambda x: x['user_id'], _users),
                      "The user has not been associated with the organization")

        _user_email = random_user_email()
        _user_password = random_user_password()
        _user_name = random_user_name()
        _user = self._im.create_user(_user_email, _user_password,
                                     _user_name)

        self._im.add_user_to_organization(_org.id, _user.id, is_owner=True)

        _users = self._im.list_organization_members(_org.id)
        self.assertIn(_user.id, map(lambda x: x['user_id'], _users),
                      "The user has not been associated with the organization")

    def test_get_organization_member(self):
        """
        """
        _org = self._im.create_organization(random_org_name(),
                                            random_org_description())

        _user_email = random_user_email()
        _user_password = random_user_password()
        _user_name = random_user_name()
        _user = self._im.create_user(_user_email, _user_password,
                                     _user_name)

        self._im.add_user_to_organization(_org.id, _user.id)

        _membership = self._im.get_organization_member(_org.id, _user.id)
        self.assertEqual(_membership['user_id'], _user.id,
                         "Member user ID differs")
        self.assertEqual(_membership['organization_id'], _org.id,
                         "Member organization ID differs")
        self.assertEqual(_membership['role'], "member",
                         "Wrong member role")

        _user_email = random_user_email()
        _user_password = random_user_password()
        _user_name = random_user_name()
        _user = self._im.create_user(_user_email, _user_password,
                                     _user_name)

        self._im.add_user_to_organization(_org.id, _user.id, is_owner=True)

        _membership = self._im.get_organization_member(_org.id, _user.id)
        self.assertEqual(_membership['user_id'], _user.id,
                         "Owner user ID differs")
        self.assertEqual(_membership['organization_id'], _org.id,
                         "Owner organization ID differs")
        self.assertEqual(_membership['role'], "owner",
                         "Wrong owner role")

    def test_remove_user_from_organization(self):
        """
        """
        _org = self._im.create_organization(random_org_name(),
                                            random_org_description())

        _user_email = random_user_email()
        _user_password = random_user_password()
        _user_name = random_user_name()
        _user = self._im.create_user(_user_email, _user_password,
                                     _user_name)

        self._im.add_user_to_organization(_org.id, _user.id)

        _membership = self._im.get_organization_member(_org.id, _user.id)
        self.assertEqual(_membership['user_id'], _user.id,
                         "Member user ID differs")
        self.assertEqual(_membership['organization_id'], _org.id,
                         "Member organization ID differs")
        self.assertEqual(_membership['role'], "member",
                         "Wrong member role")

        self._im.remove_user_from_organization(_org.id, _user.id)
        _membership = self._im.get_organization_member(_org.id, _user.id)
        self.assertIsNone(_membership, "User is still there")

    def test_remove_user_wrong_role_from_organization(self):
        """
        """
        _org = self._im.create_organization(random_org_name(),
                                            random_org_description())

        _user_email = random_user_email()
        _user_password = random_user_password()
        _user_name = random_user_name()
        _user = self._im.create_user(_user_email, _user_password,
                                     _user_name)

        self._im.add_user_to_organization(_org.id, _user.id)

        _membership = self._im.get_organization_member(_org.id, _user.id)
        self.assertEqual(_membership['user_id'], _user.id,
                         "Member user ID differs")
        self.assertEqual(_membership['organization_id'], _org.id,
                         "Member organization ID differs")
        self.assertEqual(_membership['role'], "member",
                         "Wrong member role")

        with self.assertRaises(
                HTTPError,
                msg="Not raising error on existing oser"):
            self._im.remove_user_from_organization(_org.id, _user.id,
                                                   ownership=True)

    def tearDown(self):
        _orgs = self._im.list_organizations()
        for _org in _orgs:
            if _org.name.startswith('pykeyrock unittest'.capitalize()):
                self._im.delete_organization(_org.id)

        _users = self._im.list_users()
        for _user in _users:
            if _user.email.startswith('pykeyrock_unittest'):
                self._im.delete_user(_user.id)
