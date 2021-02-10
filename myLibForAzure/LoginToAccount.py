from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import DiskCreateOption



from .SelectAccount import tenentid
from .SelectAccount import clientid
from .SelectAccount import clientsecret
from .SelectAccount import subscriptionid

# Acquire a credential object using CLI-based authentication, We are not using this method.
# credential = AzureCliCredential()

def getClientSecretCredential():
    secretCredential = ClientSecretCredential(tenentid,clientid,clientsecret)
    return secretCredential

def getComputeClient():
    secretCredential = getClientSecretCredential()
    computeClient = ComputeManagementClient(secretCredential,subscriptionid)
    return computeClient

def getResourceClient():
    secretCredential = getClientSecretCredential()
    resourceClient = ResourceManagementClient(secretCredential, subscriptionid)
    return resourceClient

def getSubscriptionClient():
    secretCredential = getClientSecretCredential()
    subscriptionClient = SubscriptionClient(secretCredential)
    return subscriptionClient

def getNetworkClient():
    secretCredential = getClientSecretCredential()
    networkClient = NetworkManagementClient(secretCredential, subscriptionid)
    return networkClient

def getListOfLocations():
    SubscriptionClient = getSubscriptionClient()
    locations = SubscriptionClient.subscriptions.list_locations(subscriptionid)
    return list(locations)

def getStorageClient():
    secretCredential = getClientSecretCredential()
    StorageClient = StorageManagementClient(secretCredential, subscriptionid)
    return StorageClient

def getListOfStorageAccountSKUS():
    storageClient= getStorageClient()
       # use set to remove duplicates.
    skus = {sku.name for sku in storageClient.skus.list()}
    return list(skus)

def getListOfStorageAccountNames():
    storageClient = getStorageClient()
    storageAccountslist = [item.name for item in storageClient.storage_accounts.list()]
    return storageAccountslist

def getListOfStorageAccountIds():
    storageClient = getStorageClient()
    storageAccountslist = [item.id for item in storageClient.storage_accounts.list()]
    return storageAccountslist

def getDictOfStorageAccountNameKeyAndIdValue():
    storageClient = getStorageClient()
    storageDict = dict()
    for item in storageClient.storage_accounts.list():
        storageDict[item.name] = item.id
    return storageDict    

def ifStorageAccountExist(storageAccountName):
    dictOfStorageAccountNameKeyAndIdValue = getDictOfStorageAccountNameKeyAndIdValue()
    result = False
    for key in dictOfStorageAccountNameKeyAndIdValue.keys():
        if key.casefold() == storageAccountName.casefold():
            result = True
            break
        else:
            continue
    return result

def getListOfDetailedDictsOfResourceGroup():
    resourceClient = getResourceClient()
    ListOfDetailedDictsOfResourceGroup = list()
    for item in resourceClient.resource_groups.list():
        resourceGroupDict = dict()
        resourceGroupDict['name'] = item.name
        resourceGroupDict['id'] = item.id
        resourceGroupDict['location'] = item.location
        ListOfDetailedDictsOfResourceGroup.append(resourceGroupDict)
    return ListOfDetailedDictsOfResourceGroup

def ifResourceGroupExist(resGrpName):
    result = False
    ListOfDetailedDictsOfResourceGroup = getListOfDetailedDictsOfResourceGroup()
    # string.casefold() will match lower and upper case both
    for item in ListOfDetailedDictsOfResourceGroup:
        if (item['name'].casefold() == resGrpName.casefold()):
            result = True
            break
        else:
            continue
    return result

