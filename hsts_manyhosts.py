#!/usr/bin/python

######################
#
# A great BIG THANK YOU to Greg Hetrick for adding the error handling
#
#	requests.exceptions.RequestException
#	requests.exceptions.ConnectionError:
#	urllib3.exceptions.MaxRetryError
#	urllib3.exceptions.SSLError
#
######################

import sys
import requests
import urllib3
import certifi
from urllib3 import PoolManager, Timeout
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ConnectionError

# Read the input file 500.txt
file = open('500.txt', 'r')
domains = file.readlines()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

i=0
urlstart="https://"

using = 0
notusing = 0
broke = 0
http = urllib3.PoolManager(
      cert_reqs='CERT_REQUIRED', # Force certificate check.
      ca_certs=certifi.where(),  # Path to the Certifi bundle.
 )


while i<len(domains):
 domain = domains[i].rstrip('\n')
 url=urlstart + domains[i].rstrip('\r\n')
 http = PoolManager(timeout=Timeout(read=2.0))
 try:
  check = http.request('GET', url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'},timeout=2)
  if 'strict-transport-security' in check.headers:
   print str(i) + ': ' + url + ': is using HSTS!!!'
   i+=1
   using+=1
  else:
   print str(i) + ': ' + url + ': is NOT using HSTS'
   notusing+=1
   i+=1
 # check = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'},timeout=2)
 except requests.exceptions.RequestException as e:
  print e
  i+=1
  broke+=1
 except requests.exceptions.ConnectionError as e:
  print e
  i+=1
  broke+=1
 except urllib3.exceptions.MaxRetryError as e:
  print e
  i+=1
  broke+=1
 except urllib3.exceptions.SSLError as e:
  print e
  i+=1
  broke+=1

print '=================================================='
print str(using) + ' are using HSTS, ' + ' while ' + str(notusing) + ' are not using HSTS'
print 'Found ' + str(broke) + ' are somehow fucked up'
total = using + notusing + broke
print str(total) + ' sites tested'
