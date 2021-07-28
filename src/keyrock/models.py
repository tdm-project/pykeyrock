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


class IDMOrganization(object):
    """
    This class represent an organization inside the Keyrock IDM.

    Args:
        org_name: Mandatory if 'org_dict' argument is not provided or does
            not contain the 'name' key. The name of the organization. It takes
            the precedence over 'org_dict''s 'name' key.
        org_dict: a dictionary used to initialize the instance with the
            result of an IDM query. If 'org_name' argument is not provided,
            'org_dict' must be provided and have the 'name' key.

    """
    def __init__(self, org_name: str = None, org_dict: dict = None):
        self._org_name = org_name or org_dict['name']
        self._org_dict = org_dict
        self._org_id = org_dict.get('id', None)
        self._org_description = org_dict.get('description', None)

    @property
    def name(self):
        """Gets the name of the organization."""
        return self._org_name

    @property
    def id(self):
        """Gets the id of the organization."""
        return self._org_id

    @property
    def description(self):
        """Gets the description of the organization."""
        return self._org_description

    @property
    def dict(self):
        """Gets the dictionary that is passed to the constructor (it can be used to
        retrieve optional attributes returned by the IDM)."""
        return self._org_dict

    def __repr__(self):
        return (f"<IDMOrganization id: {self._org_id}, "
                f"name: \"{self._org_name}\", "
                f"description: \"{self._org_description}\">")


class IDMApplication(object):
    """
    This class represent an application inside the Keyrock IDM.

    Args:
        app_name:
            Mandatory if 'app_dict' argument is not provided or does not
            contain the 'name' key. The name of the application. It takes the
            precedence over 'app_dict''s 'name' key.
        app_dict:
            a dictionary used to initialize the instance with the result of an
            IDM query. If 'app_name' argument is not provided, 'app_dict' must
            be provided and have the 'name' key.

    """
    def __init__(self, app_name: str = None,
                 app_dict: dict = None):
        self._app_name = app_name or app_dict['name']
        self._app_dict = app_dict
        self._app_id = app_dict.get('id', None)
        self._app_secret = app_dict.get('secret', None)
        self._app_description = app_dict.get('description', None)

    @property
    def name(self):
        """Gets the name of the application."""
        return self._app_name

    @property
    def id(self):
        """Gets the id of the application."""
        return self._app_id

    @property
    def description(self):
        """Gets the description of the application."""
        return self._app_description

    @property
    def secret(self):
        """Gets the secret key of the application (it is available only at the
        application creation)."""
        return self._app_secret

    @property
    def dict(self):
        """Gets the dictionary that is passed to the constructor (it can be used to
        retrieve optional attributes returned by the IDM)."""
        return self._app_dict

    def __repr__(self):
        return (f"<IDMApplication id: {self._app_id}, "
                f"name: \"{self._app_name}\", "
                f"description: \"{self._app_description}\">")


class IDMProxy(object):
    """
    This class represent an application's proxy inside the Keyrock IDM.

    Args:
        proxy_id:
            Mandatory if 'proxy_dict' argument is not provided or does not
            contain the 'id' key. This is the id of the proxy. It takes the
            precedence over 'proxy_dict''s 'id' key.
        proxy_dict:
            a dictionary used to initialize the instance with the result of an
            IDM query. If 'proxy_id' argument is not provided, 'proxy_dict'
            must be provided and have the 'id' key.

        """
    def __init__(self, proxy_id: str = None, proxy_dict: dict = None):

        self._proxy_dict = proxy_dict
        self._proxy_id = proxy_id or proxy_dict['id']
        self._proxy_password = proxy_dict.get('password', None)
        self._proxy_oauth_client_id = proxy_dict.get('oauth_client_id', None)

    def update(self, proxy_dict: dict):
        """
        Updates some of the proxy attributes.
        Currently only the 'password' attribute can be updated (the key
        'new_password' can be used as alias).
        """
        if 'password' in [*proxy_dict]:
            self._proxy_password = proxy_dict['password']
            self._proxy_dict.update({'password': proxy_dict['password']})
        if 'new_password' in [*proxy_dict]:
            self._proxy_password = proxy_dict['new_password']
            self._proxy_dict.update({'password': proxy_dict['new_password']})

    @property
    def id(self):
        """Gets the id of the proxy."""
        return self._proxy_id

    @property
    def password(self):
        """Gets the password of the proxy (it is available only at the proxy
        creation)."""
        return self._proxy_password

    @property
    def oauth_client_id(self):
        """
        Gets the oauth client id of the proxy (it is available only after the
        proxy creation).
        """
        return self._proxy_oauth_client_id

    @property
    def dict(self):
        """Gets the dictionary that is passed to the constructor (it can be used to
        retrieve optional attributes returned by the IDM)."""
        return self._proxy_dict

    def __repr__(self):
        return (f"<IDMProxy id: {self._proxy_id}, oauth_client_id: "
                f"{self._proxy_oauth_client_id}>")


