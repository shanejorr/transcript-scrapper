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

# break up name into first and last name
df[['name_last', 'name_first']] = df['name'].str.split(', ', expand=True)
df.drop("name", axis=1, inplace=True)

print(df.head())