def getListOfDetailedDictsOfVmsInResourceGroup(resGrpName):
    computeClient = getComputeClient()
    listOfDetailedDictsOfVmsInResourceGroup = list()
    """
    for item in computeClient.virtual_machines.list_all():
    vm_list = compute_client.virtual_machines.list('resource_group_name')
    i= 0
    for vm in vm_list:
        array = vm.id.split("/")
        resource_group = array[4]
        vm_name = array[-1]
        statuses = compute_client.virtual_machines.instance_view(resource_group, vm_name).statuses
        status = len(statuses) >= 2 and statuses[1]
        if status and status.code == 'PowerState/running':
        print(vm_name)
    """
    for item in computeClient.virtual_machines.list(resGrpName):
        detailedDictOfVmsInResourceGroup = dict()
        detailedDictOfVmsInResourceGroup['name'] = item.name
        detailedDictOfVmsInResourceGroup['id'] = item.id
        detailedDictOfVmsInResourceGroup['location'] = item.location
        detailedDictOfVmsInResourceGroup['zones'] = item.zones
        detailedDictOfVmsInResourceGroup['os_profile'] = item.os_profile
        detailedDictOfVmsInResourceGroup['availability_set'] = item.availability_set
        detailedDictOfVmsInResourceGroup['virtual_machine_scale_set'] = item.virtual_machine_scale_set
        detailedDictOfVmsInResourceGroup['proximity_placement_group'] = item.proximity_placement_group
        detailedDictOfVmsInResourceGroup['provisioning_state'] = item.provisioning_state
        detailedDictOfVmsInResourceGroup['license_type'] = item.license_type
        detailedDictOfVmsInResourceGroup['resource_group'] = resGrpName
        listOfDetailedDictsOfVmsInResourceGroup.append(detailedDictOfVmsInResourceGroup)
    return listOfDetailedDictsOfVmsInResourceGroup

def ifVmExistInResourceGroup(vmName,resGrpName):
    result = False
    listOfDetailedDictsOfVmsInResourceGroup = getListOfDetailedDictsOfVmsInResourceGroup(resGrpName)
    for item in listOfDetailedDictsOfVmsInResourceGroup:
        if (item['name'].casefold() == vmName.casefold()):
            result = True
            break
        else:
            continue
    return result

def getSizeOfParticularVmInResourceGroup(ResGrpName,VmName):
    computeClient = getComputeClient()
    detailsOfVM = computeClient.virtual_machines.get(ResGrpName, VmName, expand='instanceView')
    vmSize = detailsOfVM.hardware_profile.vm_size
    return vmSize


    
    # https://docs.microsoft.com/en-us/azure/virtual-machines/windows/python#get-information-about-the-vm
def printParticularVmDetailsinResourceGroup(ResGrpName,VmName):
    computeClient = getComputeClient()
    detailsOfVM = computeClient.virtual_machines.get(ResGrpName, VmName, expand='instanceView')
    print("hardwareProfile")
    print("   vmSize: ", detailsOfVM.hardware_profile.vm_size)
    print("\nstorageProfile")
    if detailsOfVM.storage_profile.image_reference:
        print("  imageReference")
        print("    publisher: ", detailsOfVM.storage_profile.image_reference.publisher)
        print("    offer: ", detailsOfVM.storage_profile.image_reference.offer)
        print("    sku: ", detailsOfVM.storage_profile.image_reference.sku)
        print("    version: ", detailsOfVM.storage_profile.image_reference.version)
    print("  osDisk")
    print("    osType: ", detailsOfVM.storage_profile.os_disk.os_type)
    print("    name: ", detailsOfVM.storage_profile.os_disk.name)
    print("    createOption: ", detailsOfVM.storage_profile.os_disk.create_option)
    print("    caching: ", detailsOfVM.storage_profile.os_disk.caching)
    
    if detailsOfVM.os_profile:
        print("\nosProfile")
        print("  computerName: ", detailsOfVM.os_profile.computer_name)
        print("  adminUsername: ", detailsOfVM.os_profile.admin_username)
        print("  provisionVMAgent: {0}".format(detailsOfVM.os_profile.windows_configuration.provision_vm_agent))
        print("  enableAutomaticUpdates: {0}".format(detailsOfVM.os_profile.windows_configuration.enable_automatic_updates))
    print("\nnetworkProfile")
    for nic in detailsOfVM.network_profile.network_interfaces:
        print("  networkInterface id: ", nic.id)

    if detailsOfVM.instance_view.vm_agent:
        print("\nvmAgent")
        print("  vmAgentVersion", detailsOfVM.instance_view.vm_agent.vm_agent_version)
        print("    statuses")
        for stat in detailsOfVM.instance_view.vm_agent.statuses:
            print("    code: ", stat.code)
            print("    displayStatus: ", stat.display_status)
            print("    message: ", stat.message)
            print("    time: ", stat.time)
    print("\ndisks");
    for disk in detailsOfVM.instance_view.disks:
        print("  name: ", disk.name)
        print("  statuses")
        for stat in disk.statuses:
            #print("    code: ", stat.code)
            #print("    displayStatus: ", stat.display_status)
            #print("    time: ", stat.time)
            print("______________________")
            print("    stat: ", stat)
    
    print("\nVM general status")
    print("  provisioningStatus: ", detailsOfVM.provisioning_state)
    print("  id: ", detailsOfVM.id)
    print("  name: ", detailsOfVM.name)
    print("  type: ", detailsOfVM.type)
    print("  location: ", detailsOfVM.location)
    print("\nVM instance status")
    for stat in detailsOfVM.instance_view.statuses:
        print("  code: ", stat.code)
        print("  displayStatus: ", stat.display_status)




