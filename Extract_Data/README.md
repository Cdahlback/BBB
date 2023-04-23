# Extract_Data folder
The purpose of this folder is to contain all the scripts that actually
do all the web scraping work. They search the web to create new urls, extract data from a website, and run the independant variable functions on them. It also contains two csv files that store all of that data and check which independant variables are the best.
## Files
- create_urls.py
- data_extraction.py
- fill_ind_var_columns.py
- filled_ind_vars.csv
- best_ind_vars.csv

## create_urls.py
This file attempts to find new urls to fill in to the database. It does this in two ways:
1. Building a url from the domain name in an email address
2. Searching google for with a business's information (name, city) and checking the results for urls that are not a reviews page

## data_extraction.py
This file searches the html of a webpage for various pieces of information. It contains two functions that extract data and also contains all of our independant variable functions.
+ Extraction Functions:
    + extract_phone_data
    + extract_email_data
+ Independant Variable Functions:
    + contains_contacts_page
    + contains_business_name
    + contains_business_name_in_copyright
    + contains_social_media_links
    + contains_reviews_page
    + contains_zipCode
    + contains_phone_number
    + contains_email
    + get_domain_owner
    + url_is_review_page

## fill_ind_var_columns.py
This file runs the functions in data_extraction.py that collect data related to a website for use in the machine learning models.
It then creates a new column for each piece of data we gather in a dataframe, and attaches the result of these functions to each business. The final dataframe is then stored in filled_ind_var.csv
.