"""
Various Google Places tool utilizing Google Places API
"""
import os
import pandas as pd
import googlemaps
import logging
from dotenv import load_dotenv
from pathlib import Path
import requests

URL = 'https://places.googleapis.com/v1/places:searchText'

ENV_PATH = str(Path(__file__).parent.parent.parent / ".env")
load_dotenv(dotenv_path=ENV_PATH)
# Setup logging to capture detailed logs about warnings, errors, and other critical information.
logging.basicConfig(filename="functions.log", level=logging.DEBUG)

class new_GoogleMaps:
    """
    The class that will be used to interact with the Google Maps API
    """
    url = ''
    fields = 'places.id'
    headers = {
        'Context-Type': 'application/json',
        'X-Goog-Api-Key': os.getenv("GOOGLE_API_KEY"),
        'X-Goog-FieldMask': fields
    }
    def __init__(self, url:str, fields:str):
        """
        Initializes the class with the url and fields that will be used
        """
        self.url = url
        self.fields = fields

headers = {
    'Context-Type': 'application/json',
    'X-Goog-Api-Key': os.getenv("GOOGLE_API_KEY"),
    'X-Goog-FieldMask': 'places.displayName,places.id'
}
data= {
    'textQuery': 'River Rock Coffee, Mankato MN',
}
print(requests.post(URL, headers=headers, data=data).json())
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