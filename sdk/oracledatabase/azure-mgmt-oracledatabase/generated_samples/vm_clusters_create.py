# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from typing import Any, IO, Union

from azure.identity import DefaultAzureCredential

from azure.mgmt.oracledatabase import OracleDatabaseMgmtClient

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-oracledatabase
# USAGE
    python vm_clusters_create.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


def main():
    client = OracleDatabaseMgmtClient(
        credential=DefaultAzureCredential(),
        subscription_id="00000000-0000-0000-0000-000000000000",
    )

    response = client.cloud_vm_clusters.begin_create_or_update(
        resource_group_name="rg000",
        cloudvmclustername="cluster1",
        resource={
            "location": "eastus",
            "properties": {
                "backupSubnetCidr": "172.17.5.0/24",
                "cloudExadataInfrastructureId": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg000/providers/Oracle.Database/cloudExadataInfrastructures/infra1",
                "clusterName": "cluster1",
                "cpuCoreCount": 2,
                "dataCollectionOptions": {
                    "isDiagnosticsEventsEnabled": False,
                    "isHealthMonitoringEnabled": False,
                    "isIncidentLogsEnabled": False,
                },
                "dataStoragePercentage": 100,
                "dataStorageSizeInTbs": 1000,
                "dbNodeStorageSizeInGbs": 1000,
                "dbServers": ["ocid1..aaaa"],
                "displayName": "cluster 1",
                "domain": "domain1",
                "giVersion": "19.0.0.0",
                "hostname": "hostname1",
                "isLocalBackupEnabled": False,
                "isSparseDiskgroupEnabled": False,
                "licenseModel": "LicenseIncluded",
                "memorySizeInGbs": 1000,
                "nsgCidrs": [
                    {"destinationPortRange": {"max": 1522, "min": 1520}, "source": "10.0.0.0/16"},
                    {"source": "10.10.0.0/24"},
                ],
                "ocpuCount": 3,
                "scanListenerPortTcp": 1050,
                "scanListenerPortTcpSsl": 1025,
                "sshPublicKeys": ["ssh-key 1"],
                "subnetId": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg000/providers/Microsoft.Network/virtualNetworks/vnet1/subnets/subnet1",
                "timeZone": "UTC",
                "vnetId": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg000/providers/Microsoft.Network/virtualNetworks/vnet1",
            },
            "tags": {"tagK1": "tagV1"},
        },
    ).result()
    print(response)


# x-ms-original-file: specification/oracle/resource-manager/Oracle.Database/stable/2023-09-01/examples/vmClusters_create.json
if __name__ == "__main__":
    main()
