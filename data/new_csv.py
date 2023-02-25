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

df['contains_contacts_page'] = df.apply(lambda row: contains_contacts_page(row['Website']), axis=1)
df['contains_business_name'] = df.apply(lambda row: contains_business_name(row['Website'], row['BusinessName']), axis=1)
df['contains_business_name_in_copyright'] = df.apply(lambda row: contains_business_name_in_copyright(row['Website'], row['BusinessName']), axis=1)
df['contains_social_media_links'] = df.apply(lambda row: contains_social_media_links(row['Website']), axis=1)
df['contains_reviews_page'] = df.apply(lambda row: contains_reviews_page(row['Website'],), axis=1)
df['contains_zipCode'] = df.apply(lambda row: contains_zipCode(row['Website'], row['PostalCode']), axis=1)
#df['extract_phone_data'] = df.apply(lambda row: extract_phone_data(row['BusinessID'], row['Website']), axis=1)
df['extract_email_data'] = df.apply(lambda row:extract_email_data(row['BusinessID'], row['Website']), axis=1)


# df['contains_contacts_page'] = df['Website'].apply(contains_contacts_page)
# df['contains_business_name'] = df.apply(contains_business_name, arg1='Website', arg2='BusinessName')
# df['contains_business_name_in_copyright'] = df.apply(contains_business_name_in_copyright, arg1='Website', arg2='BusinessName')
# df['contains_social_media_links'] = df['Website'].apply(contains_social_media_links)
# df['contains_reviews_page'] = df.apply(contains_reviews_page, arg1='Website', arg2 = 'PostalCode')
# df['contains_zipCode'] = df['Website'].apply(contains_zipCode)
# df['extract_phone_data'] = df.apply(extract_phone_data, arg1='BusinessName', arg2='Website')
# df['extract_email_data'] = df.apply(extract_email_data, arg1='BusinessName', arg2='Website')


df.to_csv('output.csv', index=False)
