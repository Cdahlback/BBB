import logging
import os
import pandas as pd
from apify_client import ApifyClient


scraped_yellow_pages_data = pd.DataFrame(columns=["Business Name", "City", "BusinessNameYP", "BusinessAddressYP",
                                                  "BusinessPhoneYP", "BusinessWebsiteYP"])


# Custom Exception class for Authentication Errors.
class AuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)


def update_dataframe_with_yellow_pages_data(data) -> pd.DataFrame:
    """
    Update the given DataFrame 'data' with information from Yellow Pages based on matching business names.
    If matching data is found in Yellow Pages, updates corresponding columns in the 'data' DataFrame.
    The updates are performed based on the presence of certain columns in the original 'data'.

    :param data: DataFrame containing the original data.
    :return: Updated DataFrame.
    """

    # For each row in the input data, try to scrape Yellow Pages data.
    data.apply(call_scrape_yellow_page_data, axis=1)

    # Iterate through each row of the data.
    for index, row in data.iterrows():
        # If all update fields have data, skip processing for this row.
        if (
            pd.notna(row["BusinessWebsiteUpdate"])
            and pd.notna(row["BusinessPhoneUpdate"])
            and pd.notna(row["BusinessAddressUpdate"])
        ):
            continue

        # Check if we have any data to update from the scraped_yellow_pages_data based on matching business name.
        business_name = row["BusinessName"]
        matching_row = scraped_yellow_pages_data[
            scraped_yellow_pages_data["Business Name"] == business_name
        ]

        if not matching_row.empty:
            # Update data fields if they're not already populated.
            # Here we're looking for BusinessName, Website, Phone, and Address.
            # If found in the Yellow Pages data, we update the original dataframe and mark the source as 'YP'.
            for column, yp_column in [
                ("BusinessNameUpdate", "BusinessNameYP"),
                ("BusinessWebsiteUpdate", "BusinessWebsiteYP"),
                ("BusinessPhoneUpdate", "BusinessPhoneYP"),
                ("BusinessAddressUpdate", "BusinessAddressYP"),
            ]:
                if pd.isna(row[column]):
                    data.at[index, column] = matching_row.iloc[0][yp_column]
                    data.at[index, column.replace("Update", "Found")] = "YP"

    # Clean up the Yellow Pages data for next usage by dropping all its columns.
    scraped_yellow_pages_data.drop(
        columns=scraped_yellow_pages_data.columns, inplace=True
    )

    return data


def call_scrape_yellow_page_data(data: pd.DataFrame) -> None:
    """
    Calls the scrape_yellow_page_data function for each row in the dataframe.
    Extracts required fields and invokes the scraper function.
    Results from scraper are stored in a global dataframe.

    :param data: Row from the dataframe.
    """

    # Construct the search term and location from the data.
    search_term = (
        data["BusinessNameUpdate"]
        if not pd.isna(data["BusinessNameUpdate"])
        else data["BusinessName"]
    )
    location = data["City"] if not pd.isna(data["City"]) else "Minnesota"

    if not isinstance(search_term, str):
        return
    # Invoke the scraper for the given search term and location.
    result = scrape_yellow_page_data(search_term, location, maxItems=1)

    # Add the scraped data to the global dataframe.
    global scraped_yellow_pages_data
    scraped_yellow_pages_data = scraped_yellow_pages_data.append(
        {
            "Business Name": search_term,
            "City": location,
            "BusinessNameYP": result["name"],
            "BusinessAddressYP": result["address"],
            "BusinessPhoneYP": result["phone"],
            "BusinessWebsiteYP": result["url"],
        },
        ignore_index=True,
    )


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

    # Iterate through the actor's results and return the relevant data based on the search term.
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if item["name"] in searchTerm:
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
        logging.debug(f"ApifyClient API token expired, {e}")
        return False
