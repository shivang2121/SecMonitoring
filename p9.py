# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 02:29:14 2023

@author: shiva
"""



import requests
import pandas as pd 
API_ENDPOINT = "https://mb-api.abuse.ch/api/v1/"
API_KEY = "-api.abuse.ch/api/v1/"
headers = {'API-KEY': '12ecb62a793113ef0478bc9f3180317c'}  # Replace with your actual API key



with open('quakbot_hashes.txt', 'r') as file:
    data = file.read()

# Split the data into individual lines (assuming each line contains one hash)
hash_list = data.strip().split('\n')
hashes=hash_list
#hashes = ["9b6e3977e1e40cba19d5be5bbc194fd72131e019febae55ba82e91ea3ca28d19","775ca69b395e7d228e5326cfbbd6a47b2456e743c684050317749cff6eec9150"]
first_seen_list = []
last_seen_list=[]
file_type_list = []
delivery_method= []
sha256_hash=[]
i=1
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
        #print(result)
        print(i)
        i+=1
        for item in result['data']:
            first_seen_list.append(item['first_seen'])
            last_seen_list.append(item['last_seen'])

            file_type_list.append(item['file_type'])
            delivery_method.append(item['delivery_method'])
            sha256_hash.append(item['sha256_hash'])

    else:
        print(f"Request failed with status code {response.status_code}.")
df = pd.DataFrame({'First Seen': first_seen_list,'Last Seen': last_seen_list, 'File Type': file_type_list, 'Delivery Method': delivery_method, 'Hash': sha256_hash})

# Save to Excel
df.to_excel('output.xlsx', index=False)