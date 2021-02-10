#!/usr/bin/python3

import argparse
from myLibForAzure.LoginToAccount import getResourceClient

def createResGrp(cli_argument_dict):
    if ('location' not  in cli_argument_dict.keys() or 'resource_group' not in cli_argument_dict.keys()):
        print("Required arguments missing: use createResGrp.py -h")
        exit()
    else:
        locDict=dict()
        locDict['location']=cli_argument_dict['location']
        # get resourceClient object
        resourceClient = getResourceClient()
        rg_result = resourceClient.resource_groups.create_or_update(cli_argument_dict['resource_group'],locDict)
        print(f"Provisioned resource group {rg_result.name} in the {rg_result.location} region")


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--location",required=True,help="Mandate : -l or --location")
ap.add_argument("-r", "--resource_group",required=True,help="Mandate : -r or --resource_group")
cli_argument_dict = vars(ap.parse_args())
createResGrp(cli_argument_dict)
