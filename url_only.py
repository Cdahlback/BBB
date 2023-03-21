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
import csv

# specify the input and output file names
input_file = "yagooglesearch.py.log"
output_file = "data/biruk_results.csv"

# open the input and output files
with open(input_file, "r") as in_file, open(output_file, "w", newline="") as out_file:
    # create a CSV writer for the output file
    csv_writer = csv.writer(out_file)

    # loop over each line in the input file
    for line in in_file:
        # check if the line contains "Found unique URL"
        if "Found unique URL" in line:
            # extract the URL from the line
            url = line[line.index("http"):].strip()

            csv_writer.writerow([url])


