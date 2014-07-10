#!/usr/bin/python

import sys
import CloudStack
import time
from termcolor import colored
from urllib2 import urlopen, HTTPError
import cloudconstants as k
import nikkeys as nik

# Initialize the API
cloudstack = CloudStack.Client(k.api, nik.apikey, nik.secret)

# Fetch all the private cloud projects associated with the API key
projects = cloudstack.listProjects()

# This is so we can format the output to screen better - tokenized field names
header = ['IP Address', 'State', 'Project Name', 'Template', 'Instance', 'Hostname']

# Print the header for the output
print "\nVirtual Machines"
print "============================\n"
print colored(header[0].ljust(15) + header[1].center(11) + header[2].center(23)+ header[3].center(29)+ header[4].center(8)+ header[5].center(37) + '\n', attrs=['bold', 'underline'])

# Iterate through the projects to retrieve all the VMs associated
for project in projects:
  args = {'projectid' : project['id']}
  vms = cloudstack.listVirtualMachines(args)
  
  # Iterate through each VM in each project and format and print the details to screen
  for vm in vms:
    for nic in vm['nic']:
      vmip=nic['ipaddress']
      print "%s" % (vmip).ljust(15),
      sys.stdout.flush()

      # Color-code the VM status - red if down and green, if up
      if vm['state'] == 'Stopped':
        print "%s" % colored(vm['state'][:7].center(9), 'yellow', 'on_red'),
        sys.stdout.flush()
      else:
        print "%s" % colored(vm['state'][:7].center(9), 'blue', 'on_green'),
        sys.stdout.flush()

      # Parse through the service instance and get the basic details
      svctype = vm['serviceofferingname'].lower().split()

      if 'hourly' in svctype:
        t = 'HR'
      elif 'daily' in svctype:
        t = 'DY'
      else:
        t = 'UN'

      if 'micro' in svctype:
        sz = 'MIC'
      elif 'small' in svctype:
        sz = 'SML'
      elif 'medium' in svctype:
        sz = 'MED'
      elif 'large' in svctype:
        sz = 'LRG'
      else:
        sz = 'UNK'

      svcstr = t + '-' + sz
      print "%s %s %s %s\n" % (project['name'][:22].ljust(22), vm['templatename'][:28].ljust(28), svcstr.ljust(8), vm['name'])


