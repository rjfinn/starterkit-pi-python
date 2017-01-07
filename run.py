#!/usr/bin/python
import os
import requests
import time

LOOPS = 0  # number of times to loop, set to 0 for infinte
DELAY = 10 # seconds between loops

URL = "https://run-east.att.io/aace54c7ff90c/e858c181b5d5/6c34b27c9b8180e/in/flow/command"

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

# Return CPU temperature as a character string
def getCPUtemp():
	res = os.popen('vcgencmd measure_temp').readline()
	return(res.replace("temp=","").replace("'C\n",""))

myserial = getserial()

# check if this Pi is registered
payload = {'cmd': 'registered', 'serial': myserial}
#r = requests.post(URL, data=payload)
r = requests.get(URL, params=payload)
print(r.text)
obj = r.json()
if(obj['statusCode'] == 404):
	time.sleep(2);
elif(obj['statusCode'] == 403):
	exit()

count = 0
while count <= LOOPS or LOOPS == 0:
	count += 1
	print("sensor reading #%d" % count)
	# send sensor reading
	temp = getCPUtemp()
	payload = {'cmd': 'sensor', 'temp': temp}
	r = requests.get(URL, params=payload)
	print(r.text)
	time.sleep(DELAY)

print("Exiting")
#print(myserial)
#print(temp+"C")
