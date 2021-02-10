def start_vm(compute_client):
    compute_client.virtual_machines.start(GROUP_NAME, VM_NAME)
