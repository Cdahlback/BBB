import pandas as pd

"""
Script uses pandas to add FoundVia column to current mn_bbb_businesses.csv data

FoundVia: Determines where URL came from (or is going to come from) in the current
          Database. There are three values in FoundVia.
          1.) "BBB" is when the URL was already in the current database.
          2.) "Email" is the URL we might obtain from the email that is in the current database.
          3.) "Search" is the URL we might obtain using the business name
              to google search for the URL.
              
          Note: There are pre-set values, if we end up not finding a URL from either the Email or
          Searching methods, then we will not end up using the business for feature selection.
"""

BBB_file = pd.read_csv('data/mn_bbb_businesses.csv')

# add new column in database
BBB_file['FoundVia'] = ''

# if business row already has a URL, then its extracted and given the "BBB" value
has_URL = BBB_file.loc[BBB_file['Website'].notna()]
has_URL['FoundVia'] = "BBB"

# If business row already has an email, but no URL, then its extracted and given "Email" value
has_Email = BBB_file.loc[BBB_file['Email'].notna() & BBB_file['Website'].isna()]
has_Email['FoundVia'] = "Email"

# If business row neither and email or URL, then its extracted and give "Search" value
has_Neither = BBB_file.loc[BBB_file['Email'].isna() & BBB_file['Website'].isna()]
has_Neither['FoundVia'] = 'Search'

# merges all extracted datasets back into one dataset
frames = [has_URL, has_Email, has_Neither]
mn_bbb_businesses_foundVia = pd.concat(frames)

# converts to csv file
mn_bbb_businesses_foundVia.to_csv('data/mn_bbb_businesses_foundVia.csv')
