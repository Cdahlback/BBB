import pandas as pd

def filter_dataframes(df, valid_flag=True):
    if valid_flag:
        # Keep rows with at least one non-null value in 'name', 'address', 'phone', or 'website'
        filtered_df = df.dropna(subset=['name', 'address', 'phone', 'website'], how='all')
    else:
        # Keep rows where all values in 'name', 'address', 'phone', and 'website' are null
        filtered_df = df[~df[['name', 'address', 'phone', 'website']].notna().any(axis=1)]
    
    return filtered_df
