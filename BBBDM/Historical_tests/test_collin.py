import numpy as np
import pandas as pd
import pytest
from BBBDM.historical_functions.Collin import compare_dataframes_sos, \
    update_dataframe_with_yellow_pages_data  # Import your actual function here
from BBBDM.data_processing.main import join_dataframe_firmid
from BBBDM.historical_functions.Collin import extract_data

# Define a test case for a passing case in compare_dataframes
def test_compare_dataframes_pass1():
    # Create a sample historicalData DataFrame
    historicalData = pd.DataFrame({
        'Firm_id': [1, 2, 3],
        'BusinessName': ['XYZ Corp', 'LMN Ltd', 'ABC Inc'],
        'Active': [True, False, True],
        'Address': ['123 Main St', '789 Oak St', '456 Elm St'],
        'Zip Code': ['12345', '67890', '54321']
    })

    # Create a sample newData DataFrame with matching and non-matching rows
    newData = pd.DataFrame({
        'Business Name': ['XYZ Corp', 'PQR Corp', 'ABC Inc'],
        'Address 1': ['123 Main St', '777 Maple St', '456 Elm St'],
        'Zip Code New': ['12345', '99999', '54321'],
        'Business Filing Type': ['Type A', 'Type B', 'Type C'],
        'Filing Date': ['2022-01-01', '2022-02-02', '2022-03-03'],
        'Status': ['Active', 'Inactive', 'Active'],
        'Address 2': ['Suite 100', '', 'Apt 2B'],
        'City': ['City1', 'City2', 'City3'],
        'Region Code': ['NY', 'CA', 'TX'],
        'Party Full Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'Next Renewal Due Date': ['2023-01-01', '2023-02-02', '2023-03-03']
    })

    # Call your function to find matching datapoints
    result_df = compare_dataframes_sos(historicalData, newData)

    # Check if the result is a DataFrame
    assert isinstance(result_df, pd.DataFrame)

def test_compare_dataframes_pass2():
    # Create a sample historicalData DataFrame
    historicalData = pd.DataFrame({
        'Firm_id': [1, 2, 3],
        'BusinessName': ['XYZ Corp', 'LMN Ltd', 'ABC Inc'],
        'Active': [True, False, True],
        'Address': ['123 Main St', '789 Oak St', '456 Elm St'],
        'Zip Code': ['12345', '67890', '54321']
    })

    # Create a sample newData DataFrame with matching and non-matching rows
    newData = pd.DataFrame({
        'Business Name': ['XYZ Corp', 'PQR Corp', 'ABC Inc'],
        'Address 1': ['123 Main St', '777 Maple St', '456 Elm St'],
        'Zip Code New': ['12345', '99999', '54321'],
        'Business Filing Type': ['Type A', 'Type B', 'Type C'],
        'Filing Date': ['2022-01-01', '2022-02-02', '2022-03-03'],
        'Status': ['Active', 'Inactive', 'Active'],
        'Address 2': ['Suite 100', '', 'Apt 2B'],
        'City': ['City1', 'City2', 'City3'],
        'Region Code': ['NY', 'CA', 'TX'],
        'Party Full Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'Next Renewal Due Date': ['2023-01-01', '2023-02-02', '2023-03-03']
    })

    # Call your function to find matching datapoints
    result_df = compare_dataframes_sos(historicalData, newData)

    # Check if the result has the expected columns
    expected_columns = [
        'Firm_id', 'BusinessName', 'BusinessNameCorrect', 'BusinessNameUpdate', "BusinessNameFound",
        'Address', 'BusinessAddressCorrect', 'BusinessAddressUpdate', 'BusinessAddressFound',
        'Zip Code', 'BusinessZipCorrect', 'BusinessZipUpdate', 'BusinessZipFound'
    ]

    assert result_df.columns.tolist() == expected_columns


# Define a test case for a failing case in compare_dataframes
def test_compare_dataframes_fail():
    # Create two sample DataFrames with non-overlapping data
    historicalData = pd.DataFrame({
        'Firm_id': [1, 2, 3],
        'BusinessName': ['XYZ Corp', 'LMN Ltd', 'ABC Inc'],
        'Active': [True, False, True],
        'Address': ['123 Main St', '789 Oak St', '456 Elm St'],
        'Zip Code': ['12345', '67890', '54321']
    })

    # Create a sample newData DataFrame which is empty
    newData = pd.DataFrame({})

    # Call your function to find matching datapoints
    error_message = compare_dataframes_sos(historicalData, newData)

    # Check if the result is an empty DataFrame
    assert error_message is False


