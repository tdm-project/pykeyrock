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

from .models import IDMApplication, IDMOrganization, IDMProxy, IDMUser, IDMRole
import dateutil.parser
import inspect
import json
import logging
import requests
from http.client import responses


def get_auth_token(host: str, port: int, user: str, password: str):
    url = f"http://{host}:{port}/v1/auth/tokens"
    payload = {
        "name": user,
        "password": password
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    expires = dateutil.parser.isoparse(response.json()['token']['expires_at'])
    expires = expires.strftime("%c")

    token = response.headers['X-Subject-Token']

    return(token, expires)


class IDMManager(object):
    def __init__(self, host: str, port: int, auth_token: str):
        self._host = host
        self._port = port
        self._idm_url = f"http://{host}:{port}"
        self._auth_token = auth_token

        self._logger = logging.getLogger('keyrock.IDMManager')
        self._logger.debug(
            'creating an instance of IDMManager (%s, %s)',
            self._idm_url, self._auth_token)

    def _log_response(self, response):
        _func_name = inspect.stack()[1].function
        _http_ver = ('HTTP/1.1' if
                     response.raw.version == 11 else 'HTTP/1.0')
        _level = logging.DEBUG if response.status_code < 400 else logging.ERROR

        if response.status_code < 400:
            _reason = ""
        elif 'error' in response.json():
            _reason = f"\"{response.json()['error']['message']}\""
        else:
            _reason = f"\"{response.json()}\""

        self._logger.log(
            _level,
            (f'{_func_name}() - '
             f'{self._idm_url} "{response.request.method} '
             f'{response.request.path_url} {_http_ver}" '
             f'{response.status_code} "{responses[response.status_code]}": '
             f'{_reason}'))

    def get_oauth2_token(self, user: str, password: str,
                         application_secret: str, permanent: bool):
        url = f"{self._idm_url}/oauth2/token"
        payload = {
            "username": user,
            "password": password,
            "grant_type": "password"
        }

        if permanent:
            payload.update({"scope": "permanent"})

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {application_secret}',
            'Accept': 'application/json'
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload)
        self._log_response(response)
        response.raise_for_status()

        return response.json()['access_token']

    ###########################################################################
    # ORGANIZATIONS section
    ###########################################################################
    def get_organization(self, organization_id: str):
        """
        Retrieves information about the organization with the given id,
        if exists.

        Args:
            organization_id (str): The organization id.

            Returns:
                - an IDMOrganization object with the organization details
                - None if the organization does not exist.
        """
        url = f"{self._idm_url}/v1/organizations/{organization_id}"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("GET", url, headers=headers)
        self._log_response(response)

        if response.status_code == requests.codes.ok:
            _organization = IDMOrganization(
                org_dict=response.json()['organization'])
        else:
            _organization = None

        return _organization

    def list_organizations(self):
        """
        Returns a list of all the organizations in the IDM.

        Returns:
            - a list of IDMOrganization objects.
        """
        url = f"{self._idm_url}/v1/organizations"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("GET", url, headers=headers)
        self._log_response(response)

        _org_list = list()
        if response.status_code == requests.codes.ok:
            for _org in response.json()['organizations']:
                _org_list.append(
                    IDMOrganization(org_dict=_org['Organization']))

        return _org_list

    def delete_organization(self, organization_id: str):
        """
        Deletes the organizations with the given id, if exist.
        WARNING: it does not asks for confirmation!

        Args:
            organization_id (str): The organization id.

        Raises:
            HTTPError if the operation was not successfull.

        Reference:
            https://github.com/FIWARE/tutorials.Identity-Management#delete-an-organization
        """
        url = f"{self._idm_url}/v1/organizations/{organization_id}"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("DELETE", url, headers=headers)
        self._log_response(response)

        response.raise_for_status()

    def get_organizations_by_name(self, org_name: str):
        """
        Retrieves information about the organizations with the given name,
        if exist. Warning: more than one organization can exist with the same
        name.

        Args:
            organization_name (str): The organization name.

            Returns:
                - a list of IDMOrganization objects.
        """
        orgs = self.list_organizations()
        org_list = list()

        for _org in orgs:
            if _org.name == org_name:
                org_list.append(_org)

        if len(org_list) > 1:
            self._logger.warning(
                'multiple organization with the name "%s" found',
                org_name)

        return org_list

    def create_organization(self, name, description: str = None):
        """
        Creates a new organization.
        Warning: more than one organization can be created with the same!

        Args:
            name (str): The organization's name.
            description (str): The organization's description.

            Returns:
                - the IDMOrganization object.
        """
        url = f"{self._idm_url}/v1/organizations"

        # XXX: Due to a bug (?) in Keyrock an empty-string description is
        # refused with a 500 error code. None or a missing description key are
        # accepted but disrupt the database.
        payload = {
            "organization": {
                "name": name,
                "description":
                    description or f"This is the {name} organization"
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))
        self._log_response(response)
        response.raise_for_status()

        self._logger.info(
            "IDM organizzation \"%s\" created", name)
        return IDMOrganization(
            name, response.json()['organization'])

    def update_organization(self, organization_id: str):
        raise NotImplementedError()

    ###########################################################################
    # APPLICATIONS section
    ###########################################################################
    def get_application(self, application_id: str):
        """
        Retrieves information about the application with the given id,
        if exists.

        Args:
            application_id (str): The application id.

        Returns:
            - an IDMApplication object with the application details
            - None if the application does not exist.
        """
        url = f"{self._idm_url}/v1/applications/{application_id}"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("GET", url, headers=headers)
        self._log_response(response)

        if response.status_code == requests.codes.ok:
            _application = IDMApplication(
                app_dict=response.json()['application'])
        else:
            _application = None

        return _application

    def list_applications(self):
        """
        Returns a list of all the applications in the IDM.

        Returns:
            - a list of IDMApplication objects.
        """
        url = f"{self._idm_url}/v1/applications"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("GET", url, headers=headers)
        self._log_response(response)

        _app_list = list()
        if response.status_code == requests.codes.ok:
            for _app in response.json()['applications']:
                _app_list.append(
                    IDMApplication(app_dict=_app))

        return _app_list

    def delete_application(self, application_id: str):
        """
        Deletes the application with the given id, if exist.
        WARNING: it does not asks for confirmation!

        Args:
            application_id (str): The application id.

        Raises:
            HTTPError if the operation was not successfull.
        """
        url = f"{self._idm_url}/v1/applications/{application_id}"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("DELETE", url, headers=headers)
        self._log_response(response)

        response.raise_for_status()

    def get_applications_by_name(self, application_name: str):
        """
        Retrieves information about the applications with the given name, if
        exist. More than one applications can exists with the same name.

        Args:
            application_name (str): The application name.

            Returns:
                - a list of IDMApplication objects.
        """
        apps = self.list_applications()
        app_list = list()

        for _app in apps:
            if _app.name == application_name:
                app_list.append(_app)

        if len(app_list) > 1:
            self._logger.warning(
                'multiple applications with the name "%s" found',
                application_name)

        return app_list

    def create_application(self, name, description: str = None):
        """
        Creates a new application.
        Warning: more than one application can be created with the same!

        Args:
            name (str): The application's name.
            description (str): The organization's description.

        Returns:
            - the IDMApplication object.
        """
        url = f"{self._idm_url}/v1/applications"

        # XXX: Due to a bug (?) in Keyrock an empty-string description is
        # refused with a 500 error code. None or a missing description key are
        # accepted but disrupt the database.
        payload = {
            "application": {
                "name": name,
                "description":
                    description or f"{name} application protected by Keyrock",
                "redirect_uri": "http://localhost",
                "url": "http://localhost",
                "grant_type": [
                    "authorization_code",
                    "implicit",
                    "password"
                ],
                "token_types": ["permanent"]
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))
        self._log_response(response)
        response.raise_for_status()

        self._logger.info("IDM application \"%s\" created", name)
        return IDMApplication(name, response.json()['application'])

    def update_application(self, application_id: str):
        raise NotImplementedError()

    ###########################################################################
    # APPLICATION's PROXY section
    ###########################################################################
    def get_proxy(self, application_id):
        """
        Retrieves information about the proxy, if any, of the
        given application.

        Args:
            application_id (str): The application id.

            Returns:
                - the IDMProxy object, if exists;
                - None if proxy is not set for the application.

        Reference:
            https://fiware-tutorials.readthedocs.io/en/stable/pep-proxy/#pep-proxy-crud-actions
        """
        url = (
            f"{self._idm_url}/v1/applications/"
            f"{application_id}/pep_proxies")
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("GET", url, headers=headers)
        self._log_response(response)

        if response.status_code == requests.codes.ok:
            _proxy = IDMProxy(proxy_dict=response.json()['pep_proxy'])
        else:
            _proxy = None

        return _proxy

    def create_proxy(self, application_id):
        """
        Creates a new proxy for the given application.

        Args:
            application_id (str): The application id.

        Returns:
            - the IDMApplication object.

        Reference:
            https://fiware-tutorials.readthedocs.io/en/stable/pep-proxy/#pep-proxy-crud-actions
        """
        url = (f"{self._idm_url}/v1/applications/{application_id}/pep_proxies")

        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }

        response = requests.request("POST", url, headers=headers)
        self._log_response(response)
        response.raise_for_status()

        self._logger.info(
            "IDM proxy \"%s\" created",
            response.json()['pep_proxy']['id'])

        return IDMProxy(proxy_dict=response.json()['pep_proxy'])

    def delete_proxy(self, application_id: str):
        """
        Deletes the existing PEP Proxy Account for the given application.
        WARNING: it does not asks for confirmation!

        Args:
            application_id (str): The application id.

        Raises:
            HTTPError if the operation was not successfull.
        Reference:
            https://fiware-tutorials.readthedocs.io/en/stable/pep-proxy/#pep-proxy-crud-actions
        """
        url = f"{self._idm_url}/v1/applications/{application_id}/pep_proxies"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("DELETE", url, headers=headers)
        self._log_response(response)
        response.raise_for_status()

        self._logger.info(
            "IDM proxy for application \"%s\" deleted",
            application_id)

    def reset_proxy(self, application_id: str):
        """
        Renews the password of the PEP Proxy Account for the given application.

        Args:
            application_id (str): The application id.

        Returns:
            - the IDMApplication object.

        Reference:
            https://fiware-tutorials.readthedocs.io/en/stable/pep-proxy/#pep-proxy-crud-actions
        """
        _proxy = self.get_proxy(application_id)

        url = f"{self._idm_url}/v1/applications/{application_id}/pep_proxies"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("PATCH", url, headers=headers)
        response.raise_for_status()

        self._logger.info(
            "IDM password for PEP Proxy Account \"%s\" refreshed",
            _proxy.id)

        _proxy.update(response.json())

        return _proxy

    ###########################################################################
    # USERS section
    ###########################################################################
    def create_user(self, user_email: str, user_password: str,
                    user_name: str = None):
        """
        Creates a new user in the IDM System.

        Args:
            user_email (str): mandatory, the user's email and the user's login;
                              it must be unique;
            user_password (str): mandatory, the password of the user to create;
            user_name (str): the user's name;

        Returns:
            - the IDMUser object.

        Reference:
            https://fiware-tutorials.readthedocs.io/en/stable/identity-management/#user-crud-actions
        """
        url = f"{self._idm_url}/v1/users"
        payload = {
            "user": {
                "username": user_name,
                "email": user_email,
                "password": user_password
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))
        self._log_response(response)
        response.raise_for_status()

        self._logger.info("IDM user \"%s\" created", user_email)

        return IDMUser(user_dict=response.json()['user'])

    def get_user(self, user_id: str):
        """
        Retrieves information about the user with the given id, if exists.

        Args:
            user_id (str): The user's id

        Returns:
            - an IDMUSer object with the user's details
            - None if the user does not exist.

        Reference:
            https://fiware-tutorials.readthedocs.io/en/stable/identity-management/#user-crud-actions
        """
        url = f"{self._idm_url}/v1/users/{user_id}"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("GET", url, headers=headers)
        self._log_response(response)

        if response.status_code == requests.codes.ok:
            _user = IDMUser(
                user_dict=response.json()['user'])
        else:
            _user = None

        return _user

    def list_users(self):
        """
        Returns a list of all the users in the IDM.

        Returns:
            - a list of IDMUser objects.

        Reference:
            https://fiware-tutorials.readthedocs.io/en/stable/identity-management/#user-crud-actions
        """
        url = f"{self._idm_url}/v1/users"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("GET", url, headers=headers)
        self._log_response(response)

        _user_list = list()
        if response.status_code == requests.codes.ok:
            for _user in response.json()['users']:
                _user_list.append(
                    IDMUser(user_dict=_user))

        return _user_list

    def update_user(self, user_id: str):
        raise NotImplementedError()

    def delete_user(self, user_id: str):
        """
        Deletes the user with the given id, if exist.
        WARNING: it does not asks for confirmation!

        Args:
            user_id (str): The user id.

        Raises:
            HTTPError if the operation was not successfull.

        Reference:
            https://fiware-tutorials.readthedocs.io/en/stable/identity-management/#user-crud-actions
        """
        url = f"{self._idm_url}/v1/users/{user_id}"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("DELETE", url, headers=headers)
        self._log_response(response)

        response.raise_for_status()

    ###########################################################################
    # ROLES section
    ###########################################################################
    def list_roles(self, application_id):
        """
        Returns a list of all the roles in the IDM for the given application.

        Args:
            application_id (str): The application id.

        Returns:
            - a list of IDMRole objects.

        Reference:
            https://keyrock.docs.apiary.io/reference/keyrock-api/roles
        """
        url = f"{self._idm_url}/v1/applications/{application_id}/roles"
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("GET", url, headers=headers)
        self._log_response(response)

        _role_list = list()
        if response.status_code == requests.codes.ok:
            for _role in response.json()['roles']:
                _role_list.append(
                    IDMRole(role_dict=_role, application_id=application_id))

        return _role_list

    def create_role(self, application_id: str, role_name: str):
        """
        Creates a new role for the given application in the IDM System.

        Warning: more than one role can exist with the same name in the same
        application.

        Args:
            application_id (str): mandatory, the id of the application to which
                                  the role belongs to;
            role_name (str): mandatory, the role name; it must not be empty.

        Returns:
            - the IDMRole object.

        Raises:
            HTTPError if the operation was not successfull.

        Reference:
            https://keyrock.docs.apiary.io/reference/keyrock-api/roles
        """
        url = f"{self._idm_url}/v1/applications/{application_id}/roles"
        payload = {
            "role": {
                "name": role_name
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))
        self._log_response(response)
        response.raise_for_status()

        self._logger.info("IDM role \"%s\" created", role_name)

        return IDMRole(role_dict=response.json()['role'],
                       application_id=application_id)

    def get_role(self, application_id: str, role_id: str):
        """
        Retrieves information about the role with the given id that belongs to
        the given application, if exists.

        Args:
            application_id (str): mandatory, the id of the application to which
                                  the role belongs to;
            role_id (str): mandatory, the role id;

        Returns:
            - an IDMRole object with the role's details
            - None if the role does not exist.

        Reference:
            https://keyrock.docs.apiary.io/reference/keyrock-api/roles
        """
        url = (f"{self._idm_url}/v1/applications/{application_id}"
               f"/roles/{role_id}")
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("GET", url, headers=headers)
        self._log_response(response)

        if response.status_code == requests.codes.ok:
            _role = IDMRole(
                role_dict=response.json()['role'],
                application_id=application_id)
        else:
            _role = None

        return _role

    def update_role(self, application_id: str, roled_id: str):
        raise NotImplementedError()

    def delete_role(self, application_id: str, role_id: str):
        """
        Deletes the role with the given id, that belongs to
        the given application, if exists.
        WARNING: it does not asks for confirmation!

        Args:
            application_id (str): mandatory, the id of the application to which
                                  the role belongs to;
            role_id (str): mandatory, the role id;

        Raises:
            HTTPError if the operation was not successfull.

        Reference:
            https://keyrock.docs.apiary.io/reference/keyrock-api/roles
        """
        url = (f"{self._idm_url}/v1/applications/{application_id}"
               f"/roles/{role_id}")
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-token': self._auth_token
        }
        response = requests.request("DELETE", url, headers=headers)
        self._log_response(response)

        response.raise_for_status()
