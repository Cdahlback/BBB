"""
Various Google Places tool utilizing Google Places API
"""
import os
import pandas as pd
import logging
from dotenv import load_dotenv
from pathlib import Path
import requests


ENV_PATH = str(Path(__file__).parent.parent.parent / ".env")
load_dotenv(dotenv_path=ENV_PATH)
# Setup logging to capture detailed logs about warnings, errors, and other critical information.
logging.basicConfig(filename="functions.log", level=logging.DEBUG)

class google_maps:
    """
    The class that will be used to interact with the Google Maps API
    """
    api_key = ""
    place_ids = []
    # Initialized our object the url and fields that will be used
    def __init__(self, api_key:str):
        """
        Initializes the class with the url and fields that will be used
        """
        self.api_key = api_key
    
    def find_place(self, input:str):
        """
        Finds the place based on the input and input_type and returns the fields that are specified
        
        :parameter input: The input that is being searched for such as the name of the business

        :parameter fields: The fields that are being returned from the API at the second level field and down

        :return: dictionary of the information that is returned from the API
        """
        url = 'https://places.googleapis.com/v1/places:searchText'

        headers = {
            'Context-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'places.id'
        }
        #Appends the first level field to the fields
        # field_str = ""
        # for field in fields:
        #     if field == "displayName":
        #         field_str = field_str + ",places.displayName.text"
        #     else:
        #         field_str = field_str + ",places." + field.strip()

        data = {
            'textQuery': input,
        }
        #Sends the request to the API and returns the json
        try:
            logging.info("Sending request to Google API for place_id")
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                self.place_ids =  response.json()['places'].values()
        except:
            logging.error("Could not connect to Google API")
            raise Exception("Could not connect to Google Places API")
        
    def find_details(self,input: str) -> dict:
        """
        Finds the details of the place based on the place_id and returns the fields that are specified

        :parameter input: The input that is being searched for such as the name of the business

        :parameter fields: The fields that are being returned from the API at the second level field and down
        """
        self.find_place(input)

        if not self.place_ids:
            logging.error("Could not find place_id")
            return None
    
url = 'https://places.googleapis.com/v1/places:searchText'

headers = {
    'Context-Type': 'application/json',
    'X-Goog-Api-Key': os.getenv("GOOGLE_API_KEY"),
    'X-Goog-FieldMask': 'places.id'
}
data= {
    'textQuery': 'Invalid request that wont work mankato minnesota',
}
print(requests.post(url, headers=headers, data=data).json())
try:
    gmaps = googlemaps.Client(key = os.getenv("GOOGLE_API_KEY"))
except:
    logging.error("Could not connect to Google API")
    raise Exception("Could not connect to Google Places API")


def find_place_by_exact_location(address:str) -> str:
    """
    Finds the location and returns place_id based on the known EXACT locaiton
    
    :parameter: address of the business
    
    :returns: place_id of the location for google
    """
    gmaps.find_place(input=address, input_type="textquery", fields=["place_id","photos","name"])

def find_places_by_name(name:str) -> str:
    """
    Using assumed name find the business by searching all of MN for it.
    
    :parameter:  name of the business
    
    :return: place_id of the assumed locaiton
    """
    gmaps.find_place(input=name, input_type="textquery", fields=["place_id"])


def find_place_details(place_id:str) -> dict:
    """
    Using the place_id find the details of the business

    :parameter: place_id of the business

    :return: dictionary of the details of the business
    """



def google_validation(dataframe:pd.Series) -> pd.Series:
    """
    Takes in a Series and checks if the information is valid using the google places API

    :parameter: Series of the information

    :return: dataframe with the updated information
    """
    #Check to see if the series contains the information that is expected, if not return a error
    try:
        dataframe["Address"]
        dataframe["City"]
        dataframe["State"]
        dataframe["Zip"]
    #Iterate over the dataframe for verified locations and use those to find the place_id
    except:
        logging.error("Dataframe does not contain the correct information")
        raise Exception("Dataframe does not contain the correct information")
    #Use that place_id to then find information on it and fill that out
    

    #Checks using the website for a valid email and if it is then it will update the dataframe with that information

    #If couldn't using the internal tool attempt to find email using the API and if it is then update the dataframe with that information

    #Repeat this process with checking for if name is verified using that and not repeating with any of the ones 
    #previously verified

    #

    #Return the dataframe with the updated information