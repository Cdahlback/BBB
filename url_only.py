import re
import pandas as pd

true_list = []
business_IDs = []
websites = []

terminal_txt = open('yagooglesearch.py.log', 'r')
for line in terminal_txt:
    if re.match(r'^\d{8}.*', line):
        true_list.append(line)

for entry in true_list:
    delete = re.sub(r'\n', '', entry)
    split = re.split(r' ', delete)
    if len(split) == 1:
        business_IDs.append(split[0])
        websites.append('')
    else:
        business_IDs.append(split[0])
        websites.append(split[1])

dict_for_pandas = {"BusinessID": business_IDs, "Website": websites}
complete = pd.DataFrame(dict_for_pandas)

complete.to_csv('data/biruk_results.csv')