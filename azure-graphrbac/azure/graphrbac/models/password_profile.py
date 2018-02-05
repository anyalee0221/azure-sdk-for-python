# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PasswordProfile(Model):
    """The password profile associated with a user.

    :param additional_properties: Unmatched properties from the message are
     deserialized this collection
    :type additional_properties: dict[str, object]
    :param password: Password
    :type password: str
    :param force_change_password_next_login: Whether to force a password
     change on next login.
    :type force_change_password_next_login: bool
    """

    _validation = {
        'password': {'required': True},
    }

    _attribute_map = {
        'additional_properties': {'key': '', 'type': '{object}'},
        'password': {'key': 'password', 'type': 'str'},
        'force_change_password_next_login': {'key': 'forceChangePasswordNextLogin', 'type': 'bool'},
    }

    def __init__(self, password, additional_properties=None, force_change_password_next_login=None):
        super(PasswordProfile, self).__init__()
        self.additional_properties = additional_properties
        self.password = password
        self.force_change_password_next_login = force_change_password_next_login
