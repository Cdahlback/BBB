# Tools-for-manual-checking folder

##Three files:
###1. Chromedriver

The chromedriver file supports the selenium 'webdriver' import within the manual_url_checking_helper.py file.
The chromedriver works by taking in a URL input, and automatically opening that website into chrome. In this case,
We use chromedriver to go through a list of URLs, and once we are finished marking a website for manually checking,
chromedriver will automatically go to the next URL within the list, and open that next website. This ultimately
saves us time when doing any manual checking.

###2. Manual_url_checking_helper.py

This script is used to help us scan through newly generated URLs faster in order to manually check them.
Manual checking consists of looking at a newly generated URL we got from either scraping emails or by the search method,
and seeing weather or not the URL is associated with the business that we were trying to scrape the new URL for.

### 3. Manually_check_scrapers.py

This script is used to verify the validity of our independent variable scrapers. If any changes were made to any
scraper, or a new one was built, this file can be used as additional testing for that scraper. Any new scraper that
needs to be tested will have to be added to the list of function calls within the 'print_info' function.