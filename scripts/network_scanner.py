import nmap
import subprocess
from subprocess import Popen, PIPE, CalledProcessError

# ! IMPORTANT !
# Dont scan for ports on every IP, as it will probably crash the WiFi Network.

# try to find the subnet which you are in
def iwconfig():
    cmd = 'ifconfig'
    returned_output = subprocess.check_output(cmd)

    out = returned_output.decode('utf-8')
    splitted = out.split()
    
    try:
        for i in splitted:
            if '192.168' in i:
                index = splitted.index(i)
                if 'inet' in splitted[index-1]:
                    ip_split = i.split('.')
                    subnet = ip_split[2]
                    return str(subnet)
    except:
        print('Subnet cant be figured out. Type in subnet manually (192.168.x.0-255):\n')
        subnet_input = raw_input()
        return str(subnet_input)

def main():
    nm = nmap.PortScanner()
    nm.scan('192.168.' + iwconfig() + '.1/24')

    for count, i in enumerate(nm.all_hosts()):
        print('[' + str(count) + '] ' + str(i) + ' (' + nm[i].hostname() + ')\nStatus: ' + nm[i].state())

if __name__ == '__main__': 
    main()
