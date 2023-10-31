import logging
import re
import pandas as pd

from apify_client import ApifyClient

class AuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)


def update_dataframe_with_yellow_pages_data(data) -> pd.DataFrame:
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