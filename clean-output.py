"""
This file cleans the final output of the scrapped data
"""

import pandas as pd
import numpy as np
import glob
import boto3

output_dir = "transcript-scrapper/scrapper-output/"

# get list of all scrapped csv files
scrapped_output = glob.glob(output_dir + "*.csv")

# load all dataframes as a list
list_df = [pd.read_csv(f) for f in scrapped_output]

# combine into one dataset
df = pd.concat(list_df, ignore_index=True)

# break up name into first and last name
df[['name_last', 'name_first']] = df['name'].str.split(', ', expand=True)
df.drop("name", axis=1, inplace=True)

# strip leading and trailing whitespace from grade
df['grade'] = df['grade'].str.strip()

# convert letter grade into numeric grade

# create mapping of letter and numeric grades for pre-2013 and 2013 and later
pre_mapping = { "A+": 4.30,
                "A": 4.15,
                "A-": 3.85,
                "B+": 3.55,
                "B": 3.25,
                "B-": 2.95,
                "C+": 2.65,
                "C": 2.35,
                "C-": 2.05,
                "D+": 1.75,
                "D": 1.45,
                "D-": 1.15,
                "F+": 0.85,
                "F": 0.30 }
                
post_mapping = {"A+": 4.33,
                "A": 4.00,
                "A-": 3.67,
                "B+": 3.33,
                "B": 3.00,
                "B-": 2.67,
                "C+": 2.33,
                "C": 2.00,
                "C-": 1.67,
                "D+": 1.33,
                "D": 1.00,
                "D-": 0.67,
                "F": 0.00}
                
# map letter grades to numbers
df['grade_number'] = np.where(df['class_year'] < 2013, df['grade'].map(pre_mapping), df['grade'].map(post_mapping))

file_output = output_dir + "cleaned_transcript.csv"

df.to_csv(file_output, index=False)

# send raw csv file to s3 bucket
s3 = boto3.client('s3')
with open(file_output, "rb") as f:
    s3.upload_fileobj(f, "elon-transcripts", "cleaned_transcript.csv")