# Define a passing test case for update_dataframe_with_yellow_pages_data
# Define a passing test case for update_dataframe_with_yellow_pages_data
def test_update_dataframe_with_yellow_pages_data_fail():
    # Create a sample 'data' DataFrame with the specified columns
    data = pd.DataFrame({
        'Firm_id': [2],
        'BusinessName': [np.nan],
        'BusinessNameCorrect': [False],
        'BusinessNameUpdate': [np.nan],
        'BusinessNameFound': [np.nan],
        'Address': ["blah"],
        'BusinessAddressCorrect': [False],
        'BusinessAddressUpdate': [np.nan],
        'BusinessAddressFound': [np.nan],
        'Zip Code': ["blah"],
        'BusinessZipCorrect': [False],
        'BusinessZipUpdate': [np.nan],
        'BusinessZipFound': [np.nan],
        'Website': ['blah'],
        'BusinessWebsiteCorrect': [False],
        'BusinessWebsiteUpdate': [np.nan],
        'BusinessWebsiteFound': [np.nan],
        'Phone': ['blah'],
        'BusinessPhoneCorrect': [False],
        'BusinessPhoneUpdate': [np.nan],
        'BusinessPhoneFound': [np.nan],
        'City': ["Saint Paul"]
    })

    # Apply the function to update 'data'
    updated_data = update_dataframe_with_yellow_pages_data(data)

    # Check if the 'data' DataFrame has been updated correctly
    assert not updated_data


def test_update_dataframe_with_yellow_pages_data_pass1():
    # Create a sample 'data' DataFrame with no matching 'BusinessName' and the specified columns
    data = pd.DataFrame({
        'Firm_id': [2],
        'BusinessName': ["Able Fence, Inc."],
        'BusinessNameCorrect': [False],
        'BusinessNameUpdate': [np.nan],
        'BusinessNameFound': [np.nan],
        'Address': ["blah"],
        'BusinessAddressCorrect': [False],
        'BusinessAddressUpdate': [np.nan],
        'BusinessAddressFound': [np.nan],
        'Zip Code': ["blah"],
        'BusinessZipCorrect': [False],
        'BusinessZipUpdate': [np.nan],
        'BusinessZipFound': [np.nan],
        'Website': ['blah'],
        'BusinessWebsiteCorrect': [False],
        'BusinessWebsiteUpdate': [np.nan],
        'BusinessWebsiteFound': [np.nan],
        'Phone': ['blah'],
        'BusinessPhoneCorrect': [False],
        'BusinessPhoneUpdate': [np.nan],
        'BusinessPhoneFound': [np.nan],
        'City': ["Saint Paul"]
    })

    # Apply the function to update 'data' with non-matching data
    updated_data = update_dataframe_with_yellow_pages_data(data)

    # Check that none of the rows in 'data' have been updated
    assert isinstance(updated_data, pd.DataFrame)

def test_update_dataframe_with_yellow_pages_data_pass2():
    # Create a sample 'data' DataFrame with no matching 'BusinessName' and the specified columns
    data = pd.DataFrame({
        'Firm_id': [2],
        'BusinessName': ["Able Fence, Inc."],
        'BusinessNameCorrect': [False],
        'BusinessNameUpdate': [np.nan],
        'BusinessNameFound': [np.nan],
        'Address': ["blah"],
        'BusinessAddressCorrect': [False],
        'BusinessAddressUpdate': [np.nan],
        'BusinessAddressFound': [np.nan],
        'Zip Code': ["blah"],
        'BusinessZipCorrect': [False],
        'BusinessZipUpdate': [np.nan],
        'BusinessZipFound': [np.nan],
        'Website': ['blah'],
        'BusinessWebsiteCorrect': [False],
        'BusinessWebsiteUpdate': [np.nan],
        'BusinessWebsiteFound': [np.nan],
        'Phone': ['blah'],
        'BusinessPhoneCorrect': [False],
        'BusinessPhoneUpdate': [np.nan],
        'BusinessPhoneFound': [np.nan],
        'City': ["Saint Paul"]
    })

    # Apply the function to update 'data' with non-matching data
    updated_data = update_dataframe_with_yellow_pages_data(data)

    expected_columns = [
        'Firm_id', 'BusinessName', 'BusinessNameCorrect', 'BusinessNameUpdate', "BusinessNameFound",
        'Address', 'BusinessAddressCorrect', 'BusinessAddressUpdate', 'BusinessAddressFound',
        'Zip Code', 'BusinessZipCorrect', 'BusinessZipUpdate', 'BusinessZipFound',
        'Website', 'BusinessWebsiteCorrect', 'BusinessWebsiteUpdate', 'BusinessWebsiteFound',
        'Phone', 'BusinessPhoneCorrect', 'BusinessPhoneUpdate', 'BusinessPhoneFound',
        'City'
    ]
    actual_columns = updated_data.columns.tolist()
    assert actual_columns == expected_columns


