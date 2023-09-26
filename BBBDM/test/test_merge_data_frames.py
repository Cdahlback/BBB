"""
Test merging dataframes based on firmid"""
import sys
from pathlib import Path
data_processing_path = str(Path(__file__).resolve().parent.parent / 'data_processing')

# Append the 'data_processing' directory to sys.path
sys.path.append(data_processing_path)
#from data_processing import chris_function
import pandas as pd
print(sys.path)


def test_join_dataframe_firmid_multiple_success():
    """
    Test joining multiple dataframes in the given function
    """
    # Input dataframes
    df1 = pd.DataFrame({'FirmID': [1, 2, 3], 'Name': ['A', 'B', 'C']})
    df2 = pd.DataFrame({'FirmID': [1, 2, 3], 'Business_type': ['Construction', 'Construction', 'Something']})
    df3 = pd.DataFrame({'FirmID': [1, 2, 3], 'Location': ['USA', 'USA', 'USA']})

    #Expected output
    expected = pd.DataFrame({'FirmID': [1, 2, 3], 'Name': ['A', 'B', 'C'], 'Business_type': ['Construction', 'Construction', 'Something'], 'Location': ['USA', 'USA', 'USA']})

    # Actual output
    actual = chris_function.join_dataframe_firmid(df1, df2, df3)

    # Compare
    assert actual.equals(expected)
