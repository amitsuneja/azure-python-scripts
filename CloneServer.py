#!/usr/bin/python3

import json
import argparse
from pprint import pprint 
from myLibForAzure.LoginToAccount import ifResourceGroupExist
from myLibForAzure.LoginToAccount import ifVmExistInResourceGroup
from myLibForAzure.LoginToAccount import ifVnetExist
from myLibForAzure.LoginToAccount import ifSubnetExist
from myLibForAzure.LoginToAccount import ifStorageAccountExist
from myLibForAzure.LoginToAccount import getSizeOfParticularVmInResourceGroup
from myLibForAzure.LoginToAccount import getSubnetInfoObject
from myLibForAzure.LoginToAccount import getNicParamsObject
from myLibForAzure.LoginToAccount import createNic
from myLibForAzure.LoginToAccount import getListOfAllDisksNameForParticularVminResourceGroup
from myLibForAzure.LoginToAccount import getOsDiskDictForParticularVminResourceGroup
from myLibForAzure.LoginToAccount import getIDofDiskWithName
from myLibForAzure.LoginToAccount import getReplaceText
from myLibForAzure.LoginToAccount import diskCreate
from myLibForAzure.LoginToAccount import getStorageProfiletoAttachExistingOsDisk
from myLibForAzure.LoginToAccount import getHardwareProfile
from myLibForAzure.LoginToAccount import getNetworkProfile
from myLibForAzure.LoginToAccount import getVmProfile
from myLibForAzure.LoginToAccount import createVm

ap = argparse.ArgumentParser()
ap.add_argument("-srg", "--source_resource_group",required=True,help="Mandate : -srg or --source_resource_group")
ap.add_argument("-svm", "--source_virtual_machine",required=True,help="Mandate : -svm or --source_virtual_machine")
ap.add_argument("-drg", "--destination_resource_group",required=True,help="Mandate : -srg or --source_resource_group")
ap.add_argument("-dvm", "--destination_virtual_machine",required=True,help="Mandate : -dvm or --destination_virtual_machine")
ap.add_argument("-dvnet", "--destination_vnet",required=True,help="Mandate : -dvnet or --destination_vnet")
ap.add_argument("-dsub", "--destination_subnet",required=True,help="Mandate : -dsub or --destination_subnet")
ap.add_argument("-dsa", "--destination_storage_account",required=True,help="Mandate : -dsa or --destination_storage_account")

cli_argument_dict = vars(ap.parse_args())

srcResGrp=cli_argument_dict['source_resource_group'].lower()
srcVmName=cli_argument_dict['source_virtual_machine'].upper()
dstResGrp=cli_argument_dict['destination_resource_group'].lower()
dstVmName=cli_argument_dict['destination_virtual_machine'].upper()
dstVNet=cli_argument_dict['destination_vnet'].lower()
dstSubnet=cli_argument_dict['destination_subnet'].lower()
dstStorageAccount=cli_argument_dict['destination_storage_account'].lower()

#Defining Variables
dstIpConfigName =  dstVmName + "IpConfig"
nicNameForDstVmName = dstVmName + "__eth0"

print("checking existance of Source Resource Group: {}".format(srcResGrp))
result=ifResourceGroupExist(srcResGrp)
print("Resource Group: {} , result: {} script will continue ...\n".format(srcResGrp,result))
if not result:
    print("Source Resource Group {} does not exist".format(srcResGrp))
    print("ifResourceGroupExist(srcResGrp) does not returned expected result\n".format(srcResGrp))
    exit()

print("checking existance of Destination Resource Group: {}".format(dstResGrp))
result=ifResourceGroupExist(dstResGrp)
print("Resource Group: {}, result: {} script will continue ...\n".format(dstResGrp, result))
if not result:
    print("Destination Resource Group {} does not exist".format(dstResGrp))
    exit()

print("checking existance of Source VM: {} in Source Resource Group:{} ".format(srcVmName,srcResGrp))
result=ifVmExistInResourceGroup(srcVmName,srcResGrp)
if (result == True):
    srcVMSize = getSizeOfParticularVmInResourceGroup(srcResGrp,srcVmName)
    print("result:{}, Vmsize:{} script will continue ...\n".format(result,srcVMSize))
if (result == False):
    print("Error - Source VM: {} , does not exist in Source Resource Group:{} ,  result:{}\n".format(srcVmName,srcResGrp,result))
    exit()

print("checking existance of Destination VM: {} in Destination Resource Group:{} ".format(dstVmName,dstResGrp))
result=ifVmExistInResourceGroup(dstVmName,dstResGrp)
if (result == False):
    print("result:{} script will continue ...\n".format(result))
