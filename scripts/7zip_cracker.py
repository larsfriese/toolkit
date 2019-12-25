import sys
import zipfile
import itertools
import string
from threading import Thread

def main():
    if len(sys.argv) <= 2:
        print('ARGUMENT ERROR:\nUsage: sudo python3 7zip_cracker.py -f -w\n-f path to target 7zip archive\n-w path to wordlist')
        exit(1)
    
    zipFile = zipfile.ZipFile(sys.argv[1])
    passwords = open(sys.argv[2])
    for line in passwords.readlines():
        pwd = line.strip('\n')
        t = Thread(target=crack, args=(zipFile, pwd))
        t.start()

def crack(zip, pwd):
    try:
        zip.extractall(pwd=str.encode(pwd))
        print('Success: Password is ' + pwd)
    except:
        pass

if __name__ == '__main__': 
    main()