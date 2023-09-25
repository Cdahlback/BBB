import pandas as pd
from BBBDM.data_processing.Tebibu import filter_dataframes

# Test filtering of valid DataFrames
def test_filter_valid_dataframes():
    df = pd.DataFrame({'name': ['Company A', None, 'Company C'],
                       'address': ['123 Main St', None, None],
                       'phone': ['555-123-4567', None, '555-789-1234'],
                       'website': ['www.companya.com', None, 'www.companyc.com']})
    
    filtered_df = filter_dataframes(df, valid_flag=True)
    
    assert len(filtered_df) == 2
    assert all(col in filtered_df.columns for col in ['name', 'address', 'phone', 'website'])

# Test filtering of invalid DataFrames
def test_filter_invalid_dataframes():
    df = pd.DataFrame({'name': [None, None, None],
                       'address': [None, None, None],
                       'phone': [None, None, None],
                       'website': [None, None, None]})
    
    filtered_df = filter_dataframes(df, valid_flag=False)
    
    assert len(filtered_df) == 3

test_filter_valid_dataframes()
test_filter_invalid_dataframes()