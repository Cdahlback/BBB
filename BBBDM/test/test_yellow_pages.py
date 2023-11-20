import numpy as np
import pandas as pd

from BBBDM.lib.yellow_pages_tools import update_dataframe_with_yellow_pages_data


def test_update_dataframe_with_yellow_pages_data_pass1():
    # Create a sample 'data' DataFrame with no matching 'BusinessName' and the specified columns
    data = pd.DataFrame(
        {
            "Firm_id": [2],
            "BusinessName": [["Able Fence, Inc."]],
            "BusinessNameCorrect": [False],
            "BusinessNameUpdate": ["Able Fence, Inc."],
            "BusinessNameFound": ["SOS"],
            "Address": [["blah"]],
            "BusinessAddressCorrect": [False],
            "BusinessAddressUpdate": [np.nan],
            "BusinessAddressFound": [np.nan],
            "Zip Code": [["blah"]],
            "BusinessZipCorrect": [False],
            "BusinessZipUpdate": [np.nan],
            "BusinessZipFound": [np.nan],
            "Website": [["blah"]],
            "BusinessWebsiteCorrect": [False],
            "BusinessWebsiteUpdate": [np.nan],
            "BusinessWebsiteFound": [np.nan],
            "Phone": [["blah"]],
            "BusinessPhoneCorrect": [False],
            "BusinessPhoneUpdate": [np.nan],
            "BusinessPhoneFound": [np.nan],
            "City": [["Saint Paul"]],
        }
    )

    # Apply the function to update 'data' with non-matching data
    updated_data = update_dataframe_with_yellow_pages_data(data)

    # Check that none of the rows in 'data' have been updated
    assert isinstance(updated_data, pd.DataFrame)


def test_update_dataframe_with_yellow_pages_data_pass2():
    # Create a sample 'data' DataFrame with no matching 'BusinessName' and the specified columns
    data = pd.DataFrame(
        {
            "Firm_id": [2],
            "BusinessName": [["Able Fence, Inc."]],
            "BusinessNameCorrect": [False],
            "BusinessNameUpdate": [np.nan],
            "BusinessNameFound": [np.nan],
            "Address": [["blah"]],
            "BusinessAddressCorrect": [False],
            "BusinessAddressUpdate": [np.nan],
            "BusinessAddressFound": [np.nan],
            "Zip Code": [["blah"]],
            "BusinessZipCorrect": [False],
            "BusinessZipUpdate": [np.nan],
            "BusinessZipFound": [np.nan],
            "Website": [["blah"]],
            "BusinessWebsiteCorrect": [False],
            "BusinessWebsiteUpdate": [np.nan],
            "BusinessWebsiteFound": [np.nan],
            "Phone": [["blah"]],
            "BusinessPhoneCorrect": [False],
            "BusinessPhoneUpdate": [np.nan],
            "BusinessPhoneFound": [np.nan],
            "City": [["Saint Paul"]],
        }
    )

    # Apply the function to update 'data' with non-matching data
    updated_data = update_dataframe_with_yellow_pages_data(data)

    expected_columns = [
        "Firm_id",
        "BusinessName",
        "BusinessNameCorrect",
        "BusinessNameUpdate",
        "BusinessNameFound",
        "Address",
        "BusinessAddressCorrect",
        "BusinessAddressUpdate",
        "BusinessAddressFound",
        "Zip Code",
        "BusinessZipCorrect",
        "BusinessZipUpdate",
        "BusinessZipFound",
        "Website",
        "BusinessWebsiteCorrect",
        "BusinessWebsiteUpdate",
        "BusinessWebsiteFound",
        "Phone",
        "BusinessPhoneCorrect",
        "BusinessPhoneUpdate",
        "BusinessPhoneFound",
        "City",
    ]
    actual_columns = updated_data.columns.tolist()
    assert actual_columns == expected_columns


def test_update_dataframe_with_yellow_pages_data_pass3():
    # Create a sample 'data' DataFrame with no matching 'BusinessName' and the specified columns
    data = pd.DataFrame(
        {
            "Firm_id": [2],
            "BusinessName": ["Able Fence, Inc."],
            "BusinessNameCorrect": [False],
            "BusinessNameUpdate": [np.nan],
            "BusinessNameFound": [np.nan],
            "Address": ["blah"],
            "BusinessAddressCorrect": [False],
            "BusinessAddressUpdate": [np.nan],
            "BusinessAddressFound": [np.nan],
            "Zip Code": ["blah"],
            "BusinessZipCorrect": [False],
            "BusinessZipUpdate": [np.nan],
            "BusinessZipFound": [np.nan],
            "Website": ["blah"],
            "BusinessWebsiteCorrect": [False],
            "BusinessWebsiteUpdate": [np.nan],
            "BusinessWebsiteFound": [np.nan],
            "Phone": ["blah"],
            "BusinessPhoneCorrect": [False],
            "BusinessPhoneUpdate": [np.nan],
            "BusinessPhoneFound": [np.nan],
            "City": ["Saint Paul"],
        }
    )

    # Apply the function to update 'data' with non-matching data
    updated_data = update_dataframe_with_yellow_pages_data(data)

    assert not updated_data.empty
