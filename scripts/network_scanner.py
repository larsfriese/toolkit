import nmap

# ! IMPORTANT !
# Dont scan for ports on every IP, as it will probably crash the WiFi Network.

def main():
    nm = nmap.PortScanner()
    nm.scan('192.168.2.1/24')

    for count, i in enumerate(nm.all_hosts()):
        print('[' + str(count) + '] ' + str(i) + ' (' + nm[i].hostname() + ')\nStatus: ' + nm[i].state())

if __name__ == '__main__': 
    main()
