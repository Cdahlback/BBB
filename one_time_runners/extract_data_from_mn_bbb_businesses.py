"""Functions built to extract info contained in mn_bbb_businesses.csv. ONLY NEEDS TO RUN WHEN SPREADSHEET IS CHANGED!"""

# module to read/write to csv
import csv


def extract_all(opt_file_path):
    """Extracts all from the file"""
    inputFile = open('mn_bbb_businesses.csv', 'r')
    inputReader = csv.reader(inputFile)

    outputFile = open(opt_file_path, 'w')
    outputWriter = csv.writer(outputFile)

    for row in inputReader:
        if row[0] != "704":
            continue
        # this is modeling a stop the csv reader once we hit 100 rows
        text = row[11]
        # write column 3 to file
        outputWriter.writerow([row[1], text])

    outputFile.close()
    inputFile.close()


def extract_urls_with_no_email(opt_file_path):
    """Extract all urls with no email"""
    inputFile = open('mn_bbb_businesses.csv', 'r')
    inputReader = csv.reader(inputFile)

    outputFile = open(opt_file_path, 'w')
    outputWriter = csv.writer(outputFile)

    for row in inputReader:
        if row[0] != "704":
            continue
        if row[11] == "":
            continue
        if row[10] == "":
            try:
                outputWriter.writerow((row[1], row[11]))
            except Exception as e:
                print(str(e))

    outputFile.close()
    inputFile.close()


def extract_urls_with_no_phone(opt_file_path):
    """Extract all urls with no phone number (Only a function so it doesn't run when I run this file)"""
    inputFile = open('mn_bbb_businesses.csv', 'r')
    inputReader = csv.reader(inputFile)

    outputFile = open(opt_file_path, 'w')
    outputWriter = csv.writer(outputFile)

    for row in inputReader:
        if row[0] != "704":
            continue
        if row[11] == "":
            continue
        if row[9] == "":
            try:
                outputWriter.writerow((row[1], row[11]))
            except Exception as e:
                print(str(e))

    outputFile.close()
    inputFile.close()


def extract_emails_no_url(opt_file_path):
    """Extract all emails with no url (Only a function so it doesn't run when I run this file)"""
    inputFile = open('mn_bbb_businesses.csv', 'r')
    inputReader = csv.reader(inputFile)

    outputFile = open(opt_file_path, 'w')
    outputWriter = csv.writer(outputFile)

    for row in inputReader:
        # not needed if top two lines of ipt file are deleted
        if row[0] != "704":
            continue
        if row[10] == "":
            continue
        if row[11] == "":
            try:
                outputWriter.writerow((row[1], row[10]))
            except Exception as e:
                print(str(e))

    outputFile.close()
    inputFile.close()


# EXAMPLE RUN
# extract_urls_with_no_phone("txt_files/emails_with_no_url.txt")