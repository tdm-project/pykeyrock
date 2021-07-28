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

from lorem_text import lorem
import random


def random_org_name(prefix='pykeyrock unittest', words=2):
    return f"{prefix} {lorem.words(words)}".capitalize()


def random_org_description(words=5):
    return lorem.words(words).capitalize() + '.'


def random_app_name(prefix='pykeyrock unittest', words=2):
    return f"{prefix} {lorem.words(words)}".capitalize()


def random_app_description(words=5):
    return lorem.words(words).capitalize() + '.'


def random_role_name(prefix='pykeyrock unittest', words=2):
    _w = prefix.split() + lorem.words(2).split()
    return ''.join(list(map(str.capitalize, _w)))


def random_user_email(prefix='pykeyrock_unittest'):
    _login, _domain, _tld = lorem.words(3).split()
    return f"{prefix}_{_login}@{_domain}.{_tld[0:2]}".lower()


def random_user_password():
    return '.'.join(lorem.words(3).split()).lower()


def random_user_name(prefix='pykeyrock', words=2):
    return f"{prefix} {lorem.words(words)}".capitalize()


def random_permission_name(prefix='pykeyrock unittest', words=2):
    return f"{prefix} {lorem.words(words)}".capitalize()


def random_permission_action(prefix='pykeyrock unittest', words=2):
    _actions = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    return random.choice(_actions)


def random_permission_resource(prefix='pykeyrock unittest', words=1):
    _w = prefix.split() + lorem.words(words).split()
    return '/'.join(list(map(str.lower, _w)))
