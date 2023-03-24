# import pandas as pd
#
#
# file_paths = ["biruk_checked_rows.csv", "biruk_checked_rows2.csv", "biruk_checked_rows3.csv", "biruk_checked_rows4.csv", "collin_finished_rows.csv", "dylan_checked_rows.csv", "justin_checked_rows.csv", "jackson_finished_check.csv"]
#
# # Initialize an empty DataFrame
# merged_data = pd.DataFrame()
#
# # Loop through each file  and append
# for path in file_paths:
#     #data = pd.read_csv(path, engine='python')
#     data = pd.read_excel(path, engine='python')
#     merged_data = merged_data.append(data, ignore_index=True)
#
# # Write the merged data to a new Excel file
# merged_data.to_excel("merged_file.csv", index=False)

import pandas as pd

file_names = ["biruk_checked_rows.csv", "biruk_checked_rows2.csv", "biruk_checked_rows3.csv", "biruk_checked_rows4.csv", "collin_finished_rows.csv", "dylan_checked_rows.csv", "justin_checked_rows.csv", "jackson_finished_check.csv"]

dfs = []

for file_name in file_names:
    data = pd.read_csv(file_name)
    dfs.append(data)

combined_data = pd.concat(dfs)

combined_data.to_csv('combined_data.csv', index=False)