def getListOfDetailedDictsOfVnets():
    NetworkClient = getNetworkClient()
    listOfDetailedDictsOfVnets = list()
    #for item in NetworkClient.subnets.list(): need Vnet and resource Group
    #    print(item)
    for item in NetworkClient.virtual_networks.list_all():
        detailedDictsOfVnets = dict()
        detailedDictsOfVnets['id'] = item.id
        # string.split("splitterWord") return list , [4] fetch 5th element of list
        detailedDictsOfVnets['resource_group'] = item.id.split("/")[4]
        detailedDictsOfVnets['name'] = item.name
        detailedDictsOfVnets['location'] = item.location
        detailedDictsOfVnets['extended_location'] = item.extended_location
        detailedDictsOfVnets['provisioning_state'] = item.provisioning_state
        listOfDetailedDictsOfVnets.append(detailedDictsOfVnets)
    return listOfDetailedDictsOfVnets


def ifVnetExist(vNetName):
    ListOfDetailedDictsOfVnets = getListOfDetailedDictsOfVnets()
    result = [False,False,False]
    for item in ListOfDetailedDictsOfVnets:
        if (item['name'].casefold() == vNetName.casefold()):
            result[0] = True
            result[1] = item['resource_group']
            result[2] = item['location']
            break
        else:
            continue
    return result


def getListOfDetailedDictsOfSubnets(resGrpName,VNetName):
    NetworkClient = getNetworkClient()
    listOfDetailedDictsOfSubnets = list()
    for item in NetworkClient.subnets.list(resGrpName,VNetName): #need Vnet and resource Group
        detailedDictsOfSubnets = dict()
        detailedDictsOfSubnets['id'] = item.id
        detailedDictsOfSubnets['name'] = item.name
        detailedDictsOfSubnets['address_prefix'] = item.address_prefix
        detailedDictsOfSubnets['route_table'] = item.route_table
        detailedDictsOfSubnets['nat_gateway'] = item.nat_gateway
        detailedDictsOfSubnets['provisioning_state'] = item.provisioning_state
        listOfDetailedDictsOfSubnets.append(detailedDictsOfSubnets)
    return listOfDetailedDictsOfSubnets

def ifSubnetExist(subnetNameToCheck,resGrpName,VNetName):
    listOfDetailedDictsOfSubnets = getListOfDetailedDictsOfSubnets(resGrpName,VNetName)
    result = False
    for item in listOfDetailedDictsOfSubnets:
        if(item['name'].casefold() == subnetNameToCheck.casefold()):
            result = True
            break
        else:
            continue
    return result

#def createNic(VNet,Subnet,VNetResGrp,VNetLocation,VmName):
#    nicName = VmName + "__eth0"

def getSubnetInfoObject(ResourceGroupName,vNetName,subnetName):
    NetworkClient = getNetworkClient()
    subnet_info = NetworkClient.subnets.get(ResourceGroupName,vNetName,subnetName)
    return subnet_info

def getNicParamsObject(LOCATION,someName,subnet_info):
    nic_params = {
        'location': LOCATION,
        'ip_configurations': [{
            'name': someName,
            'subnet': {
                'id': subnet_info.id
            }
        }]
    }
    return nic_params


def createNic(ResGrpName,nicName,nicParams):
    NetworkClient = getNetworkClient()
    nicCreationPoller = NetworkClient.network_interfaces.begin_create_or_update(ResGrpName,nicName,nicParams,)
    return nicCreationPoller

def getListOfAllDisksNameForParticularVminResourceGroup(resourceGroupName,vmName):
    computeClient=getComputeClient()
    detailsOfVM = computeClient.virtual_machines.get(resourceGroupName,vmName,expand='instanceView')
    allDiskOfVmList = [disk.name for disk in detailsOfVM.instance_view.disks]
    return allDiskOfVmList

