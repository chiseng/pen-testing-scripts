#!/usr/bin/env python


#Run file as following: scanning_script.py <target host IP> y (if you want dirs to be created to store stuff)
import subprocess
import nmap
import sys
import glob
import os

try:
    target=sys.argv[1]
except IndexError:
    print('Example: ./scanning_script.py <rhost> <y to create custom folders>')
    sys.exit(-1) #exit when error

#use pipelining to ensure the process run correctly. 
def processor(process): #huge creds to phi10s 
    output=""
    while process.poll() is None:
    	readline=process.stdout.readline()
    	output+=readline
    	sys.stdout.write(readline) #write the output from process
    readline=process.stdout.read()
    output+=readline
    sys.stdout.write(readline)
    sys.stdout.flush()
    return output

try:
    wd=os.getcwd() #get current working dir to change back
    if(sys.argv[2]=='y'):
        try:
            subprocess.call(['mkdir',sys.argv[1]])
	    os.chdir(sys.argv[1])	
            subprocess.call(['mkdir','scripts'])
            subprocess.call(['mkdir','exploits'])
            subprocess.call(['mkdir','scans'])
	    os.chdir(wd)
	    print('')
        except OSError, e:
            print('Directory not created')
            print('')
except IndexError:
    pass
print('===========================================') #i was too lazy to make one for nmap :<
print('Nmap service running')
target=sys.argv[1]
nm=nmap.PortScanner()
nm.scan(hosts=target, arguments='-sV') #print product, state, version, name
print("Port\tState\tVersion\tType\t\tService")
ports=nm[target]['tcp']
portlist=[]
for port in ports:
    portlist.append(port)
    print("\n%s\t%s\t%s\t%s\t\t%s" % (port, ports[port]['state'], ports[port]['version'], ports[port]['name'], ports[port]['product']))
print('===========================================')
print('')
if '80' in portlist:
    print('Get a drink or something')
    print('\n  ___'
    	+'\n /         |'
	+'\n|   __  __ |__      ___|__ __  ___'
	+'\n|  |_ ||  ||  ||  ||__ |  / _\|   '
	+'\n \____||__||__||__| __|\__\___|   ')
    wordlist = "/usr/share/seclists/Discovery/Web-Content/common.txt"
    url="http://"+str(target)
    errorcodes='200,204,301,302,307,403,500'
    processor(subprocess.Popen(['gobuster','-u',url,'-w',wordlist, '-s',errorcodes, '-e'], stdout=subprocess.PIPE))
    print('')
    print("Get another drink, this shit's gonna hurt")
    print('\n _   _         _______ _____'
	+'\n| \ | | [] |  /__   __|     |'
	+'\n|  \| ||  ||_/   | |  | _|_ |'
	+'\n|  .  ||  || \   | |  |  |  |'
	+'\n|_| \_||__||  \  | |  |_____|')
    processor(subprocess.Popen(['nikto','-h',url],stdout=subprocess.PIPE))

