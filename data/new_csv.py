import pandas as pd
from data_extraction import contains_contacts_page, contains_business_name, contains_business_name_in_copyright, contains_reviews_page, contains_zipCode, contains_social_media_links, extract_email_data, extract_phone_data

df = pd.read_csv('sample_data.csv')

# Define the 7 new columns

df['contains_contacts_page'] = ""
df['contains_business_name'] = ""
df['contains_business_name_in_copyright'] = ""
df['contains_social_media_links'] = ""
df['contains_reviews_page'] = ""
df['contains_zipCode'] = ""
df['extract_phone_data'] = ""
df['extract_email_data'] = ""

df['contains_contacts_page'] = df['Website'].apply(contains_contacts_page)
df['contains_business_name'] = df['Website', 'business_name'].apply(contains_business_name)
df['contains_business_name_in_copyright'] = df['Website', 'business_name'].apply(contains_business_name_in_copyright)
df['contains_social_media_links'] = df['Website'].apply(contains_social_media_links)
df['contains_reviews_page'] = df['Website'].apply(contains_reviews_page)
df['contains_zipCode'] = df['Website', 'PostalCode'].apply(contains_zipCode)
df['extract_phone_data'] = df['Website', 'BusinessID'].apply(extract_phone_data)
df['extract_email_data'] = df['Website', 'BusinessID'].apply(extract_email_data)


df.to_csv('output.csv', index=False)
