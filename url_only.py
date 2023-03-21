# import re
# import pandas as pd

# true_list = []
# business_IDs = []
# websites = []

# terminal_txt = open('yagooglesearch.py.log', 'r')
# for line in terminal_txt:
#     if re.match(r'^\d{8}.*', line):
#         true_list.append(line)

# for entry in true_list:
#     delete = re.sub(r'\n', '', entry)
#     split = re.split(r' ', delete)
#     if len(split) == 1:
#         business_IDs.append(split[0])
#         websites.append('')
#     else:
#         business_IDs.append(split[0])
#         websites.append(split[1])

# dict_for_pandas = {"BusinessID": business_IDs, "Website": websites}
# complete = pd.DataFrame(dict_for_pandas)

# complete.to_csv('data/biruk_results.csv')

# import csv

# # specify the input and output file names
# input_file = "yagooglesearch.py.log"
# output_file = "data/biruk_results.csv"

# # open the input and output files
# with open(input_file, "r") as in_file, open(output_file, "w", newline="") as out_file:
#     # create a CSV writer for the output file
#     csv_writer = csv.writer(out_file)

#     # loop over each line in the input file
#     for line in in_file:
#         # check if the line contains "Found unique URL"
#         if "Found unique URL" in line:
#             # extract the URL from the line
#             url = line[line.index("http"):].strip()

#             csv_writer.writerow([url])

# import csv

# with open('data/biruk.csv', mode='r') as input_file, open('output.csv', mode='w', newline='') as output_file:
#     reader = csv.DictReader(input_file)
#     writer = csv.DictWriter(output_file, fieldnames=['BusinessID', 'BusinessName'])
#     writer.writeheader()

#     for row in reader:
#         business_id = row['BusinessID']
#         business_name = row['BusinessName']
#         writer.writerow({'BusinessID': business_id, 'BusinessName': business_name})

import pandas as pd

# Load the first CSV file
df1 = pd.read_csv('data/biruk_results.csv')

# Load the second CSV file
df2 = pd.read_csv('output.csv')

# Merge the two dataframes based on a common column
merged_df = pd.merge(df1, df2, on='BusinessID,BusinessName,URL')

# Save the merged dataframe to a new CSV file
merged_df.to_csv('merged_file.csv', index=False)






