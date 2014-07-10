#!/usr/bin/python

import sys
import CloudStack
import time
from termcolor import colored
from urllib2 import urlopen, HTTPError
import cloudconstants as k

cloudstack = CloudStack.Client(API_URI, YOUR_API_KEY, YOUR_API_SECRET)

sos = cloudstack.listServiceOfferings()

print "Service Offerings"
print "============================"
print colored("name  \t\t\t\tid    \t\t\t\t\tcpucount \tmemory \tcpuspeed\n", attrs=['bold', 'underline'])
for so in sos:
        print "%s\t%s\t%s\t\t%s\t%s\n" % (so['name'], so['id'], so['cpunumber'], so['memory'], so['cpuspeed'])



