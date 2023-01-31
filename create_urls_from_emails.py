import csv
import requests
import re

# I want to take "emails_no_url.txt" as an input
# Iterate through all the emails
#   extract the domain name
#   build url around domain name
#   see what request our url gives
# add good urls to "successful_urls.txt"

# list of domain names we dont want
bad_domain_names = ['yahoo.com', 'gmail.com', "hotmail.com", "icloud.com", "comcast.net", "GMAIL.COM",
                    "outlook.com", "msn.com", "arvig.net", "charter.net", "winona.edu"]

# regex to detect valid email (works great so far, may need building upon
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def build_url(email, output_file):
    """
    :param email: email to build url from
    :return:
    If our email matches the regex and is not in our list of invalid domain names
        - Return complete URL ready to test
    If our email matches the regex, but is in our list of invalid domain names
        - Return empty string, to let the test_url function know to disregaurd it
    Else in case of not matching regex,
        - we return the full text of the email to investigate why we got a bad email from our extract_email function
    """
    if re.fullmatch(regex, email):
        domain_name = email.split("@")[-1]
        if domain_name not in bad_domain_names:
            return "https://www.{0}/".format(domain_name)
        else:
            return ""
    output_file.writerow([email])
    return ""


def test_url(url):
    """
    :param url: Passed in url we need to verify works
    :return:
    If our url is an empty string, we know it didn't pass our build_url function
        - Return an empty string, to let our main function know we don't want to add it
    If our url has a successful response (200), return the url to the main function to save it to a file
    """
    if url == "":
        print("URL not testable (either contained in the bad_domain_names or didn't match our regex)")
        return ""
    # set up a timer here on how long we want it to run for before claiming it bad
    try:
        # tries for 5 seconds, then fails
        response = requests.get(url, timeout=5)
        return url
    except Exception as e:
        print(str(e))


# input file from where we get our emails
ipt_file = open("txt_files/emails_with_no_url.txt", "r")
ipt_reader = csv.reader(ipt_file)

# Writer to the "successful_extracted_urls.txt"
opt_file = open("txt_files/successful_extracted_urls.txt", "w")
out_writer = csv.writer(opt_file)

# Writer to the "unsuccessful_emails_to_extract_urls.txt"
opt_file1 = open("txt_files/unsuccessful_emails_to_extract_urls.txt", "w")
out_writer1 = csv.writer(opt_file1)

# iterate over ipt file
for line in ipt_reader:
    # place the business id you want to stop at (this will change once threading is introduced)
    if line[0] == "1000000059":
        break
    # save email and business id
    email = line[1]
    business_id = line[0]
    # get either an empty string (didn't pass build_url) or a successfully built url
    url = test_url(build_url(email, out_writer1))
    # make sure the url is not empty before writing it to the output file
    if url:
        out_writer.writerow([business_id, url])
    print("------------------------")

# close files
ipt_file.close()
opt_file.close()
opt_file1.close()
