import pandas as pd
import logging


logging.basicConfig(filename='functions.log', encoding='utf-8', level=logging.DEBUG)

def filter_dataframes(df):
    conditions = (
        ((df['name'].notna() & (df['name'] != '')) |
         (df['address'].notna() & (df['address'] != '')) |
         (df['phone'].notna() & df['phone'].str.match(r'^\d{10}$')) |
         (df['website'].notna() & (df['website'] != '')) |
         (df['email'].notna() & (df['email'] != ''))
        )
    )

    valid_df = df[conditions]
    invalid_df = df[~conditions]

    # Log information about the valid and invalid DataFrames
    logging.info("Valid DataFrame:\n%s", valid_df.to_string())
    logging.info("Invalid DataFrame:\n%s", invalid_df.to_string())

    return valid_df, invalid_df


df = pd.DataFrame({
    'name': ['John Doe', '', None],
    'address': ['123 Main St', '', None],
    'phone': ['1234567890', '123456789012', None],
    'website': ['www.example.com', '', None],
    'email': ['john.doe@example.com', '', None]
})

valid_df, invalid_df = filter_dataframes(df)
