# extract_data folder

## Files
- create_urls.py
- data_extraction.py
- fill_ind_var_columns.py

### create_urls.py
This file attempts to find new urls to fill in to the database. It does this in two ways:
1. Building a url from the domain name in an email address
2. Searching google for with a business's information (name, city) and checking the results for urls that are not a reviews page

### data_extraction.py
This file searches the html of a webpage for various pieces of information.
This information is both data to fill in gaps in the database and data used for the machine learning model.

### fill_ind_var_columns.py
This file runs the functions in data_extraction.py that collect data related to a website for use in machine learning models.
It then creates a new column for each piece of data we gather in a dataframe, and attaches the result of these functions to each business.
