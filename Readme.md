1. download repo and then go to config directory . Rename the file dummy_azureAccountDetails.ini to azureAccountDetails.ini
2. update your account and subscription details in azureAccountDetails.ini.
3. with in config file run ./generateCredentials.py , it will ask you to select specific subscription you want to work on and accordingly it will generate SelectAccount.py in your myLibForAzure directory .
4. You can use scripts now.
5. To switch to other subscription run generateCredentials.py again to over write myLibForAzure/SelectAccount.py file. 


Ref - https://docs.microsoft.com/en-us/python/api/?view=azure-python
sample codes - https://docs.microsoft.com/en-us/samples/browse/
https://docs.microsoft.com/en-gb/azure/developer/python/azure-sdk-example-virtual-machines?tabs=cmd
https://docs.microsoft.com/en-gb/azure/developer/python/azure-sdk-samples-managed-disks?view=azure-python
https://docs.microsoft.com/en-gb/azure/developer/python/azure-sdk-authenticate?tabs=cmd
https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-samples-managed-disks
