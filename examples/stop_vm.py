def stop_vm(compute_client):
    compute_client.virtual_machines.power_off(GROUP_NAME, VM_NAME)
def deallocate_vm(compute_client):
    compute_client.virtual_machines.deallocate(GROUP_NAME, VM_NAME)
