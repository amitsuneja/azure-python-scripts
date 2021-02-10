#!/usr/bin/python3

from myLibForAzure.LoginToAccount import getComputeClient


computeClient = getComputeClient()
listOfVmNames = [vm.name for vm in computeClient.virtual_machines.list_all()]

for VmName in listOfVmNames:
    print(VmName)