if (result == True):
    print("Error - Destination VM: {} ,exist in Destination Resource Group:{} ,  result:{}\n".format(dstVmName,dstResGrp,result))
    exit()

print("check existance of Destination Vnet:{}".format(dstVNet))
result=ifVnetExist(dstVNet)
if (result[0] == True):
    dstVNetResGrp = result[1]
    dstVNetLocation = result[2]
    print("result:{}...Destination Vnet:{} exist in  Resource Group:{}\n".format(result[0],dstVNet,dstVNetResGrp))
if (result[0] == False):
    print("Error - Destination Vnet: {} does not exist.".format(dstVNet))
    exit()

print("check existence of Subnet:{}".format(dstSubnet))
result=ifSubnetExist(dstSubnet,dstVNetResGrp,dstVNet)
if (result == True):
    print("result:{}.. Destination Subnet:{} exist in  Resource Group:{}, its vnet is:{}\n".format(result,dstSubnet,dstVNetResGrp,dstVNet))

print("checking existance of Storage Account:{}".format(dstStorageAccount))
result = ifStorageAccountExist(dstStorageAccount)
if (result == True):
    print("Storage Account:{} ,result:{}. script will continue ...\n".format(dstStorageAccount,result))
if (result == False):
    print("Error - Storage Account:{} does not exist\n".format(dstStorageAccount))

print("Collecting Object for subnetInfo to create Network Card:{}".format(nicNameForDstVmName))
subnet_info = getSubnetInfoObject(dstVNetResGrp,dstVNet,dstSubnet)
if subnet_info:
    print("We need subnet_info.id: {} to create NIC\n".format(subnet_info.id))
else:
    print("getSubnetInfoObject({},{},{}) failed to fetch subnetInfoObject\n".format(dstVNetResGrp,dstVNet,dstSubnet))


print("collecting Nic Params object to create Nic:{}".format(nicNameForDstVmName))
nicParams = getNicParamsObject(dstVNetLocation,dstIpConfigName,subnet_info)
print(nicParams)
print("\n")


print("Network Card Creation is in progress... NIC:{}".format(nicNameForDstVmName))
nicCreationResult=createNic(dstVNetResGrp,nicNameForDstVmName,nicParams)
tempVarNicId=nicCreationResult.result().id
print(tempVarNicId)
print("\n")



print("Collecting DiskNames for SourceVm: {} in ResourceGroup: {} ".format(srcVmName,srcResGrp))
print("\n")
SrcDiskList=getListOfAllDisksNameForParticularVminResourceGroup(srcResGrp,srcVmName)
finalDiskList=list()
lunNumber=0
for diskName in SrcDiskList:
    diskDict = dict()
    if (lunNumber == 0):
        diskDict['lun'] = "osdisk"
    else:
        diskDict['lun'] = lunNumber - 1
    lunNumber = lunNumber + 1
    diskDict['srcDiskName'] = diskName
    diskDict['srcDiskId'] = getIDofDiskWithName(diskName)
    diskDict['dstDiskName'] = getReplaceText(diskName,srcVmName,dstVmName)
    finalDiskList.append(diskDict)

diskCreationResultList = list()
for item in finalDiskList:
    print("Disk Creation in progress...")
    print("Lun : ",item['lun'])
    print("Source Disk Name: ",item['srcDiskName'])
    print("Destination Disk Name: ",item['dstDiskName'])
    print("Source Disk Resource ID: ",item['srcDiskId'])
    result = diskCreate(dstResGrp,item['dstDiskName'],dstVNetLocation,item['srcDiskId'])
    diskCreationResultList.append(result.result())
    print("\n")

tempVarDiskId=diskCreationResultList[0].id
tempVarDiskName=diskCreationResultList[0].name

print("Fetching Storage Profile:\n")
storageProfile=getStorageProfiletoAttachExistingOsDisk(tempVarDiskId,dstResGrp,tempVarDiskName,"Linux")
pprint(storageProfile)
print("\n")

print("Fetching Hardware Profile:\n")
hardwareProfile=getHardwareProfile(srcVMSize)
pprint(hardwareProfile)
print("\n")

print("Fetching Network Profile:\n")
networkProfile=getNetworkProfile(tempVarNicId)
pprint(networkProfile)
print("\n")

print("Fetching Vm Profile:\n")
vmProfile = getVmProfile(dstVNetLocation,storageProfile,hardwareProfile,networkProfile)
pprint(vmProfile)
print("\n")

createVmResult=createVm(dstResGrp,dstVmName,vmProfile)
print(createVmResult.result())
