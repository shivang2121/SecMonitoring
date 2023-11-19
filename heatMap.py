import os
import json
import csv
import xlsxwriter
from collections import Counter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# Get the current directory
current_directory = os.getcwd()

# List all files in the directory
file_names = os.listdir(current_directory)

# Filter only JSON files
json_files = [file for file in file_names if file.endswith('.json')]
appended_list = []

# Loop through each JSON file
for json_file in json_files:
    with open(os.path.join(current_directory, json_file), 'r') as file:
        data = json.load(file)
        techniques = data.get('techniques', [])
        appended_list.extend(techniques)

filtered_technique_ids = [entry['techniqueID'] for entry in appended_list if 'techniqueID' in entry and '.' not in entry['techniqueID']]

# Count the frequency of technique IDs
technique_id_counts = Counter(filtered_technique_ids)

# Sort the technique IDs by frequency in decreasing order
sorted_technique_ids = sorted(technique_id_counts.items(), key=lambda item: item[1], reverse=True)





# Initialize a list to store the appended data
data = []

# Open the original CSV file
with open('t2.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Get the headers
    data.append([headers[0], headers[1], headers[7]])  # Append headers for the selected columns

    for row in reader:
        data.append([row[0], row[1], row[7]])  # Append the required columns

# Save the appended data to a new CSV file
with open('appended_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

            

# Save the data to a CSV file
with open('HeatMapData2.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Technique ID', 'Frequency', 'Technique','Tactic'])
    for technique_id, frequency in sorted_technique_ids:
        for total_data in data:
            #print(total_data[0])
            if(technique_id==total_data[0]):
                writer.writerow([technique_id, frequency,total_data[1],total_data[2]])

                #print("SHI")

print("Data has been saved to HeatMapData.csv")




dfz = pd.read_csv('HeatMapData.csv')

# Read the data from the CSV file
df = pd.read_csv('HeatMapData.csv')

# Filter the DataFrame to include only rows with frequency >= 2
df_filtered = df[df['Frequency'] >= 2]

# Pivot the filtered DataFrame to make Technique as subheaders of each Tactic
df_pivot = df_filtered.pivot_table(index='Tactic', columns='Technique', values='Frequency', fill_value=0)

# Create a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(df_pivot, annot=True, cmap='YlGnBu', fmt='g')
plt.title('Technique Frequency Heatmap (Frequency >= 2)')
plt.show()





val1=[]
# Open the CSV file for reading
with open('HeatMapFin.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

# Create a new Excel file
workbook = xlsxwriter.Workbook('HeatMsapV1.xlsx')
worksheet = workbook.add_worksheet()
freq=[]
for i in range(0,len(dfz)):
    freq.append(dfz.iloc[i,1])
frequencies=freq
norm = plt.Normalize(min(frequencies), max(frequencies))
colors = plt.cm.RdYlBu_r(norm(frequencies))
tot_freq=sum(frequencies)
# Convert RGB to HEX
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

main_list=[]
main_cols=[]
row_cols=[]
dfzz = pd.DataFrame(columns=['Value', 'Row', 'Column', 'Freq', 'Color'])
data3=data
# Iterate through the data and write it to the Excel file
for row_num, data_row in enumerate(data):
    row_list=[]
    cols=[]
    rows=[]
    for col_num, value in enumerate(data_row):
        # Apply color to cells with the value "SHIV"
        for i in range(0,len(dfz)):
            val=(dfz.iloc[i,2])
            #val1.append(val)
            if value == val:
                #colors[]
                row_list.append(dfz.iloc[i,1])
                cols.append(col_num)
                rows.append(row_num)
                cell_format = workbook.add_format({'bg_color': rgb_to_hex(colors[i])})
                value=str(value)
                print(value)
                #worksheet.write(row_num, col_num, value, cell_format)
                dfzz = dfzz.append({'Value': value, 'Row': row_num, 'Column': col_num, 'Color': rgb_to_hex(colors[i]), 'Freq': dfz.iloc[i,1]}, ignore_index=True)
                



for col_num, data_column in enumerate(zip(*data)):
    for row_num, value in enumerate(data_column):
        # Apply color to cells with the value "SHIV"
        for i in range(0,len(dfz)):
            val=(dfz.iloc[i,2])
            #val1.append(val)
            if value == val:
                #colors[]
                cell_format = workbook.add_format({'bg_color': rgb_to_hex(colors[i])})
                value=str(value)
                print(value)
                #worksheet.write(row_num, col_num, value, cell_format)

# Storing the data for each column in a list of lists
# Your existing code

# List to store data for each column
# Your existing code

# List to store data for each column
column_data = []

# Iterate through the data and store values for each column
for col_num, data_column in enumerate(zip(*data)):
    col_data = []
    for row_num, value in enumerate(data_column):
        # Apply color to cells with the value "SHIV"
        for i in range(len(dfz)):
            val = dfz.iloc[i, 2]
            if value == val:
                col_data.append((row_num, value, colors[i], dfz.iloc[i, 1]))

    # Sorting the data in each column based on frequency
    col_data.sort(key=lambda x: x[3], reverse=True)

    # Adding the column to the worksheet in decreasing order of frequency
    i=1
    for index, (col_row_num, value, color, freq) in enumerate(col_data):
        cell_format = workbook.add_format({'bg_color': rgb_to_hex(color)})
        value = str(value)
        print(value)
        percent_value = f"{freq/tot_freq:.1%}"
        value_with_percent = f"{value}: {percent_value}"
        
        worksheet.write(i, col_num, value_with_percent, cell_format)
        i+=1
        


workbook.close()
