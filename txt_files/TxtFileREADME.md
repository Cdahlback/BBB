The text files contained in txt_files contain a few txt files with certain data we need for our algorithms.

emails_with_no_url.txt:
- Contains ALL emails in spreadsheet mn_bbb_businesses.csv (file from eli) which don't have urls filled out.
- We can take these emails and extract the urls from the end.
- From there we can use string concat to build urls to fill the csv file with
  - new_url = "https://www." + website_name (+ "/contacts/)


urls_with_no_email.txt:
- Contains ALL urls in spreadsheet mn_bbb_businesses.csv (file from eli) with no email filled out.
- We can take these urls, scrape email data from the websites and use that to fill out the csv file


urls_with_no_phone.txt:
- same as urls_with_no_email, aside from scraping phone#'s instead


