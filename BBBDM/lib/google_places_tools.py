"""
Various Google Places tool utilizing Google Places API
"""
import logging
import os

import pandas as pd
import requests
from lib.data_processing import is_same_business
from lib.Normalizing import (
    normalize_address_i18n,
    normalize_url,
    normalize_us_phone_number,
    standardizeName,
)

# ENV_PATH = str(Path(__file__).parent.parent.parent / ".env")
# load_dotenv(dotenv_path=ENV_PATH)
# Setup logging to capture detailed logs about warnings, errors, and other critical information.
logging.basicConfig(filename="functions.log", level=logging.DEBUG)


class google_maps:
    """
    The class that will be used to interact with the Google Places 2.0 API
    """

    api_key = ""
    place_ids = []

    # Initialized our object the url and fields that will be used
    def __init__(self, api_key: str):
        """
        Object focused on interacting with the Google Places API and returning the information that is needed

        AKA it returns:

        Name
        URL
        Address
        Phone Number
        Googles place_id

        from the given api_key
        """
        self.api_key = api_key

    def find_place(self, input: str):
        """
        Finds the place based on the input and input_type and returns the fields that are specified

        :parameter input: The input that is being searched for such as the name of the business

        :parameter fields: The fields that are being returned from the API at the second level field and down

        :return: dictionary of the information that is returned from the API
        """
        url = "https://places.googleapis.com/v1/places:searchText"

        headers = {
            "Context-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "places.id",
        }
        # Appends the first level field to the fields
        # field_str = ""
        # for field in fields:
        #     if field == "displayName":
        #         field_str = field_str + ",places.displayName.text"
        #     else:
        #         field_str = field_str + ",places." + field.strip()

        data = {
            "textQuery": input,
        }
        # Sends the request to the API and returns the json
        try:
            logging.info("Sending request to Google API for place_id")
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                try:
                    self.place_ids = response.json()["places"].values()
                except KeyError:
                    logging.error("Could not find place_id, no results returned")
                    return None
            else:
                logging.error(
                    f"Invalid request with response code {response.status_code}"
                )
                raise Exception(
                    f"Invalid request with response code {response.status_code}"
                )
        except Exception as e:
            logging.error("Could not connect to Google API")
            raise Exception(f"Could not connect to Google Places API {e}")

    def details(self, input: str) -> dict:
        """
        Finds the details of the place based on the place_id and returns the fields that are specified

        :parameter input: The input that is being searched for such as the name of the business

        :parameter fields: The fields that are being returned from the API at the second level field and down
        """
        self.find_place(input)

        return_values = {"Name": [], "Address": [], "PhoneNumber": [], "Website": []}

        # Checks to see if the place_id was found
        if not self.place_ids:
            logging.info("No places found please try with different input")
            return None

        # Iterates over the place_ids and finds the details for each one
        for id in self.place_ids:
            url = "https://places.googleapis.com/v1/places/" + id
            headers = {
                "Context-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
                "X-Goog-FieldMask": "displayName.text,formattedAddress,nationalPhoneNumber,websiteUri",
            }
            try:
                logging.info("Sending request to Google API for place details")
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    try:
                        try:
                            return_values["Name"].append(
                                standardizeName(response.json()["displayName"]["text"])
                            )
                        except KeyError:
                            logging.error(
                                "Could not find place details, no results returned"
                            )
                            return None
                        # Split the address into the different parts and then normalize them based on commas
                        address = response.json()["formattedAddress"].split(",")
                        return_values["Address"].append(
                            normalize_address_i18n(f"{address[0]}, {address[1]}}"
                                {
                                    "street_address": address[0],
                                    "city": address[1],
                                    "country_area": address[2].split(" ")[0],
                                    "postal_code": address[2].split(" ")[1],
                                }
                            )
                        )
                        try:
                            return_values["PhoneNumber"].append(
                                normalize_us_phone_number(
                                    response.json()["nationalPhoneNumber"]
                                )
                            )
                        except KeyError:
                            logging.info(
                                "Could not find phone details, no results returned"
                            )
                        try:
                            return_values["Website"].append(
                                normalize_url(response.json()["websiteUri"])
                            )
                        except KeyError:
                            logging.info(
                                "Could not find website details, no results returned"
                            )
                    except KeyError:
                        logging.error(
                            "Could not find place details, no results returned"
                        )
                        return None
                else:
                    logging.error(
                        f"Invalid request with response code {response.status_code}"
                    )
                    raise Exception(
                        f"Invalid request with response code {response.status_code}"
                    )
            except Exception as e:
                logging.error(f"Could not connect to Google API {e}")
                raise Exception(f"Could not connect to Google Places API {e}")

        return return_values


