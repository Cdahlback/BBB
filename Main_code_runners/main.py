from Main_code_runners.main_machine_learning import main_ml
from Main_code_runners.main_url_scrape import main_scrape_urls
from Main_code_runners.main_scrape_data import scrape_data_main
import pandas as pd


if __name__ == "__main__":
    df = pd.read_csv("../data/mn_bbb_businesses.csv", low_memory=False)
    main_scrape_urls(df)
    scrape_data_main(df)
    main_ml(df)

