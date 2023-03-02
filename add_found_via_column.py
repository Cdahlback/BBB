import pandas as pd

BBB_file = pd.read_csv('data/mn_bbb_businesses.csv')

BBB_file['FoundVia'] = ''

has_URL = BBB_file.loc[BBB_file['Website'].notna()]
has_URL['FoundVia'] = "BBB"

has_Email = BBB_file.loc[BBB_file['Email'].notna() & BBB_file['Website'].isna()]
has_Email['FoundVia'] = "Email"

has_Neither = BBB_file.loc[BBB_file['Email'].isna() & BBB_file['Website'].isna()]
has_Neither['FoundVia'] = 'Search'

frames = [has_URL, has_Email, has_Neither]
mn_bbb_businesses_foundVia = pd.concat(frames)
compiled = mn_bbb_businesses_foundVia.reset_index(drop=True)

compiled.to_csv('data/mn_bbb_businesses_foundVia.csv')