def google_validation(dataframe: pd.Series) -> pd.Series:
    """
    Takes in a Series and checks if the information is valid using the google places API

    :parameter: Series of the information

    :return: dataframe with the updated information
    """
    # Check to see if the series contains the information that is expected, if not return a error
    try:
        dataframe["Address"]
        dataframe["Phone"]
        dataframe["Website"]
        dataframe["BusinessName"]

    except KeyError:
        logging.error("Dataframe does not contain the correct information")
        raise Exception("Dataframe does not contain the correct information")

    # Create a google_maps object with the api_key
    google = google_maps(os.getenv("GOOGLE_API_KEY"))

    # Search list AKA what we're using to search for stuff, did SOS work?
    sos_worked = False
    business_name = "BusinessName"
    address = "Address"

    if dataframe["BusinessNameCorrect"]:
        sos_worked = True
        for name in dataframe["BusinessNameUpdate"]:
            if not pd.isna(name):
                business_name = "BusinessNameUpdate"

    if dataframe["AddressCorrect"]:
        sos_worked = True
        for address in dataframe["AddressUpdate"]:
            if not pd.isna(address):
                address = "AddressUpdate"

    if sos_worked:
        search_list = [business_name, address]
    else:
        search_list = ["Address", "Phone", "Website", "BusinessName"]

    success = False

    for search in search_list:
        # If the information was not found then it will search for the information using the google places API
        if pd.isna(dataframe[search]):
            continue
        else:
            logging.info(f"Searching for {search} using Google Places API")
            try:
                for record in dataframe[search]:
                    # Extra security check for pd.isna
                    if pd.isna(record):
                        continue
                    # Add Minnesota to the end of the record if it is a business name
                    if search == "BusinessName" or "BusinessNameUpdate":
                        record = record + " Minnesota"
                    #Actual code call  
                    info = google.details(record)

                    # Success check
                    if info:
                        success = True
                        break
                if success:
                    break
            except Exception as e:
                logging.error(f"Could not find {search} using Google Places API {e}")
                raise Exception(f"Could not find {search} using Google Places API {e}")

    # If it couldn't find anything on Google
    if not success:
        logging.info("Could not find any information using Google Places API")
        return dataframe

    # Checks to see if the BusinessNames match, if not update dataframe['BusinessName_Update'] to the new value, always update dataframe['BusinessName_Found'] to Google
    new_names = []
    update_names = False
    if not dataframe["BusinessNameCorrect"]:
        #Looks through the list of business names to see if any of them match
        for bname in dataframe["BusinessName"]:
            for newbname in info["Name"]:
                #If it straight up matches it shows here
                if bname == newbname:
                    dataframe["BusinessNameFound"] = "Google"
                    dataframe["BusinessNameCorrect"] = True
                    update_names = True
                    new_names.append(newbname)
                else:
                    # Do a normalization check to see if the names are similar enough
                    if is_same_business(bname, info["Name"]):
                        dataframe["BusinessNameFound"] = "Google"
                        dataframe["BusinessNameCorrect"] = True
                        dataframe["BusinessNameUpdate"] = info["Name"]
                    else:
                        dataframe["BusinessNameUpdate"] = info["Name"]
                        dataframe["BusinessNameFound"] = "Google"

    # Repat this process for address
    if not dataframe["Address_Found"]:
        if (
            dataframe["Address"]
            == f"{info['Address']['street_address']}, {info['Address']['city']}, {info['Address']['country_area']}"
        ):
            dataframe["Address_Found"] = "Google"
        else:
            dataframe[
                "Address_Update"
            ] = f"{info['Address']['street_address']}, {info['Address']['city']}, {info['Address']['country_area']}"
            dataframe["Address_Found"] = "Google"

    # Repat this process for phone
    if info["PhoneNumber"]:
        if dataframe["Phone"] == info["PhoneNumber"]:
            dataframe["Phone_Found"] = "Google"
        else:
            dataframe["Phone_Update"] = info["PhoneNumber"]
            dataframe["Phone_Found"] = "Google"

    # Repat this process for website
    if info["Website"]:
        if dataframe["Website"] == info["Website"]:
            dataframe["Website_Found"] = "Google"
        else:
            dataframe["Website_Update"] = info["Website"]
            dataframe["Website_Found"] = "Google"

    return dataframe
    # Return the dataframe with the updated information
