#!/usr/bin/python3

from myLibForAzure.LoginToAccount import getComputeClient

computeClient=getComputeClient()
managed_disk = computeClient.disks.list()
for item in managed_disk:
   print(item)
   print("______________________________")

#detailsOfVM = computeClient.virtual_machines.get("AKS-CLUSTER-RG", "DOCKER", expand='instanceView')
#dictOfOSDisk=dict()
#if detailsOfVM.storage_profile.image_reference:
#        dictOfOSDisk["publisher"] = detailsOfVM.storage_profile.image_reference.publisher
#        dictOfOSDisk["offer"] = detailsOfVM.storage_profile.image_reference.offer
#        dictOfOSDisk["sku"] = detailsOfVM.storage_profile.image_reference.sku
#        dictOfOSDisk["version"] = detailsOfVM.storage_profile.image_reference.version
#dictOfOSDisk["osType"] = detailsOfVM.storage_profile.os_disk.os_type
#dictOfOSDisk["name"] = detailsOfVM.storage_profile.os_disk.name
#dictOfOSDisk["createOption"] = detailsOfVM.storage_profile.os_disk.create_option)
#dictOfOSDisk["caching"]= detailsOfVM.storage_profile.os_disk.caching
#print(dictOfOSDisk)

#allDiskOfVmList = [disk.name for disk in detailsOfVM.instance_view.disks]
#for item in allDiskOfVmList:
#    print(item)

########################################
# Create Disk
from azure.mgmt.compute.models import DiskCreateOption

# If you don't know the id, do a 'get' like this to obtain it
managed_disk = computeClient.disks.get('RG-KHJ-TRN-SAP', 'KHJAZRUSETTS02_OsDisk_1_ec73e060749d4592bc3b42378486841c')

poller = computeClient.disks.begin_create_or_update(
    'AKS-CLUSTER-RG',
    'disk_name_check_details_osType',
    {
        'location': 'eastus',
        'creation_data': {
            'create_option': DiskCreateOption.copy,
            'source_resource_id': managed_disk.id
        }
    }
)

disk_resource = poller.result()
print(disk_resource)
