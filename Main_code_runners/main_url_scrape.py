from Extract_Data.create_urls import *
from Not_Our_Code.get_status_codes import *
import pandas as pd
import re

def main_scrape_urls(df):
    """
    Given a dataframe, add any missing URLs found via email or web search and check their status codes.
    If the status code is 200, add the row to the output dataframe, otherwise skip it.
    :param df: a pandas dataframe containing business information
    :return: a new pandas dataframe containing only the rows with valid URLs
    """

    bbb_df = pd.DataFrame(columns=df.columns)
    email_df = pd.DataFrame(columns=df.columns)
    search_df = pd.DataFrame(columns=df.columns)

    for index, row in df.iterrows():
        website = row['Website']
        email = row['Email']
        business_name = row['BusinessName']

        # Check if the Website column contains a URL
        if isinstance(website, str) and re.match(r'^https?://', website):
            df.loc[index, 'Website'] = website
            bbb_df = bbb_df.append(df.iloc[index], ignore_index=True)

        # If not, find a URL in the Email column
        elif isinstance(email, str):
            website = build_url_from_email(email)
            if website:
                status_code = status_code_forPandas(website)
                if status_code == 200:
                    df.loc[index, 'Website'] = website
                    email_df = email_df.append(row, ignore_index=True)
                else:
                    pass
            else:
                pass

        # If not, use the BusinessName column to find a URL
        else:
            website = search_urls(df)
            if website:
                status_code = status_code_forPandas(website)
                if status_code == 200:
                    df.loc[index, 'Website'] = website
                    search_df = search_df.append(row, ignore_index=True)
                else:
                    pass
            else:
                pass

    # return bbb_df, email_df, search_df

    print(f"Found {len(bbb_df)} rows with URLs in the Website column:")
    print(bbb_df)
    print(f"Found {len(email_df)} rows without URLs in the Website column:")
    print(email_df)
    print(f"Found {len(search_df)} rows without URLs in the Website column:")
    print(search_df)

# Concatenate the three result DataFrames with the original DataFrame
    result_df = pd.concat([bbb_df, email_df, search_df], ignore_index=True)
    return result_df


#  original DataFrame here
df = pd.read_csv('original_dataframe.csv')

# Call main function
result_df = main_scrape_urls(df)

# New DataFrame here
result_df.to_csv('result_dataframe.csv', index=False)