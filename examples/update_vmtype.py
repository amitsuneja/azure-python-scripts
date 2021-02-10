def update_vm(compute_client):
    vm = compute_client.virtual_machines.get(GROUP_NAME, VM_NAME)
    vm.hardware_profile.vm_size = 'Standard_DS3'
    update_result = compute_client.virtual_machines.create_or_update(
        GROUP_NAME, 
        VM_NAME, 
        vm
    )

return update_result.result()
