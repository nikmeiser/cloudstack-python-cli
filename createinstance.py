#!/usr/bin/python

import sys
import CloudStack
import time
from termcolor import colored
from time import sleep
from urllib2 import urlopen, HTTPError
import cloudconstants as k
import nikkeys as nik

cloudstack = CloudStack.Client(k.api, nik.apikey, nik.secret)
projectid = k.proj_testautomation


if len(sys.argv) < 2:
   sys.exit('You must provide a valid hostname. Usage: ./createinstance.py hostname')
else:
  vmname = sys.argv[1]
  vms = cloudstack.listVirtualMachines({'name': vmname, 'projectid': projectid})

  if len(vms) > 0:
    sys.exit('\nThere is already a VM with this name in this project. Please pick another name.\n')
  else:
    args = {
        'serviceofferingid': k.svc_medium_hourly,
        'templateid':        k.tmpl_win2k8r2_std,
        'zoneid':            k.zone_amers1a,
        'networkids':        k.net_amers1a,
        'projectid':         projectid,
        'name':              vmname
    }

    try:
      job = cloudstack.deployVirtualMachine(args)
      jobid = job['jobid']

      asyncargs = {
          'jobid': jobid
      }
      
      async = cloudstack.queryAsyncJobResult(asyncargs)
      ready = async['jobstatus']
      print '\nBuilding instance'
      while (ready == 0):
        print '\b.',
        sys.stdout.flush()
        time.sleep(5)
        async = cloudstack.queryAsyncJobResult(asyncargs)
        ready = async['jobstatus']
        
      result =  async['jobresult']
      vmdetails = result['virtualmachine']  
      print "\nInstance created. Instance name is %s. Password = %s" % (vmdetails['name'], vmdetails['password'])
    except HTTPError, e:
      print e
      # print e.__dict__

print "\n"


