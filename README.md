
# BBBDM #


Better Business Bureau Data Management (BBBDM) is a tool designed by the Data Defenders team to help the Better Business Bureau (BBB) maintain and update their business data. The focus of this tool is to go over existing data and determine the continued validity of it through the output of a .csv file containing information about secondary sources that contain the same or new information. Alongside that it keeps track of new business filings based on the information given.


### What is this repository for? ###

* The goal of this repo is the collection of scripts to run the main function, alongside that it currently provides the file location to download additional data to be used with.
* 0.8.5

### How do I get set up? ###

!Note this information will be updated!

* Download the project or clone to your local machine
* Replace files located in BBBDM/Data with files of the same name but updated information
* Utilizing python=<3.9 download pip dependencies via –r requirements.txt
* Tests can be run by running pytest –v in the BBBDM/test folder
* Run the main file located in BBBDM/main.py to start

### What to do when an API token (Google, Yellow Pages) expires?
##### Google Places API token
* Open the below link and follow the steps
  * https://developers.google.com/maps/documentation/places/web-service/get-api-key
  * Ensure you do this with the correct account which has a billing account set up
  * In the .env file, update the GOOGLE_PLACES_TOKEN with the new value
 
##### Yellow Pages API token
* Open th below link and click "add token"
  * https://console.apify.com/account/integrations
  * This can be done with any account.
  * In the .env file, update the YELLOW_PAGES_TOKEn with the new value


### Useful commands 

* pdoc BBBDM:
  * Must be located in BBB folder
  * (What it does)
* coverage html
  * Must be located in BBBDM folder
  * (What it does)
* pre-commit run --all-files
  * Must be located in BBBDM folder
  * (What it does)
* pytest
  * Must be in the BBBDM folder
  * (What it does)

### Who do I talk to? ###

* BBBDM – Data Defenders
* Collin Dahlback – collin.dahlback@mnsu.edu
* Christopher Maher – christopher.maher.2@mnsu.edu
* Rania Anjorin     - raniaaweni.anjorin@mnsu.edu
* Tebibu Kebede     - tebibu.kebede@mnsu.edu 

