#!/usr/bin/python3

from myLibForAzure.LoginToAccount import getListOfLocations
from myLibForAzure.SelectAccount import subscriptionid


locations = getListOfLocations()
for location in list(locations):
    print(location.name)
