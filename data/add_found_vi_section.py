import csv
input_file_name = 'mn_bbb_businesses.csv'
input_file_name2 = 'good_emails.csv'

output_file_name = 'mn_bbb_businesses_foundVia.csv'
output_file_name2 = 'good_emails_foundVia.csv'

with open(input_file_name, 'r') as input_file:
    csv_reader = csv.reader(input_file)

    header = next(csv_reader)

    header.append("found via")

    updated_rows = [header]

    for row in csv_reader:

        if any('http' in cell for cell in row):

            row.append("bbb")
        else:
            row.append("")

        updated_rows.append(row)


with open(output_file_name, 'w', newline='') as output_file:
    csv_writer = csv.writer(output_file)

    csv_writer.writerows(updated_rows)

with open(input_file_name2, 'r') as input_file:
    csv_reader = csv.reader(input_file)

    header = next(csv_reader)

    header.append("found via")

    updated_rows = [header]

    for row in csv_reader:
        if any('@' in cell for cell in row):

            row.append("Email")
        else:
            row.append("Search")

        updated_rows.append(row)


with open(output_file_name2, 'w', newline='') as output_file2:
    csv_writer2 = csv.writer(output_file2)

    csv_writer2.writerows(updated_rows)

# import pandas as pd
# import numpy as np
#
# import pandas as pd
# import numpy as np
#
# input_file_name = 'mn_bbb_addresses.csv'
#
# output_file_name = 'new.csv'
#
# df = pd.read_csv(input_file_name)
#
#
# def has_email_and_url(s):
#     return ("@" in s) and ("http" in s)
#
#
# found_via = lambda row: "BBB" if (not pd.isnull(row['Email']) and not pd.isnull(row['Website'])) else "email" if not pd.isnull(row['Email']) else "google search"
#
#
# df['foundVia'] = df.apply(lambda row: found_via(row), axis=1)
#
# df.to_csv(output_file_name, index=False)

# found_via = lambda row: "BBB" if ("http" in str(row['Text']) and "@" in str(row['Text'])) else "email" if "@" in str(row['Text']) else "google search"
#
# df['foundVia'] = df.apply(lambda row: found_via(row), axis=1)
#
# df.to_csv(output_file_name, index=False)

# def contains_email(cell):
#     if pd.isna(cell):
#         return False
#     if '@' in str(cell):
#         return True
#     return False
#
# def contains_url(cell):
#     if pd.isna(cell):
#         return False
#     if 'http' in str(cell):
#         return True
#     return False
#
# found_via = lambda row: "BBB" if ("http" in str(row) and "@" in str(row)) else "email" if "@" in str(row) else "gs"
#
# df["found via"] = df.apply(lambda row: found_via(row), axis=1)
#
# df.to_csv(output_file_name, index=False)

# df = pd.read_csv('c')
# df.head()
