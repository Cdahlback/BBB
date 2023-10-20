import pandas as pd
import logging

from apify_client import ApifyClient

pd.options.mode.chained_assignment = None  # Disable the warning
logging.basicConfig(filename='functions.log', level=logging.DEBUG)


class AuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)


def compare_dataframes(historicalData: pd.DataFrame, newData: pd.DataFrame) -> pd.DataFrame | bool:
    left_on = "BusinessName"
    right_on = "Business Name"
    try:
        # Merge historicalData and newData on the 'BusinessName' column
        merged_data = historicalData.merge(newData, left_on=left_on, right_on=right_on, how='inner')
    except KeyError as e:
        logging.debug("Exception: KeyError {0} occurred when merging historicalData with secretary of state".format(e))
        logging.debug("Length historical data: {0}".format(len(historicalData)))
        logging.debug("Length new data: {0}".format(len(newData)))
        return False

    try:
        # Calculate MatchesAddress and MatchesZip
        merged_data['MatchesAddress'] = merged_data['Address'] == merged_data['Address 1']
        merged_data['MatchesZip'] = merged_data['Zip Code_x'] == merged_data['Zip Code_y']
    except KeyError as e:
        logging.debug("Exception: KeyError {0} occurred when accessing merged_data (historical/secretary)".format(e))
        return False

    # Select the desired columns
    result_df = merged_data[['Firm_id', 'BusinessName', 'MatchesAddress', 'Address 1', 'MatchesZip', 'Zip Code_y',
                             'Business Filing Type', 'Filing Date', 'Status', 'Address 2', 'City', 'Region Code',
                             'Party Full Name', 'Next Renewal Due Date']]

    # Rename columns for clarity
    result_df.rename(columns={'Address 1': 'Address_new', 'Zip Code_y': 'Zip Code_new'}, inplace=True)
    logging.info("historicalData has been merged with Secretary Of State data Successfully")

    return result_df


def scrape_yellow_page_data(searchTerm: str, location: str, maxItems: int, givenBusinessName,
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

    # Fetch and return Actor result where the name matches our name (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if item['name'] == givenBusinessName:
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


st = "Dentist"
l = "Los Angeles"
mi = 2
eof = """($, record) => {const website = $('a.business-website').attr('href');return { website };}"""

scrape_yellow_page_data(st, l, mi, eof, "givenBusinessName")
