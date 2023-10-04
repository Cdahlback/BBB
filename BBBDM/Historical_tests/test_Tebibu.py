import pandas as pd
import sys
sys.path.append(r'C:\Users\tebib\OneDrive\Desktop\Project 1\BBB')

from BBBDM.historical_functions.Tebibu import filter_dataframes


# Test filtering of valid DataFrames
def test_filter_success():
    df = pd.DataFrame({
        'name': ['Company A', 'Company C'],
        'address': ['123 Main St', '456 Oak St'],
        'phone': ['5551234567', '5557891234'],
        'website': ['www.companya.com', 'www.companyc.com'],
        'email': ['email@companya.com', 'email@companyc.com']
    })

    valid_df, invalid_df = filter_dataframes(df)

    assert len(valid_df) == 2
    assert len(invalid_df) == 0

    assert all(col in valid_df.columns for col in ['name', 'address', 'phone', 'website', 'email'])

    assert 'Company A' in valid_df['name'].values
    assert 'Company C' in valid_df['name'].values

# Test filtering of invalid DataFrames
def test_filter_failure():
    df = pd.DataFrame({
        'name': ['', None],
        'address': ['', None],
        'phone': ['12345678901234567890', None],
        'website': ['', None],
        'email': ['', None]
    })

    valid_df, invalid_df = filter_dataframes(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 2

    assert all(col in invalid_df.columns for col in ['name', 'address', 'phone', 'website', 'email'])

if __name__ == "__main__":
    test_filter_success()
    test_filter_failure()
