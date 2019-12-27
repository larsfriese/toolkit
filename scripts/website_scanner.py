import sys
import os

# ! IMPORTANT !
# Nikto Package needs to be installed on system for this to work.

def main(input_server):
    cmd = 'nikto -h ' + input_server + ' -p 80'
    os.system(cmd) # no subprocess, as we want to see live output

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('ARGUMENT ERROR:\nUsage: sudo python3 target_server.py -t\n-t targets IP Adress')
        exit(1)
        
    input_server = sys.argv[1] 
    main(input_server)