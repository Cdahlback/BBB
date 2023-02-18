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
