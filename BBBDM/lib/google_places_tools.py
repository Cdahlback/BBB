"""
Various Google Places tool utilizing Google Places API
"""
import logging
import os

import pandas as pd
import numpy as np
import requests
from lib.data_processing import is_same_business
from lib.Normalizing import (
    normalize_address_i18n,
    normalize_url,
    normalize_us_phone_number,
    standardizeName,
)
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = str(Path(__file__).parent.parent.parent / ".env")
load_dotenv(dotenv_path=ENV_PATH)
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
        self.url = "https://places.googleapis.com/v1/places:searchText"

        self.headers = {
            "Context-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "places.id",
        }

        self.data = {
            "textQuery": input,
        }
        # Sends the request to the API and returns the json
        try:
            logging.info("Sending request to Google API for place_id")
            response = requests.post(self.url, headers=self.headers, data=self.data)
            if response.status_code == 200:
                try:
                    json_value = response.json()
                    for place in json_value["places"]:
                        self.place_ids.append(place["id"])

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
                            normalize_address_i18n(f"{address[0]},{address[1]},{address[2].split(' ')[-1]}")
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


def google_validation(dataframe: pd.DataFrame) -> pd.DataFrame:
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
        search_list = ["BusinessName", "Address", "Phone", "Website"]

    success = False

    for search in search_list:
        # If the information was not found then it will search for the information using the google places API
        if pd.isna(dataframe[search][0]):
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

    #Remove duplicates from the rows
    dataframe = dataframe.applymap(lambda x: [i for n, i in enumerate(x) if i not in x[:n]] if isinstance(x, list) else x)
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
                        update_names = True
                        new_names.append(newbname)
                    else:
                        # If it doesn't match then we update the dataframe
                        update_names = True
                        new_names.append(bname)
                        dataframe["BusinessNameFound"] = "Google"

    if update_names:
        dataframe["BusinessNameUpdate"] = new_names

    # Repat this process for address
    new_addresses = []
    update_addresses = False
    if not dataframe["AddressCorrect"]:
        for baddress in dataframe["Address"]:
            for newbaddress in info["Address"]:
                if (baddress == newbaddress):
                    dataframe["AddressFound"] = "Google"
                    dataframe["AddressCorrect"] = True
                    update_addresses = True
                    new_addresses.append(newbaddress)
                else:
                    update_addresses = True
                    new_addresses.append(baddress)
                    dataframe["AddressFound"] = "Google"

    if update_addresses:
        dataframe["AddressUpdate"] = new_addresses

    # Repat this process for phone
    new_phones = []
    update_phones = False
    for phone in dataframe["Phone"]:
        for newphone in info["PhoneNumber"]:
            if phone == newphone:
                dataframe["PhoneFound"] = "Google"
                dataframe["PhoneCorrect"] = True
                update_phones = True
                new_phones.append(phone)
            else:
                update_phones = True
                new_phones.append(phone)
                dataframe["PhoneFound"] = "Google"

    if update_phones:
        dataframe["PhoneUpdate"] = new_phones

    # Repat this process for website
    new_websites = []
    update_websites = False
    for website in dataframe["Website"]:
        for newwebsite in info["Website"]:
            if website == newwebsite:
                dataframe["WebsiteCorrect"] = True
                dataframe["WebsiteFound"] = "Google"
                new_websites.append(website)
                update_websites = True
            else:
                update_websites = True
                new_websites.append(website)
                dataframe["WebsiteFound"] = "Google"
                update_websites = True

    if update_websites:
        dataframe["WebsiteUpdate"] = new_websites
    #Just incase we need to use this again
    google_maps.place_ids = []

    return dataframe
    # Return the dataframe with the updated information


if __name__ == "__main__":
    sos_output = pd.DataFrame({
        "firm_id": [2, 5, 7, 9, 10],
        "BusinessName": [["able fence, inc."], ["albin endeavor inc.", "albin funeral chapel inc", "albin chapel"],
                         ["albrecht company", "albrecht enterprises llc"],
                         ["arthur williams opticians","arthur williams optical inc"],
                         ["able moving and storage snc","able movers llc"]],
        "BusinessNameUpdate": [["Able Fence, Inc."], [np.nan], ["Albrecht Enterprises, LLC"], [np.nan], [np.nan]],
        "BusinessNameCorrect": [True, False, True, False, False],
        "BusinessNameFound": ["SOS", np.nan, "SOS", np.nan, np.nan],
        "Phone": [["+1 651-222-4355"], ["+1 612-270-0491","+1 612-871-1418","+1 952-914-9410"],["+1 651-633-4510"],
                  ["+1 763-224-2883","+1 651-645-1976","+1 651-224-2883"],["+1 952-935-0331","+1 612-991-3264"]],
        "PhoneUpdate": [[np.nan], [np.nan], [np.nan], [np.nan], [np.nan]],
        "PhoneCorrect": [False, False, False, False, False],
        "PhoneFound": [np.nan, np.nan, np.nan, np.nan, np.nan],
        "Website": [[np.nan],["http://www.albinchapel.com/"],[np.nan],["http://www.arthurwilliamsoptical.com/"],
                    ["http://www.ablemovers.net"]],
        "WebsiteUpdate": [[np.nan], [np.nan], [np.nan], [np.nan], [np.nan]],
        "WebsiteCorrect": [False, False, False, False, False],
        "WebsiteFound": [np.nan, np.nan, np.nan, np.nan, np.nan],
        "Email": [[np.nan],["office@albinchapel.com","jimalbinson@gmail.com"],
                  ["edward@albrechtcompany.com","mail@albrechtcompany.com"],["arthurwilliamsoptical@gmail.com"],
                  ["ablemovers@izoom.net"]],
        "EmailUpdate": [[np.nan], [np.nan], [np.nan], [np.nan], [np.nan]],
        "EmailCorrect": [False, False, False, False, False],
        "EmailFound": [np.nan, np.nan, np.nan, np.nan, np.nan],
        "City": [["Saint Paul"],["Wayzata","Eden Prairie","Minneapolis"],["Roseville"],
                 ["Saint Paul"],["Minnetonka","Elk River"]],
        "Zip Code": [["55117"], ["55404", "55391", "55344"], ["55113"], ["55102", "55116"], ["55345", "55330"]],
        "ZipUpdate": [["55117"], [np.nan], ["55113"], [np.nan], [np.nan]],
        "ZipCorrect": [True, False, True, False, False],
        "ZipFound": ["SOS", np.nan, "SOS", np.nan, np.nan],
        "Address": [["78 Acker St E ,saint paul,55117"],
                ["PO Box 46147 ,eden prairie,55344","2200 Nicollet Ave ,minneapolis,55404","6855 Rowland Rd ,eden prairie,55344","2024 Blackberry Ln ,wayzata,55391"],
                ["1408 County Road C W ,roseville,55113"],
                ["366 Saint Peter St ,saint paul,55102","772 Cleveland Ave S ,saint paul,55116"],
                ["14601 Spring Lake Rd ,minnetonka,55345","12285 Rush Cir NW ,elk river,55330"]],
        "AddressUpdate": [["78 Acker Str E, St Paul, 55117"], [np.nan], ["1408 W Co Rd C, Roseville, 55113"], [np.nan], [np.nan]],
        "AddressCorrect": [True, False, True, False, False],
        "AddressFound": ["SOS", np.nan, "SOS", np.nan, np.nan],
    })
    newoutput = sos_output.apply(google_validation, axis=1)

    print(newoutput.head())