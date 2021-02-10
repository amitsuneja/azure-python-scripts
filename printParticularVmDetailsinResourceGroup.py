#!/usr/bin/python3
import argparse
from myLibForAzure.LoginToAccount import printParticularVmDetailsinResourceGroup

ap = argparse.ArgumentParser()
ap.add_argument("-rg", "--resource_group",required=True,help="Mandate : -rg or --resource_group")
ap.add_argument("-vm", "--virtual_machine_name",required=True,help="Mandate : -vm or --virtual_machine_name")

cli_argument_dict = vars(ap.parse_args())

ResGrp=cli_argument_dict['resource_group'].lower()
VmName=cli_argument_dict['virtual_machine_name'].upper()

printParticularVmDetailsinResourceGroup(ResGrp,VmName)
