#!/usr/bin/python

import sys
import CloudStack
import time
from termcolor import colored
from time import sleep
from urllib2 import urlopen, HTTPError
import cloudconstants as k

cloudstack = CloudStack.Client(API_URI, YOUR_API_KEY, YOUR_API_SECRET)

vmname = sys.argv[1]

args = {
    'name':      vmname,
    'projectid': k.proj_testautomation
}

vms = cloudstack.listVirtualMachines(args)
for vm in vms:
  print "Destroying %s with id %s in project %s." % (vm['name'], vm['id'], vm['project'])
  try:
    job = cloudstack.destroyVirtualMachine({'id': vm['id']})
  except HTTPError, e:
    print e
  
  jobid = job['jobid']
  
  asyncargs = {
       'jobid': jobid
  }

  async = cloudstack.queryAsyncJobResult(asyncargs)
  ready = async['jobstatus']
  print '\nDestroying instance'
  while (ready == 0):
    print '\b.',
    sys.stdout.flush()
    time.sleep(5)
    async = cloudstack.queryAsyncJobResult(asyncargs)
    ready = async['jobstatus']

  result =  async['jobresult']
  vmdetails = result['virtualmachine']
  print '\nProject %s instance %s destroyed.' % (vmdetails['project'], vmdetails['displayname'])

print '\n'