def getOsDiskDictForParticularVminResourceGroup(resourceGroupName,vmName):
    computeClient=getComputeClient()
    detailsOfVM = computeClient.virtual_machines.get(resourceGroupName,vmName,expand='instanceView')
    dictOfOSDisk=dict()
    if detailsOfVM.storage_profile.image_reference:
        dictOfOSDisk["publisher"] = detailsOfVM.storage_profile.image_reference.publisher
        dictOfOSDisk["offer"] = detailsOfVM.storage_profile.image_reference.offer
        dictOfOSDisk["sku"] = detailsOfVM.storage_profile.image_reference.sku
        dictOfOSDisk["version"] = detailsOfVM.storage_profile.image_reference.version
    dictOfOSDisk["osType"] = detailsOfVM.storage_profile.os_disk.os_type
    dictOfOSDisk["name"] = detailsOfVM.storage_profile.os_disk.name
    dictOfOSDisk["createOption"] = detailsOfVM.storage_profile.os_disk.create_option
    dictOfOSDisk["caching"]= detailsOfVM.storage_profile.os_disk.caching
    return dictOfOSDisk

def getIDofDiskWithName(diskName):
    computeClient=getComputeClient()
    managed_disk = computeClient.disks.list()
    for diskObj in managed_disk:
        if diskObj.name == diskName:
            return diskObj.id

def getReplaceText(orignalText,textToReplace,textToReplacewith):
    import re

    ifTextInString = re.search(textToReplace,orignalText,flags=re.IGNORECASE)
    if not ifTextInString:
        newText = textToReplacewith +"-" + orignalText
    if ifTextInString:
        newText = re.sub(textToReplace,textToReplacewith,orignalText, flags=re.IGNORECASE)
    return newText.lower()

def diskCreate(resourceGroupNameWhereDiskWillBeCreated,diskNameToCreate,locationOfNewDisk,orignalDiskID):
    computeClient=getComputeClient()
    diskCreationPoller = computeClient.disks.begin_create_or_update(
    resourceGroupNameWhereDiskWillBeCreated,
    diskNameToCreate,
     {
        'location': locationOfNewDisk,
        'creation_data': {
            'create_option': DiskCreateOption.copy,
            'source_resource_id': orignalDiskID
        }
     }
    )
    return diskCreationPoller

def getStorageProfiletoAttachExistingOsDisk(osDiskId,vmResourceGrpName,osDiskName,osType):
    storageProfile={"osDisk":{"caching":"ReadWrite","createOption":"Attach","managedDisk":{"id":osDiskId,"resourceGroup":vmResourceGrpName},"name":osDiskName,"osType":osType,"writeAcceleratorEnabled":"false"}}
    return storageProfile

def getHardwareProfile(vmSize):
    hardwareProfile = {"vm_size": vmSize}
    return hardwareProfile

def getNetworkProfile(nicId):
    networkProfile = {"network_interfaces": [{"id": nicId}],"primary": True}
    return networkProfile

def getVmProfile(location,storageProfile,hardwareProfile,networkProfile):
    vmProfile =  {
        "location": location,"storage_profile": storageProfile,"hardware_profile":hardwareProfile,"network_profile":networkProfile}
    return vmProfile

def createVm(resGrpName,vmName,vmProfile):
    computeClient=getComputeClient()
    poller = computeClient.virtual_machines.begin_create_or_update(resGrpName,vmName,vmProfile)
    return poller

def getVm(resourceGroupName,vmName):
    computeClient=getComputeClient()
    getVmResult = computeClient.virtual_machines.get(resourceGroupName,vmName)
    return getVmResult

def appendDataDiskToStorageProfile(getVmResult,diskCreationResultObject,lunNo):
    print("________________________________________________________________________________________")
    print(getVmResult.storage_profile)
    print("________________________________________________________________________________________")
    getVmResult.storage_profile.data_disks.append({
            'lun': lunNo,
            'name': diskCreationResultObject.result().name,
            'create_option': DiskCreateOption.attach,
            'managed_disk': {
                'id': diskCreationResultObject.result().id
            }
        })
    print("________________________________________________________________________________________")
    print(getVmResult.storage_profile)
    print("________________________________________________________________________________________")
    return getVmResult


def attachDiskToVm(resourceGroupName,vmName,getVmResult):
    computeClient=getComputeClient()
    result=computeClient.virtual_machines.begin_create_or_update(resourceGroupName,vmName,getVmResult)
    return result

