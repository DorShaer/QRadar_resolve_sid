import json
import ssl
import sys
import urllib.request
import urllib.parse
import requests
import subprocess
import os
from subprocess import *


def main_func():

## When creating a new custom action the order of the element is:
    
#host (the console url)
#KEY (SEC Key / token)
#domainUserName
#domain Password
#refset (the reference set name to add the user to)
    
host = sys.argv[0]
KEY = sys.argv[1]
domainUserName = sys.argv[2]
domainPassword = sys.argv[3]
refset = sys.argv[4]
    
certificate_file = ""
headers = {'Version': '14.0', 'Accept': 'application/json',
            'SEC': KEY, 'Range': 'items=0-0'}
#print(headers)
# You can also use a security token for authentication.
# The format for passing a security token is "'SEC': token" instead of
# "'Authorization': 'Basic encoded_credentials'".

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

# SSL version 2 and SSL version 3 are insecure. The insecure versions are
# disabled.
try:
    context.options = ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
except ValueError as e:
# Disabling SSLv2 and SSLv3 is not supported on versions of OpenSSL
# prior to 0.9.8m.
    print('WARNING: Unable to disable SSLv2 and SSLv3, caused by '
            'exception: "' + str(e) + '"')
    while True:
        response = input(
            "Would you like to continue anyway (yes/no)? ").strip().lower()
        if response == "no":
            sys.exit(1)
        elif response == "yes":
            break
        else:
            print(response + " is not a valid response.")
# Require certificate verification.
context.verify_mode = ssl.CERT_REQUIRED
if sys.version_info >= (3, 4):
    context.check_hostname = True
check_hostname = True

if certificate_file != "":
# An optional certificate file was provided by the user.

# The default QRadar certificate does not have a valid hostname so we
# must disable hostname checking.
    if sys.version_info >= (3, 4):
        context.check_hostname = False
    check_hostname = False
# Load the certificate file that was specified by the user.
    context.load_verify_locations(cafile=certificate_file)
else:
# The optional certificate file was not provided. Load the default
# certificates.
    if sys.version_info >= (3, 4):
        context.load_default_certs(ssl.Purpose.CLIENT_AUTH)
    else:
        context.set_default_verify_paths()

# Create a new HTTPSHandler and install it using the new HTTPSContext.
urllib.request.install_opener(urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=context,
                                check_hostname=check_hostname)))

# REST API requests are made by sending an HTTPS request to specific URLs.

console_code = 'https://' + host + '/api/siem/offenses?fields=offense_source'
request = urllib.request.Request(console_code, headers=headers)
response = urllib.request.urlopen(request)
parsed_response = json.loads(response.read().decode('utf-8'))
result = parsed_response[0]
#print(result)
sid = result.get("offense_source")
ldapQuery = subprocess.Popen(
    ["ldapsearch", "-x", "-b", "dc=INPUT, dc=DC-HERE, dc=com", "-H", "ldap://INPUT.DC-HERE.com", "-D", domainUserName,
     "-w", domainPassword, "(objectsid={0})".format(sid), "sAMAccountName"], stdout=subprocess.PIPE).communicate()[
    0]
resolver = ldapQuery.decode()
#print the output, put it into a list and split every line
findUser = resolver.splitlines()
for line in findUser:
    if line.startswith('sAMAccountName:'):
        x = line[16:]
        print(x)

## Add the username resolved to the reference set
    
add_user = 'https://' + host + '/api/reference_data/sets/' + refset +'?'
add_head = {
    'SEC': KEY
    
}
    
params = {
    'name': refset,
    'value': x
    
}
## Send the post request, use the  username you found and add it to the reference set:
url = add_user + urllib.parse.urlencode(params)
new_req = requests.post(url, headers=add_head, verify=False).json()
print(json.dumps(new_req, indent=2))
# Here we can see the headers of the response
# To see response headers just uncomment the 3 lines below
#print(response.headers)
#for i in parsed_response:
#print(parsed_response)
if __name__ == "__main__":
main_func()
