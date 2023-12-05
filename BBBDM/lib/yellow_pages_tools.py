import logging
import os
import time

import numpy as np
import pandas as pd
from apify_client import ApifyClient
from lib.data_processing import is_same_business
from pandarallel import pandarallel

pandarallel.initialize()


scraped_yellow_pages_data = pd.DataFrame(
    columns=[
        "Business Name",
        "City",
        "BusinessNameYP",
        "BusinessAddressYP",
        "BusinessPhoneYP",
        "BusinessWebsiteYP",
    ]
)


# Custom Exception class for Authentication Errors.
class AuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)


def add_yp_columns(data):
    data["BusinessNameYP"] = np.nan
    data["AddressYP"] = np.nan
    data["PhoneYP"] = np.nan
    data["WebsiteYP"] = np.nan
    return data


def update_dataframe_with_yellow_pages_data(data) -> pd.DataFrame:
    """
    Update the given DataFrame 'data' with information from Yellow Pages based on matching business names.
    If matching data is found in Yellow Pages, updates corresponding columns in the 'data' DataFrame.
    The updates are performed based on the presence of certain columns in the original 'data'.

    :param data: DataFrame containing the original data.
    :return: Updated DataFrame.
    """

    data = add_yp_columns(data)

    # For each row in the input data, try to scrape Yellow Pages data.
    data = data.parallel_apply(call_scrape_yellow_page_data, axis=1)

    # Iterate through each row of the data.
    for index, row in data.iterrows():
        # Check all columns in the row, to see if we need to check with yp
        if (
            (row["BusinessNameCorrect"] == True)
            & (row["PhoneCorrect"] == True)
            & (row["WebsiteCorrect"] == True)
            & (row["EmailCorrect"] == True)
            & (row["ZipCorrect"] == True)
            & (row["AddressCorrect"] == True)
        ):
            continue
        else:
            # If we haven't found a business name to update with
            if not isinstance(row["BusinessNameFound"], str):

                # Check if we have any new values from YP
                if is_same_business(row["BusinessNameYP"], row["BusinessName"][0]):
                    row["BusinessNameUpdate"].append(row["BusinessNameYP"])
                    row["BusinessNameFound"] = "YP"
                    row["BusinessNameCorrect"] = True

                # Update the rest of the missing information
                if row["PhoneCorrect"] and row["BusinessNameCorrect"]:
                    row["PhoneUpdate"].append(row["PhoneYP"])
                    row["PhoneFound"] = "YP" if pd.notna(row["PhoneYP"]) else np.nan
                    row["PhoneCorrect"] = True if pd.notna(row["PhoneYP"]) else False
                if row["WebsiteCorrect"] and row["BusinessNameCorrect"]:
                    row["WebsiteUpdate"].append(row["WebsiteYP"])
                    row["WebsiteFound"] = "YP" if pd.notna(row["WebsiteYP"]) else np.nan
                    row["WebsiteCorrect"] = True if pd.notna(row["WebsiteYP"]) else False
                if row["AddressCorrect"] and row["BusinessNameCorrect"]:
                    row["AddressUpdate"].append(row["AddressYP"])
                    row["AddressFound"] = "YP" if pd.notna(row["AddressYP"]) else np.nan
                    row["AddressCorrect"] = True if pd.notna(row["AddressYP"]) else False

                data.loc[index] = row

    return data


def call_scrape_yellow_page_data(row: pd.Series) -> None:
    """
    Calls the scrape_yellow_page_data function for each row in the dataframe.
    Extracts required fields and invokes the scraper function.
    Results from scraper are stored in a global dataframe.

    :param row: Row from the dataframe.
    """

    # Construct the search term and location from the data.
    search_term = (
        row["BusinessNameUpdate"][0]
        if len(row["BusinessNameUpdate"]) > 0
        else row["BusinessName"][0]
    )
    location = row["City"] if pd.notna(row["City"]) else "Minnesota"

    if not isinstance(search_term, str):
        return row
    # Invoke the scraper for the given search term and location.
    result = scrape_yellow_page_data(search_term, location, maxItems=1)

    if not result:
        return row

    # Add the scraped data to the global dataframe.
    global scraped_yellow_pages_data
    try:
        row["BusinessNameYP"] = result["name"]
        row["AddressYP"] = result["address"]
        row["PhoneYP"] = result["phone"]
        row["WebsiteYP"] = result["url"]
    except Exception as e:
        print(str(e))

    return row


def scrape_yellow_page_data(
    searchTerm: str, location: str, maxItems: int, extendedOutputFunction="""..."""
):
    """
    Uses the ApifyClient to scrape Yellow Pages for the given search term, location, and other parameters.
    Returns the scraped data if a match is found, otherwise returns False.

    :param searchTerm: The business name or other keyword to search.
    :param location: The location to focus the search on.
    :param maxItems: Maximum number of results to fetch.
    :param extendedOutputFunction: JS function to extract additional fields (optional).
    :return: Dictionary of scraped data or False.
    """

    # Initialize the API.
    client = login_yellow_pages()

    # If client creation failed, raise an error.
    if not client:
        raise AuthenticationError("Login for yellow pages API failed")

    # Prepare the input for the Apify actor which will perform the scrape.
    run_input = {
        "search": searchTerm,
        "location": location,
        "maxItems": maxItems,
        "extendOutputFunction": "($, record) => {return {};}",
        "proxyConfiguration": {"useApifyProxy": False},
    }

    # Execute the actor and log appropriate messages based on success/failure.
    try:
        run = client.actor("petr_cermak/yellow-pages-scraper").call(run_input=run_input)
        logging.info("Actor petr_cermak/yellow-pages-scraper finished successfully")
    except Exception as e:
        logging.debug(f"Actor petr_cermak/yellow-pages-scraper failed, {e}")
        return False

    # Future improvement: Should implement async instead of sleeping, will save time
    time.sleep(7)

    # Iterate through the actor's results and return the relevant data based on the search term.
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if is_same_business(item["name"], searchTerm):
            logging.info(
                f"Updated row with business name: {searchTerm} from truth source: YP"
            )
            return item

    return False


def login_yellow_pages():
    """
    Tries to authenticate and initialize the ApifyClient using a hardcoded API token.
    Returns the client if successful, otherwise logs an error and returns False.

    :return: ApifyClient or False.
    """

    try:
        client = ApifyClient(os.getenv("YELLOW_PAGES_API_TOKEN"))
        logging.info("ApifyClient API token success")
        return client
    except Exception as e:
        logging.error(f"ApifyClient API token expired, {e}")
        return False
