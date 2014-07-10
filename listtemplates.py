#!/usr/bin/python

import sys
import CloudStack
import time
from termcolor import colored
from urllib2 import urlopen, HTTPError
import cloudconstants as k
import nikkeys as nik

cloudstack = CloudStack.Client(k.api, nik.apikey, nik.secret)

if len(sys.argv) < 2:
  tmpltype = 'community'
else:
  tmpltype = sys.argv[1]

if tmpltype.lower() not in ['community', 'featured', 'self', 'executable']:
  sys.exit("Invalid option. Valid options are 'community', 'featured', 'self', 'executable'")
  
# args = {'templatefilter': tmpltype.lower(), 'projectid': '-1'}
args = {'templatefilter': tmpltype.lower(), 'listall': '-1', 'projectid': '-1'}
tmpls = cloudstack.listTemplates(args)

print "\nAvailable Templates for Template Type:",
sys.stdout.flush()
print '%s' % colored(tmpltype.upper(), attrs=['bold'])
print "================================================="

header = ['project', 'id', 'zone', 'name']
print colored(header[0].ljust(35) + header[1].center(42) + header[2].center(13)+ header[3].center(45) + '\n', attrs=['bold', 'underline'])

for tmpl in tmpls:
    if tmpl.get('project'):
      pname = tmpl['project']
    else:
      pname = '--|___________ Shared ____________|'

    print "%s %s %s %s\n" % (pname[:35].ljust(37, '-'), tmpl['id'][:42].ljust(42), tmpl['zonename'][:8].ljust(8),  tmpl['ostypename'])

