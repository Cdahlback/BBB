from Main_code_runners.main_machine_learning import main
from Main_code_runners.main_url_scrape import main_scrape_urls
from Main_code_runners.main_scrape_data import scrape_data_main
import pandas as pd


if __name__ == "__main__":
    df = pd.read_csv("../data/mn_bbb_businesses.csv", low_memory=False)
    df = df.sample(10)
    df_copy = df.copy(deep=True)
    df = main_scrape_urls(df)
    df = scrape_data_main(df)
    stream = main(df, df_copy)
    print(stream.head())
