import csv
input_file_name = 'mn_bbb_businesses.csv'

output_file_name = 'output.csv'

with open(input_file_name, 'r') as input_file:
    csv_reader = csv.reader(input_file)

    header = next(csv_reader)

    header.append("found vi")

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
