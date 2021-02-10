#!/usr/bin/python3

from myLibForAzure.LoginToAccount import getResourceClient

resourceClient = getResourceClient()

# Retrieve the list of resources in "aks-cluster-rg" (change to any name desired).
# The expand argument includes additional properties in the output.
resource_list = resourceClient.resources.list_by_resource_group(
    "aks-cluster-rg",
    expand = "createdTime,changedTime"
)

# Show the resources in formatted output

for resource in list(resource_list):
    if ( resource.type == "Microsoft.Compute/disks"):
        print(resource.name)