def test_update_dataframe_with_yellow_pages_data_pass3():
    # Create a sample 'data' DataFrame with no matching 'BusinessName' and the specified columns
    data = pd.DataFrame({
        'Firm_id': [2],
        'BusinessName': ["Able Fence, Inc."],
        'BusinessNameCorrect': [False],
        'BusinessNameUpdate': [np.nan],
        'BusinessNameFound': [np.nan],
        'Address': ["blah"],
        'BusinessAddressCorrect': [False],
        'BusinessAddressUpdate': [np.nan],
        'BusinessAddressFound': [np.nan],
        'Zip Code': ["blah"],
        'BusinessZipCorrect': [False],
        'BusinessZipUpdate': [np.nan],
        'BusinessZipFound': [np.nan],
        'Website': ['blah'],
        'BusinessWebsiteCorrect': [False],
        'BusinessWebsiteUpdate': [np.nan],
        'BusinessWebsiteFound': [np.nan],
        'Phone': ['blah'],
        'BusinessPhoneCorrect': [False],
        'BusinessPhoneUpdate': [np.nan],
        'BusinessPhoneFound': [np.nan],
        'City': ["Saint Paul"]
    })

    # Apply the function to update 'data' with non-matching data
    updated_data = update_dataframe_with_yellow_pages_data(data)

    assert not updated_data.empty


################### TEST DATA FOR REGRESSION #################

mn_business_fp = "/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business.csv"
mn_business_address_fp = "/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_address.csv"
mn_business_contact_fp = "/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_contact.csv"
mn_business_email_fp = "/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_email.csv"
mn_business_name_fp = "/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_name.csv"
mn_business_phone_fp = "/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_phone.csv"
mn_business_url_fp = "/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_url.csv"

mn_buisness_df = pd.DataFrame({
            "firm_id": [1, 2, 3, 4],
            "active": [True, False, True, True],
            "business_type_id": [101, 102, 103, 104],
            "number_of_employees": [50, 30, 75, 60],
            "number_of_locations": [2, 1, 3, 2],
            "size_id": [3, 2, 4, 3],
            "date_established": ["2020-01-15", "2019-06-20", "2021-03-10", "2018-12-05"],
            "state_established": ["CA", "NY", "TX", "FL"],
            "date_incorporated": ["2020-01-15", "2019-06-20", "2021-03-10", "2018-12-05"],
            "state_incorporated": ["CA", "NY", "TX", "FL"],
            "date_joined_bbb": ["2020-02-10", "2019-08-15", "2021-04-05", "2019-01-20"],
            "outofbusiness_date": ["2022-05-20", "2022-12-31", "2022-10-15", None],
            "hq": ["New York", "Los Angeles", "Houston", "Miami"],
            "lastupdate": ["2023-09-30", "2023-10-16", "2023-09-25", "2023-10-10"]
        })
mn_business_address_df = pd.DataFrame({
            "address_id": [1, 2, 3, 4],
            "firm_id": [2, 5, 5, 5],
            "address_1": ["78 Acker St E", "2200 Nicollet Ave", "6855 Rowland Rd", "PO Box 46147"],
            "address_2": ["", "", "", ""],
            "city": ["Saint Paul", "Minneapolis", "Eden Prairie", "Eden Prairie"],
            "state": ["MN", "MN", "MN", "MN"],
            "zip": ["55117", "55404", "55344", "55344"],
            "verified": [True, True, False, True],
            "verifiedon": ["2011-08-31 11:47:57", "2011-08-31 11:47:57", None, "2015-10-13 12:19:00"],
        })
mn_business_contact_df = pd.DataFrame({
            "name_id": [1, 2, 3, 4],
            "firm_id": [2, 5, 5, 5],
            "company_name": ["Able Fence, Inc.", "Albin Chapel", "Albin Funeral Chapel Inc", "Albin Endeavor, Inc."],
            "condensed_name": ["ablefenceinc", "albinchapel", "albinfuneralchapelinc", "albinendeavorinc"],
            "main": [True, False, False, True],
        })
