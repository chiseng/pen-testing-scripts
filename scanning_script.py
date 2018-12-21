#!/usr/bin/env python
import subprocess
import nmap
import sys

def processor(process): #huge creds to phi10s 
    output=""
    while process.poll() is None:
    	readline=process.stdout.readline()
    	output+=readline
    	sys.stdout.write(readline)
    readline=process.stdout.read()
    output+=readline
    sys.stdout.write(readline)
    sys.stdout.flush()
    return output

try:
    subprocess.call(['mkdir',sys.argv[1]])
    subprocess.call(['cd',sys.argv[1]])
    subprocess.call(['mkdir','scripts'])
    subprocess.call(['mkdir','exploits'])
    subprocess.call(['mkdir','scans'])
except Exception, e:
    print('Directory not created')
print('')
print('===========================================') #i was too lazy to make one for nmap :<
print('Nmap service running')
nm=nmap.PortScanner()
nm.scan(sys.argv[1], sys.argv[2]) #scan ip, ports
host=nm.all_hosts()[0]
port80=[]
for protocol in nm[host].all_protocols():
    print('Protocol : %s' % protocol)
    lport = nm[host][protocol].keys()
    lport.sort()
    for port in lport:
        port80.append(port)
        if(port==21):
            print('port : %s\tstate : %s (FTP Service)' % (port, nm[host][protocol][port]['state']))
        elif(port==80):
            print('port : %s\tstate : %s (HTTP Service)' % (port, nm[host][protocol][port]['state']))
        else:
            print ('port : %s\tstate : %s' % (port, nm[host][protocol][port]['state']))
print('===========================================')
print('')
print(host)
if 80 in port80:
    print('Get a drink or something')
    print('\n  ___'
    	+'\n /         |'
	+'\n|   __  __ |__      ___|__ __  ___'
	+'\n|  |_ ||  ||  ||  ||__ |  / _\|   '
	+'\n \____||__||__||__| __|\__\___|   ')
    wordlist = "/usr/share/seclists/Discovery/Web-Content/common.txt"
    url="http://"+str(host)
    processor(subprocess.Popen(['gobuster','-u',url,'-w',wordlist],stdout=subprocess.PIPE))
    print('')
    print('Get another drink')
    print('\n _   _         _______ _____'
	+'\n| \ | | [] |  /__   __|     |'
	+'\n|  \| ||  ||_/   | |  | _|_ |'
	+'\n|  .  ||  || \   | |  |  |  |'
	+'\n|_| \_||__||  \  | |  |_____|')
    processor(subprocess.Popen(['nikto','-h',url], stdout=subprocess.PIPE))

