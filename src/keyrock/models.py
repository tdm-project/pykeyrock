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

class IDMOrganization(object):
    """
    This class represent an organization inside the Keyrock IDM.

    Attributes:
        name (str): the name of the organization.
        id (str): the id of the organization.
        description (str): the description of the organization.
        dict (str): the dictionary that is passed to the constructor (it can be
            used to retrieve optional attributes returned by the IDM).
    """
    def __init__(self, org_name: str = None, org_dict: dict = None):
        """
        Inits IDMOrganization.

        Args:
          org_name:
            Mandatory if 'org_dict' argument is not provided or does not
            contain the 'name' key. The name of the organization. It takes the
            precedence over 'org_dict''s 'name' key.
          org_dict:
            a dictionary used to initialize the instance with the result of an
            IDM query. If 'org_name' argument is not provided, 'org_dict' must
            be provided and have the 'name' key.
        """

        self._org_name = org_name or org_dict['name']
        self._org_dict = org_dict
        self._org_id = org_dict.get('id', None)
        self._org_description = org_dict.get('description', None)

    @property
    def name(self):
        return self._org_name

    @property
    def id(self):
        return self._org_id

    @property
    def description(self):
        return self._org_description

    @property
    def dict(self):
        return self._org_dict

    def __repr__(self):
        return (f"<IDMOrganization id: {self._org_id}, "
                f"name: \"{self._org_name}\", "
                f"description: \"{self._org_description}\">")


class IDMApplication(object):
    """
    This class represent an application inside the Keyrock IDM.

    Attributes:
        name (str): the name of the application.
        id (str): the id of the application.
        description (str): the description of the application.
        secret (str): the secret key of the application (it is available only
            at the application creation).
        dict (str): the dictionary that is passed to the constructor (it can be
            used to retrieve optional attributes returned by the IDM).
    """
    def __init__(self, app_name: str = None,
                 app_dict: dict = None):
        """
        Inits IDMApplication.

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
        self._app_name = app_name or app_dict['name']
        self._app_dict = app_dict
        self._app_id = app_dict.get('id', None)
        self._app_secret = app_dict.get('secret', None)
        self._app_desc = app_dict.get('description', None)

    @property
    def name(self):
        return self._app_name

    @property
    def id(self):
        return self._app_id

    @property
    def description(self):
        return self._app_description

    @property
    def secret(self):
        return self._app_secret

    @property
    def dict(self):
        return self._app_dict

    def __repr__(self):
        return (f"<IDMApplication id: {self._app_id}, "
                f"name: \"{self._app_name}\", "
                f"description: \"{self._app_desc}\">")


class IDMProxy(object):
    """
    This class represent an application's proxy inside the Keyrock IDM.

    Attributes:
        id (str): the id of the proxy.
        password (str): the password of the proxy (it is available only
            at the proxy creation).
        dict (str): the dictionary that is passed to the constructor (it can be
            used to retrieve optional attributes returned by the IDM).
    """
    def __init__(self, proxy_id: str = None, proxy_dict: dict = None):
        """
        Inits IDMProxy.

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
        self._proxy_dict = proxy_dict
        self._proxy_id = proxy_id or proxy_dict['id']
        self._proxy_password = proxy_dict.get('password', None)
        self._proxy_oauth_client_id = proxy_dict.get('oauth_client_id', None)

    @property
    def id(self):
        return self._proxy_id

    @property
    def password(self):
        return self._proxy_password

    @property
    def dict(self):
        return self._proxy_dict

    def __repr__(self):
        return (f"<IDMProxy id: {self._proxy_id}, oauth_client_id: "
                f"{self._proxy_oauth_client_id}>")
