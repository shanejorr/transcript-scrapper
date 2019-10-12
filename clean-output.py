"""
This file cleans the final output of the scrapped data
"""

import pandas as pd
import glob

# get list of all scrapped csv files
scrapped_output = glob.glob("transcript-scrapper/scrapper-output/*.csv")

# load all dataframes as a list
list_df = [pd.read_csv(f) for f in scrapped_output]

# combine into one dataset
df = pd.concat(list_df, ignore_index=True)

print(df.head())