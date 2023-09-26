import pandas as pd

df = pd.read_csv('./Data/mn_business_name.csv')

null_values_business_name = df['company_name'].isnull()

null_count_business_name = null_values_business_name.sum()

print(null_count_business_name)