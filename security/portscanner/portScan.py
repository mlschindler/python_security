# A simple TCP port scanner... Comments above or to right of specific line

import optparse # arument parser... useful for making option flags
from socket import * # the python networking API
from threading import * # threading API

screenLock = Semaphore(value=1) ## Global Semaphore value for locking threads to screen

def main():
	parser = optparse.OptionParser('usage%prog -H <target host> -p <target port>') # parser usage statement (looks to create instance with built in usage statement)
	# the below add_option utilize the <parsername>.addoption([string], dest(destination)=[string], help=[string])
	parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
	parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by a comma')
	#creates tuples options and args for use by the parser as arguments
	(options, args) = parser.parse_args()
	tgtHost = options.tgtHost
	# strips off the commas if a list of ports is given as an argument and puts into a list
	tgtPorts = str(options.tgtPort).split(',')
	if (tgtHost == None) | (tgtPorts[0] == None):
		print parser.usage
		exit(0)
	portScan(tgtHost, tgtPorts)

def ConnScan(tgtHost, tgtPort):
	try:
		connSkt = socket(AF_INET, SOCK_STREAM) #AF_NET = family, SOCK_STREAM = protocol.  Creates a socket object called connSkt
		connSkt.connect((tgtHost, tgtPort)) # connects with (IP, PORT)
		connSkt.send('ViolentPython\r\n') # send a random string to socket object, connSkt
		results = connSkt.recv(100) # recveive 100 bytes back from connSkt
		screenLock.acquire() # unlock the screen for 1 thread
		print '[+] %d/tcp open' % tgtPort
		print'[+] ' + str(results)
	except:
		screenLock.acquire()
		print '[-] %d/tcp closed' % tgtPort
	finally:
		screenLock.release() # release ownerhsip of screenlock for current thread
		connSkt.close() # close connection

def portScan(tgtHost, tgtPorts):
	try:
		tgtIP = gethostbyname(tgtHost)
	except:
		print '[-] Cannot resolve '%' : Unknown host.' % tgtHost
		return
	try:
		tgtName = gethostbyaddr(tgtIP)
		print '\n[+] Scan Results for: ' + tgtName[0]
	except:
		print '\n[+] Scan Results for: ' + tgtIP
	setdefaulttimeout(1) # set timeout to 1 second
	for tgtPort in tgtPorts: # loop through port list
		t = Thread(target=ConnScan, args=(tgtHost, int(tgtPort))) #initiate thread object Thread(target='function', args=(arguments...))
		t.start()


if __name__ == '__main__':
	main()