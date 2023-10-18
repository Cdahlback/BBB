import re

import numpy as np
import pandas as pd
import logging

from apify_client import ApifyClient

pd.options.mode.chained_assignment = None  # Disable the warning
logging.basicConfig(filename='functions.log', level=logging.DEBUG)


scraped_yellow_pages_data = pd.DataFrame(columns=["Business Name", "City", "BusinessNameYP", "BusinessAddressYP", "BusinessPhoneYP", "BusinessWebsiteYP"])


class AuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)


def update_columns_sos(row):
    """
    Takes in a row of our dataframe with filled out values for row["BusinessNameCorrect"], row["BusinessAddressCorrect"],
    and row["BusinessZipCorrect"]

    Function makes sure we have matching name and address inorder to provide updated information

    Returns: updated row in the dataframe
    """
    if row["BusinessNameCorrect"] and row["BusinessAddressCorrect"]:
        row["BusinessNameUpdate"] = row["Business Name"]
        row["BusinessNameFound"] = "SOS" if not pd.isna(row["BusinessNameUpdate"]) else np.nan

        # Add address columns
        row["BusinessAddressUpdate"] = row["Address 1"]
        row["BusinessAddressFound"] = "SOS" if not pd.isna(row["BusinessAddressUpdate"]) else np.nan

        # Add zip columns
        row["BusinessZipUpdate"] = row["Zip Code New"]
        row["BusinessZipFound"] = "SOS" if not pd.isna(row["BusinessZipUpdate"]) else np.nan

        logging.info(f'Updated row with business name: {row["BusinessNameUpdate"]} from truth source: {row["BusinessNameFound"]}')

    return row


