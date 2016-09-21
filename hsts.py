#!/usr/bin/python
import sys
import requests
import urllib3
import certifi

#if you are having issues then set DEBUG=True
DEBUG=False

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
response=check.headers
if 'strict-transport-security' in response:
    print "[+] " +site + ': is using HSTS!!!'
    if 'preload' in str(response):
        print "  [+] Preload enabled"
    else:
    	print "  [Warning!] Preload is not configured"    
    if 'includeSubDomains' in str(response):
       print "  [+] includeSubdomains is present"
    else:
       print "  [Warning!] includeSubDomains is not configured"
    if 'max-age=31536000' in str(response):
	print "  [+] max-age is set to two years - well done"
    else:
	print "  [Warning!] max-age should really be set to two years (31536000)"
    if DEBUG:
        print str(response)
else:
    print site + ': is NOT using HSTS'
    if DEBUG:
        print str(response)
