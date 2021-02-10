def add_datadisk(compute_client):
    disk_creation = compute_client.disks.create_or_update(
        GROUP_NAME,
        'myDataDisk1',
        {
            'location': LOCATION,
            'disk_size_gb': 1,
            'creation_data': {
                'create_option': DiskCreateOption.empty
            }
        }
    )
    data_disk = disk_creation.result()
    vm = compute_client.virtual_machines.get(GROUP_NAME, VM_NAME)
    add_result = vm.storage_profile.data_disks.append({
        'lun': 1,
        'name': 'myDataDisk1',
        'create_option': DiskCreateOption.attach,
        'managed_disk': {
            'id': data_disk.id
        }
    })
    add_result = compute_client.virtual_machines.create_or_update(
        GROUP_NAME,
        VM_NAME,
        vm)

    return add_result.result()
