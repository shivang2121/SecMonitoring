# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 02:02:01 2023

@author: shiva
"""

import requests
import pandas as pd
API_ENDPOINT = "https://mb-api.abuse.ch/api/v1/"
API_KEY = "-api.abuse.ch/api/v1/"
headers = {'API-KEY': '12ecb62a793113ef0478bc9f3180317c'}  # Replace with your actual API key
# Read the contents of the file
with open('quakbot_hashes.txt', 'r') as file:
    data = file.read()

# Split the data into individual lines (assuming each line contains one hash)
hash_list = data.strip().split('\n')

# Print the resulting list


hashes = hash_list
first_seen_list = []
file_type_list = []
for hash_value in hashes:
    data = {
        "query": "get_info",
        "hash": hash_value,
    }
    headers = {"API-KEY": API_KEY}

    response = requests.post(API_ENDPOINT, data=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        # Process the result as needed
        for item in result['data']:
            first_seen_list.append(item['first_seen'])
            file_type_list.append(item['file_type'])
        print(result)
    else:
        print(f"Request failed with status code {response.status_code}.")

df = pd.DataFrame({'First Seen': first_seen_list, 'File Type': file_type_list})

# Save to Excel
df.to_excel('output.xlsx', index=False)

