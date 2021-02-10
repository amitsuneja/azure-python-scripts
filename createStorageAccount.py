#!/usr/bin/python

import argparse
from myLibForAzure.LoginToAccount import getStorageClient
from myLibForAzure.LoginToAccount import getDictOfStorageAccountNameKeyAndIdValue










# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-r", "--resource_group",required=True,help="Mandate : -r or --resource_group")
#ap.add_argument("-n", "--storage_account_name",required=True,help="Mandate : -n or --storage_account_name")
#cli_argument_dict = vars(ap.parse_args())


storageClient = getStorageClient()
print(type(storageClient.storage_accounts.list_account_sas))
