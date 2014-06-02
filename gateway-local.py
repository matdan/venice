#!/usr/bin/env python2.7

import ddpclient
import time
import json
import urllib2
from random import randint

def main():
    
    app = ddpclient.App("127.0.0.1:3000", False)
    time.sleep(1);
     
    while True:

	timestamp=time.time()
	balls=[]
	lenses=[]
	
	# generate lenses
	for ball in range(1,7):
		odd=randint(0,1)
		if odd==1:
			lenses.append([0,0])
	
	# generate balls
	for ball in range(1,7):
		odd=randint(0,1)
		if odd == 1:
			balls.append({'id':ball, 'position':{'x':randint(1,6000),'y':randint(1,6000)}, 'lenses':lenses})
	
	
	# object
	data= [{
		'timestamp': timestamp, 
		'balls': balls
	}]
	
	#print json.dumps(data)
	print "."
	
	# call
	app.do_call("gateway [\"khu8dqMtLeuUxkZUu9sPHtqVxTCxyr\","+json.dumps(data)+"]")

	req = urllib2.Request("http://localhost:3000/receive/khu8dqMtLeuUxkZUu9sPHtqVxTCxyr/30.20")
	res = urllib2.urlopen(req)
	# wait 2 secs
	time.sleep(1)
    
if __name__ == '__main__':
    main()