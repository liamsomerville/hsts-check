#!/usr/bin/python

import sys
import requests
import urllib3
import certifi

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)

site=str(sys.argv[1]).lower()
urlstart="https://"
url=''

#check if url in argument begins https if not, inject it
if site.startswith(urlstart):
 url=site
else:
 url=urlstart + site

#Peform the HSTS check and display the result
check = http.request('GET', url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'})
if 'strict-transport-security' in check.headers:
 print site + ': is using HSTS!!!'
else:
 print site + ': is NOT using HSTS'
