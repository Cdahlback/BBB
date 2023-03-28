tools-for-manual-checking folder

two files:
1. chromedriver
2. manual_url_checking_helper.py

The chromedriver file supports the selenium 'webdriver' import within the manual_url_checking_helper.py file.
The chromedriver works by taking in a URL input, and automatically opening that website into chrome. In this case,
We use chromedriver to go through a list of URLs, and once we are finished marking a website for manually checking,
chromedriver will automatically go to the next URL within the list, and open that next website. This ultimately
saves us time when doing any manual checking.

manual_url_checking_helper.py is the main file to run within this folder. We use this script to help us scan
through newly generated URLs faster in order to manually check them. Manual checking consists of looking at a
newly generated URL we got from either scraping emails or by the search method, and seeing weather or not
the URL is associated with the business that we were trying to scrape the new URL for.

manual_url_checking_helper.py starts by reading the input csv file and setting a counter. This counter
keeps track of where in the dataset the checking loop is at. A while loop then starts and goes through
each row of the dataset, where the url is pulled and put into the chromedriver for manual checking. We originally
set the while loop to break once counter exceeds 400. This is because each of us were tasked with manually checking
400 rows within the dataset for our test/training set for the machine learning model. The user can then input a '1' in
the terminal if the website pulled up from the URL is associated with the business the URL was scraped from,
or '0' if not. After an input is received, the current dataset is updated with a new column named 'manually_checked'.
This column is where the '1' or '0' is stored. Once all rows have been checked or when the counter exceeds
the limit set on the loop, the loop breaks and what is left is the updated dataset.