class IDMUser(object):
    """
    This class represent an user inside the Keyrock IDM.

    Args:
        user_email:
            Mandatory if 'user_dict' argument is not provided or does not
            contain the 'email' key. The email or login (in the form of an
            email) of the user. It takes the precedence over 'user''s 'email'
            key.
        user_dict:
            a dictionary used to initialize the instance with the result of an
            IDM query. If 'user_email' argument is not provided, 'user_dict'
            must be provided and have the 'email' key.

    """
    def __init__(self, user_email: str = None,
                 user_dict: dict = None):
        self._user_email = user_email or user_dict['email']
        self._user_dict = user_dict
        self._user_id = user_dict.get('id', None)
        self._user_name = user_dict.get('username', None)
        self._user_enabled = user_dict.get('enabled', False)
        self._user_gravatar = user_dict.get('gravatar', None)
        self._user_website = user_dict.get('website', None)
        self._user_expiration = user_dict.get('date_password', None)
        self._user_description = user_dict.get('description', None)

    @property
    def name(self):
        """Gets the user's name."""
        return self._user_name

    @property
    def id(self):
        """Gets the user's id."""
        return self._user_id

    @property
    def email(self):
        """Gets the user's email."""
        return self._user_email

    @property
    def login(self):
        """
        Gets the user's login i.e. the user's email. Actually is an alias of
        the 'email' property.
        """
        return self._user_email

    @property
    def description(self):
        """Gets the user's description."""
        return self._user_description

    @property
    def dict(self):
        """Gets the dictionary that is passed to the constructor (it can be used to
        retrieve optional attributes returned by the IDM)."""
        return self._user_dict

    def __repr__(self):
        return (f"<IDMUser id: {self._user_id}, "
                f"email: \"{self._user_email}\", "
                f"username: \"{self._user_name}\", "
                f"enabled: \"{self._user_enabled}\", "
                f"description: \"{self._user_description}\">")


class IDMRole(object):
    """
    This class represent a role of an application inside the Keyrock IDM.

    Args:
        role_name:
            Mandatory if 'role_dict' argument is not provided or does not
            contain the 'name' key. It takes the precedence over 'role_dict''s
            'name' key.
        role_dict:
            a dictionary used to initialize the instance with the result of an
            IDM query. If 'name' argument is not provided, 'role_dict'
            must be provided and have the 'name' key.
        application_id:
            the application id to which the role belongs to.
    """
    def __init__(self, role_name: str = None, role_dict: dict = None,
                 application_id: str = None):
        self._role_dict = role_dict
        self._role_name = role_name or role_dict['name']
        self._role_id = role_dict.get('id', None)
        self._role_app_id = application_id

    @property
    def name(self):
        """Gets the role's name."""
        return self._role_name

    @property
    def id(self):
        """Gets the role's id."""
        return self._role_id

    @property
    def app_id(self):
        """Gets the role's application id."""
        return self._role_app_id

    @property
    def dict(self):
        """Gets the dictionary that is passed to the constructor (it can be used to
        retrieve optional attributes returned by the IDM)."""
        return self._role_dict

    def __repr__(self):
        return (f"<IDMRole id: {self._role_id}, "
                f"name: \"{self._role_name}\", "
                f"app_id: {self._role_app_id}>")


class IDMPermission(object):
    """
    This class represent a permission of an application inside the Keyrock IDM.

    Args:
        permission_name:
            Mandatory if 'permission_dict' argument is not provided or does not
            contain the 'name' key. It takes the precedence over
            'permission_dict''s 'name' key. The name of the permission.
        permission_action:
            Mandatory if 'permission_dict' argument is not provided or does not
            contain the 'action' key. It takes the precedence over
            'permission_dict''s 'action' key. The action allowed by the
            permission ("GET", "POST", "PUT", "DELETE" etc.).
        permission_resource:
            Mandatory if 'permission_dict' argument is not provided or does not
            contain the 'resource' key. It takes the precedence over
            'permission_dict''s 'resource' key. The resource managed by the
            permission.
        is_regex:
            Whether the permission_resource is a regex or not.
            Default: 'False'.
        permission_dict:
            a dictionary used to initialize the instance with the result of an
            IDM query. If 'name' argument is not provided, 'permission_dict'
            must be provided and have the 'name' key.
        application_id:
            the application id to which the permission belongs to.
    """
    def __init__(self, permission_name: str = None,
                 permission_action: str = None,
                 permission_resource: str = None,
                 is_regex: bool = False,
                 permission_dict: dict = None,
                 application_id: str = None):
        self._permission_dict = permission_dict
        self._permission_name = permission_name or permission_dict['name']
        self._permission_action = permission_name or permission_dict['action']
        self._permission_resource = (permission_resource or
                                     permission_dict['resource'])
        self._permission_is_regex = is_regex
        self._permission_id = permission_dict.get('id', None)
        self._permission_app_id = application_id

    @property
    def name(self):
        """Gets the permission's name."""
        return self._permission_name

    @property
    def action(self):
        """Gets the permission's action."""
        return self._permission_action

    @property
    def resource(self):
        """Gets the permission's resource."""
        return self._permission_resource

    @property
    def is_regex(self):
        """Gets the permission's is_regex flag."""
        return self._permission_is_regex

    @property
    def id(self):
        """Gets the permission's id."""
        return self._permission_id

    @property
    def app_id(self):
        """Gets the permission's application id."""
        return self._permission_app_id

    @property
    def dict(self):
        """Gets the dictionary that is passed to the constructor (it can be used to
        retrieve optional attributes returned by the IDM)."""
        return self._permission_dict

    def __repr__(self):
        return (f"<IDMPermission id: {self._permission_id}, "
                f"name: \"{self._permission_name}\", "
                f"action: \"{self._permission_action}\" on "
                f"resource: \"{self._permission_resource}\" "
                f"(is regex: {self._permission_is_regex}), "
                f"app_id: {self._permission_app_id}>")
