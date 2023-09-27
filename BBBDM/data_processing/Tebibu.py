import pandas as pd

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

    return valid_df, invalid_df


# example 
df = pd.DataFrame({
    'name': ['John Doe', '', None],
    'address': ['123 Main St', '', None],
    'phone': ['1234567890', '123456789012', None],
    'website': ['www.example.com', '', None],
    'email': ['john.doe@example.com', '', None]
})

valid_df, invalid_df = filter_dataframes(df)

print("Valid DataFrame:")
print(valid_df)

print("\nInvalid DataFrame:")
print(invalid_df)
