# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from azure.identity import DefaultAzureCredential
from azure.mgmt.playwrighttesting import PlaywrightTestingMgmtClient

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-playwrighttesting
# USAGE
    python accounts_update.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


def main():
    client = PlaywrightTestingMgmtClient(
        credential=DefaultAzureCredential(),
        subscription_id="00000000-0000-0000-0000-000000000000",
    )

    response = client.accounts.update(
        resource_group_name="dummyrg",
        name="myPlaywrightAccount",
        properties={"properties": {"regionalAffinity": "Enabled"}, "tags": {"Division": "LT", "Team": "Dev Exp"}},
    )
    print(response)


# x-ms-original-file: specification/playwrighttesting/resource-manager/Microsoft.AzurePlaywrightService/preview/2023-10-01-preview/examples/Accounts_Update.json
if __name__ == "__main__":
    main()
