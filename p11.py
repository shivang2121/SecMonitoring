# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 02:06:19 2023

@author: shiva
"""

# Read the contents of the file
with open('quakbot_hashes.txt', 'r') as file:
    data = file.read()

# Split the data into individual lines (assuming each line contains one hash)
hash_list = data.strip().split('\n')

# Print the resulting list
print(hash_list)
