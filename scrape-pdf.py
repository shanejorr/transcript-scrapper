import re
import pandas as pd
import custom_functions as cf

transcript_dir = "transcript-scrapper/pdf-files/"
cropped_dir = "transcript-scrapper/cropped_pdf/"

# split pdf into right and left sectins and output results
cf.cut_pdf(transcript_dir + 'transcripts09.pdf', (0, 0), (612, 350), 
           0, cropped_dir + "outR.pdf")   
cf.cut_pdf(transcript_dir + 'transcripts09.pdf', (0, 350), (612, 792), 
           0, cropped_dir + "outL.pdf")    

# read in right and left sections, extract text, and form into a dataframe
dfR = cf.extract_grades(cropped_dir + "outR.pdf", True)
dfL = cf.extract_grades(cropped_dir + "outL.pdf", False)

# combine right and left dataframes
df = pd.concat([dfR, dfL], axis=0).reset_index(drop=True)

# pdfs from the left side will not have names, there value will be missing in the df
# forward fill missing name values
df['name'] = df['name'].fillna(method='ffill')

print(df)