mn_business_email_df = pd.DataFrame({
            "email_id": [2, 3, 5, 6],
            "firm_id": [5, 5, 7, 7],
            "email": ["office@albinchapel.com", "jimalbinson@gmail.com", "mail@albrechtcompany.com",
                      "edward@albrechtcompany.com"],
            "modifiedon": [None, None, "2023-02-08 09:41:51.75", None],
        })
mn_business_name_df = pd.DataFrame({
            "name_id": [1, 2, 3, 4],
            "firm_id": [2, 5, 5, 5],
            "company_name": ["Able Fence, Inc.", "Albin Chapel", "Albin Funeral Chapel Inc", "Albin Endeavor, Inc."],
            "condensed_name": ["ablefenceinc", "albinchapel", "albinfuneralchapelinc", "albinendeavorinc"],
            "main": [True, False, False, True],
        })
mn_business_phone_df = pd.DataFrame({
            "phone_id": [1, 2, 3, 4],
            "firm_id": [2, 5, 5, 5],
            "address_id": [1, 3, 3, 5],
            "phone": ["6512224355", "9529149410", "6128711418", "6122700491"],
            "verified": [False, False, False, False],
            "verifiedon": [None, None, None, None],
            "modifiedon": ["2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733",
                           "2016-03-25 07:01:12.733"],
            "createdon": ["2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733",
                          "2016-03-25 07:01:12.733"]
        })
mn_business_url_df = pd.DataFrame({
            "url_id": [1, 3, 5, 6],
            "firm_id": [5, 9, 10, 18],
            "url": ["http://www.albinchapel.com/", "http://www.arthurwilliamsoptical.com/", "http://www.ablemovers.net",
                    "http://www.andersencorp.com"],
            "main": [True, True, False, False],
            "verified": [False, True, True, True],
            "verifiedon": [None, "2019-10-11 10:10:03.84", "2017-10-17 13:16:13.123", "2022-10-26 13:24:22.983"],
            "createdon": [None, None, None, None],
            "modifiedon": [None, None, None, "2022-10-26 13:24:22.737"]
        })


#################### REGRESSION TESTS ###################

def test_regression_extract(mn_business_fp, mn_business_address_fp, mn_business_contact_fp, mn_business_email_fp,
                            mn_business_name_fp, mn_business_phone_fp, mn_business_url_fp):
    """
    Tests to ensure no paths return errors, and all dataframes are not none
    """
    mn_business_df = extract_data(mn_business_fp)
    mn_business_address_df = extract_data(mn_business_address_fp)
    mn_business_contact_df = extract_data(mn_business_contact_fp)
    mn_business_email_df = extract_data(mn_business_email_fp)
    mn_business_name_df = extract_data(mn_business_name_fp)
    mn_business_phone_df = extract_data(mn_business_phone_fp)
    mn_business_url_df = extract_data(mn_business_url_fp)

    assert all(df is not None for df in [mn_business_df, mn_business_address_df, mn_business_contact_df,
                                         mn_business_email_df, mn_business_name_df, mn_business_phone_df, mn_business_url_df])


def test_regression_merge(mn_buisnesses_df, mn_business_address_df, mn_business_contact_df, mn_business_email_df,
                           mn_business_name_df, mn_business_phone_df, mn_business_url_df):
    """Test to ensure that when we merge on firm_id, we get the expected columns"""
    # Test a specific regression case
    result = join_dataframe_firmid(mn_buisnesses_df, mn_business_address_df, mn_business_contact_df,
                                   mn_business_email_df, mn_business_name_df, mn_business_phone_df,
                                   mn_business_url_df)
    expected_columns = [""]
    assert result.columns.tolist() == expected_columns


def test_regression_check_standard():
    """
    Test to ensure only valid data is cross-validated with our trusted sources
    """


def test_regression_sos_compare1():
    """
    Test to ensure comparing with SOS adds needed columns
    """


def test_regression_sos_compare2():
    """
    Test to ensure returned dataframe after comparing is not empty
    """


def test_regression_google_compare1():
    """
    Test to ensure comparing with Google places adds needed columns
    """


def test_regression_google_compare2():
    """
    Test to ensure returned dataframe after comparing is not empty
    """


def test_regression_yp_compare1():
    """
    Test to ensure comparing with YP adds needed columns
    """


def test_regression_yp_compare2():
    """
    Test to ensure returned dataframe after comparing is not empty
    """


def test_regression_merge_final_output():
    """
    Test to ensure all expected columns are present
    """