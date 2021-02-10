#!/usr/bin/python3

import argparse
from myLibForAzure.LoginToAccount import getResourceClient# Show the groups in formatted output

# set column_width to format outputs
column_width = 35

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--location", action='store_true', help="Optional : -l or --location")
ap.add_argument("-with_ids", "--with_ids", action='store_true', help="Optional : -with_ids or --with_ids")
ap.add_argument("-only_ids", "--only_ids", action='store_true', help="Optional : -only_ids or --only_ids")
cli_argument_dict = vars(ap.parse_args())

# get resourceClient object
resourceClient = getResourceClient()

# Retrieve the list of resource groups
group_list = resourceClient.resource_groups.list()

if (cli_argument_dict['location']):

    # print colum headings and dotted line
    print("Resource Group".ljust(column_width) + "Location")
    print("-" * (column_width * 2))
    # Iterate over group_list
    for group in list(group_list):
        print(f"{group.name:<{column_width}}{group.location}")

elif (cli_argument_dict['with_ids']):
        # print colum headings and dotted line
    print("Resource Group".ljust(column_width) + "ID")
    print("-" * (column_width * 2))
    # Iterate over group_list
    for group in list(group_list):
        print(f"{group.name:<{column_width}}{group.id}")
elif (cli_argument_dict['only_ids']):
    for group in list(group_list):
        print(group.id)
else:
    for group in list(group_list):
        print(group.name)

