# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 01:56:57 2023

@author: shiva
"""

import requests

API_ENDPOINT = "https://mb-api.abuse.ch/api/v1/"
headers = {'API-KEY': '12ecb62a793113ef0478bc9f3180317c'}  # Replace 'YOUR_API_KEY' with your actual API key

data = {
    'query': 'get_taginfo',
    'tag': 'Quakbot',
    'limit': 1000
}

response = requests.post(API_ENDPOINT, data=data, headers=headers)

if response.status_code == 200:
    results = response.json()
    if 'data' in results:
        sha256_hashes = [entry.get('sha256_hash') for entry in results['data']]
        with open('quakbot_hashes.txt', 'w') as file:
            for hash_value in sha256_hashes:
                file.write(hash_value + '\n')
        print("SHA-256 hashes saved to 'quakbot_hashes.txt'.")
    else:
        print("No data found in the response.")
else:
    print(f"Request failed with status code {response.status_code}.")
