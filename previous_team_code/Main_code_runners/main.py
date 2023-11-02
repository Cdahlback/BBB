import glob

import pandas as pd
from Main_code_runners.main_machine_learning import main
from Main_code_runners.main_scrape_data import scrape_data_main
from Main_code_runners.main_url_scrape import main_scrape_urls

if __name__ == "__main__":
    df = pd.read_csv("../data/mn_bbb_businesses.csv", low_memory=False)
    # get the index of the last saved CSV file, or set to 0 if no files have been saved yet
    last_index = (
        int(
            pd.Series(glob.glob("stream_*.csv"))
            .apply(lambda x: x.split("_")[1].split(".")[0])
            .max()
        )
        + 1
        if glob.glob("stream_*.csv")
        else 0
    )
    for i in range(last_index * 500, len(df), 500):
        batch = df.iloc[i : i + 500]
        batch_copy = batch.copy(deep=True)
        print("Scraping for new urls")
        batch = main_scrape_urls(batch)
        print("Scraping for new data")
        batch = scrape_data_main(batch)
        print("Preforming predictions")
        stream = main(batch, batch_copy)
        # save the current state of the dataframe to a csv file
        stream.to_csv(f"stream_{i // 500}.csv")
