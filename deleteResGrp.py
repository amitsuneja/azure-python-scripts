#!/usr/bin/python3

import argparse
from myLibForAzure.LoginToAccount import getResourceClient


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-r", "--resource_group",required=True,help="Mandate : -r or --resource_group")
cli_argument_dict = vars(ap.parse_args())

print("Warning : this is dangerous script. It deletes ResGrp and its all resources witout prompting")
print("Remove the '#' mark from last 3 lines to activate script")

# get resourceClient object
#resourceClient = getResourceClient()
#poller = resourceClient.resource_groups.begin_delete(cli_argument_dict['resource_group'])
#result = poller.result()
