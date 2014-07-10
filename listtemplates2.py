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
  
args = {'templatefilter': tmpltype.lower()}
tmpls = cloudstack.listTemplates(args)

print "\nAvailable Templates for Template Type:",
sys.stdout.flush()
print '%s' % colored(tmpltype.upper(), attrs=['bold'])
print "================================================="
print colored("id  \t\t\t\t\tname\n", attrs=['bold', 'underline'])
for tmpl in tmpls:
    print "%s\t%s\n" % ( tmpl['id'], tmpl['ostypename'])


