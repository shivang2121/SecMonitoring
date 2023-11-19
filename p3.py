#!/usr/bin/env python3
import requests
import sys
import argparse
import json
import pyzipper

__author__ = "Corsin Camichel"
__copyright__ = "Copyright 2020, Corsin Camichel"
__license__ = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__ = "1.0"
__email__ = "cocaman@gmail.com"

def check_sha256(s):
    if s == "":
        return
    if len(s) != 64:
        raise argparse.ArgumentTypeError("Please use sha256 value instead of '" + s + "'")
    return str(s)

parser = argparse.ArgumentParser(description='Download a malware sample from Malware Bazaar by abuse.ch')
parser.add_argument('-s', '--hash', help='File hash (sha256) to download', metavar="HASH", required=True, type=check_sha256)
parser.add_argument('-u', '--unzip', help='Unzip the downloaded file', required=False, default=False, action='store_true')
parser.add_argument('-i', '--info', help='Get information on a hash (do not download file)', required=False, default=False, action='store_true')

args = parser.parse_args()

if(args.unzip == True and args.info == True):
    print("Sorry, please select unzip or information display.")
    sys.exit(1)

ZIP_PASSWORD = b'infected'
headers = { 'API-KEY': '12ecb62a793113ef0478bc9f3180317c' }

if(args.info == False):
    data = {
        'query': 'get_file',
        'sha256_hash': args.hash,
    }

    response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=15, headers=headers, allow_redirects=True)

    if 'file_not_found' in response.text:
        print("Error: file not found")
        sys.exit()
    else:
        open(args.hash+'.zip', 'wb').write(response.content)

        if(args.unzip == True):  
            with pyzipper.AESZipFile(args.hash+".zip") as zf:
                zf.pwd = ZIP_PASSWORD
                my_secrets = zf.extractall(".")  
                print("Sample \""+args.hash+"\" downloaded and unpacked.")
        else:
            print("Sample \""+args.hash+"\" downloaded.")  
else:
    data = {
        'query': 'get_info',
        'hash': args.hash,
    }
    print(data)
    response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=15, headers=headers)
    print(response.content.decode("utf-8", "ignore"))
    