def add_sos_columns(merged_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates if our data is correct or not when compared to SOS
    sets null values for other columns
    """
    # See if the business name and address match
    merged_data["BusinessNameCorrect"] = merged_data["BusinessName"] == merged_data["Business Name"]
    merged_data["BusinessAddressCorrect"] = merged_data["Address"] == merged_data["Address 1"]
    merged_data["BusinessZipCorrect"] = merged_data["Zip Code"] == merged_data["Zip Code New"]

    # Give null values for all columns, which we will fill out when needed
    merged_data["BusinessNameUpdate"] = np.nan
    merged_data["BusinessNameFound"] = np.nan
    merged_data["BusinessAddressUpdate"] = np.nan
    merged_data["BusinessAddressFound"] = np.nan
    merged_data["BusinessZipUpdate"] = np.nan
    merged_data["BusinessZipFound"] = np.nan

    merged_data.apply(update_columns_sos, axis=1)

    return merged_data


def compare_dataframes_sos(historicalData: pd.DataFrame, newData: pd.DataFrame) -> pd.DataFrame | bool:
    left_on = "BusinessName"
    right_on = "Business Name"

    try:
        # Merge the data, keeping all values from historicalData rows from newData where BusinessNames match
        merged_data = historicalData.merge(newData, left_on=left_on, right_on=right_on, how='inner')
        merged_data = pd.concat([historicalData, merged_data], ignore_index=True)

        # Drop duplicate rows which contain no updated information
        merged_data['is_duplicate'] = merged_data.duplicated(subset='Firm_id', keep=False)
        merged_data = merged_data[(merged_data['is_duplicate'] & merged_data['Business Name'].notna()) | (~merged_data['is_duplicate'])]
        merged_data.drop(columns=['is_duplicate'], inplace=True)
    except KeyError as e:
        logging.debug("Exception: KeyError {0} occurred when merging historicalData with secretary of state".format(e))
        logging.debug("Length historical data: {0}".format(len(historicalData)))
        logging.debug("Length new data: {0}".format(len(newData)))
        return False

    try:
        add_sos_columns(merged_data)
    except KeyError as e:
        logging.debug("Exception: KeyError {0} occurred when accessing merged_data (historical/secretary)".format(e))
        return False

    # Select the desired columns
    result_df = merged_data[[
        'Firm_id', 'BusinessName', 'BusinessNameCorrect', 'BusinessNameUpdate', "BusinessNameFound",
        'Address', 'BusinessAddressCorrect', 'BusinessAddressUpdate', 'BusinessAddressFound',
        'Zip Code', 'BusinessZipCorrect', 'BusinessZipUpdate', 'BusinessZipFound'
        # Optional output columns
        # 'Business Filing Type', 'Filing Date', 'Status', 'Address 2', 'City', 'Region Code', 'Party Full Name',
        # 'Next Renewal Due Date'
    ]]

    logging.info("historicalData has been merged with Secretary Of State data Successfully")
    return result_df


def update_dataframe_with_yellow_pages_data(data) -> pd.DataFrame | bool:
    """
        Update the 'data' DataFrame with information from 'yellow_pages_data' based on matching 'BusinessName'.
        If a match is found, update certain columns in 'data' with corresponding values from 'yellow_pages_data'.

        :param data: The DataFrame containing your data.
        :return: The updated 'data' DataFrame.
    """
    # Calls call_scrape_yellow_page_data and fills in global dataframe scraped_yellow_pages_data
    data.apply(call_scrape_yellow_page_data, axis=1)

    for index, row in data.iterrows():
        # IF we have updated data for all data types, we can continue for that row. Since this is the lowest on the
        # trust pyramid
        if pd.notna(row["BusinessWebsiteUpdate"]) and pd.notna(
                row["BusinessPhoneUpdate"]) and pd.notna(row["BusinessAddressUpdate"]):
            continue

        # Else, see which values we can update
        business_name = row["BusinessName"]
        if pd.isna(business_name):
            return False
        matching_row = scraped_yellow_pages_data[scraped_yellow_pages_data["Business Name"] == business_name]

        if not matching_row.empty:
            # Check and update columns if they are None
            if pd.isna(row["BusinessNameUpdate"]):
                data.at[index, "BusinessNameUpdate"] = matching_row.iloc[0]["BusinessNameYP"]
                data.at[index, "BusinessNameFound"] = "YP"

            if pd.isna(row["BusinessWebsiteUpdate"]):
                data.at[index, "BusinessWebsiteUpdate"] = matching_row.iloc[0]["BusinessWebsiteYP"]
                data.at[index, "BusinessWebsiteFound"] = "YP"

            if pd.isna(row["BusinessPhoneUpdate"]):
                data.at[index, "BusinessPhoneUpdate"] = matching_row.iloc[0]["BusinessPhoneYP"]
                data.at[index, "BusinessPhoneFound"] = "YP"

            if pd.isna(row["BusinessAddressUpdate"]):
                data.at[index, "BusinessAddressUpdate"] = matching_row.iloc[0]["BusinessAddressYP"]
                data.at[index, "BusinessAddressFound"] = "YP"

    # Clean up the scraped data dataframe for the next run
    scraped_yellow_pages_data.drop(columns=scraped_yellow_pages_data.columns, inplace=True)
    return data

    # Example usage:
    # Assuming 'data' is your original DataFrame and 'scraped_yellow_pages_data' is the DataFrame with Yellow Pages data
    # updated_data = update_dataframe_with_yellow_pages_data(data, scraped_yellow_pages_data)


def call_scrape_yellow_page_data(data: pd.DataFrame) -> None:
    """
    Example usage:
    - Assuming 'df' is your dataframe, you can apply the function to each row
    - results = df.apply(call_scrape_yellow_page_data, axis=1)

    Columns Needed to search:
    - City (if no city, use "Minnesota")
    - Business Name (used as a search term)
    """

    # # This should also check for expected columns to be present
    # if len(data) == 0:
    #     return False

    search_term = data["BusinessNameUpdate"] if not pd.isna(data["BusinessNameUpdate"]) else data["BusinessName"]
    location = data["City"] if not pd.isna(data["City"]) else "Minnesota"
    max_items = 1

    # Ideally, we would store the results in their own dataFrame, making it easier to compare after this step
    result = scrape_yellow_page_data(search_term, location, max_items)

    # Add the result to the 'scraped_yellow_pages_data' DataFrame
    global scraped_yellow_pages_data
    scraped_yellow_pages_data = scraped_yellow_pages_data.append(
        {
            "Business Name": search_term,
            "City": location,
            "BusinessNameYP": result['name'],
            "BusinessAddressYP": result['address'],
            "BusinessPhoneYP": result['phone'],
            "BusinessWebsiteYP": result['url']
        },
        ignore_index=True
    )


def scrape_yellow_page_data(searchTerm: str, location: str, maxItems: int,
                            extendedOutputFunction="""
                            ($, record) => {const website = $('a.business-website').attr('href');return { website };}
                            """):
    """
    Ideally we would run this function for each row where we have an address OR searchTerm
    Input: Set of parameters listed in function
    Returned by API:
    - Dictionary filled with these values
        - Yellow pages link: 'url'
        - Company Name:      'name'
        - Address:           'address'
        - Phone:             'phone'
        - Rating (1-5):      'rating'
        - Categories:        'categories'

    We should append these columns to rows in our final output dataframe
    Columns will include:
    - BusinessNameCorrectSOS: Bool
    - BusinessNameUpdate:     string
    - AddressCorrectSOS:      Bool
    - AddressUpdate:          string
    - PhoneCorrectSOS:        Bool
    - PhoneUpdate:            string
    - RatingSOS:              int
    - BusinessCategories:     List[string]
    - POSSIBLY some extended output:
        - Data Transformation: Put the names, addresses, and phones through our normalize function prior to comparison
    """
    # Initialize the API
    client = login_yellow_pages()

    if not client:
        raise AuthenticationError("Login for yellow pages API failed")

    # Prepare the Actor input
    run_input = {
        "search": searchTerm,
        "location": location,
        "maxItems": maxItems,
        "extendOutputFunction": extendedOutputFunction,
        "proxyConfiguration": {"useApifyProxy": False}, }

    # Try to run the actor
    try:
        run = client.actor("petr_cermak/yellow-pages-scraper").call(run_input=run_input)
        logging.info("Actor petr_cermak/yellow-pages-scraper finished successfully")
    except Exception as e:
        logging.debug(f"Actor petr_cermak/yellow-pages-scraper failed, {e}")
        return False

    # Fetch and return Actor result where the name matches our name (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        # In for now, will update with standardized function
        searchTerm = re.sub(r'[^A-Za-z0-9 ]', '', searchTerm)
        if item['name'] in searchTerm:
            logging.info(
                f'Updated row with business name: {searchTerm} from truth source: YP')
            return item

    # If no result is found which matches, return False
    return False


def login_yellow_pages():
    # Try to initialize the API
    try:
        # Initialize the ApifyClient with your API token
        client = ApifyClient("apify_api_U8uBSwlhXCfv3sghNe50sbJ3udhdsY3loZKy")
        logging.info("ApifyClient API token success")
        return client
    except Exception as e:
        logging.debug(f"ApifyClient API token expired, {e}")
        return False


