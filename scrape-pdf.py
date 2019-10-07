import re
import pandas as pd
import custom_functions as cf
import glob
import pdftotext

transcript_dir = "transcript-scrapper/pdf-files/"
cropped_dir = "transcript-scrapper/cropped_pdf/"

# keep transcript files to iterate through
transcript_files = glob.glob(transcript_dir + "*.pdf")
"""
#with open(transcript_files[0], "rb") as f:
#    pdf = pdftotext.PDF(f)
cf.cut_pdf(transcript_files[0], (0, 350), (612, 792), 7, transcript_dir + "outL.pdf")
sem = cf.extract_grades(cropped_dir + "outL.pdf", False)

print(sem)
"""
#with open(transcript_dir + "outL.pdf", "rb") as f:
#    pdf = pdftotext.PDF(f)
#    print(repr(pdf[0]))

# iterate over each yearly transcript file
for file in transcript_files:
           
    # find out how many pages are in the file, so we know how many to iterate through
    with open(file, "rb") as f:
           pdf = pdftotext.PDF(f)

    for page in range(len(pdf)):
           print(page)
           
           # iterate through each page, extracting text from single page
           single_page = cf.extract_whole_page(transcript_dir + 'transcripts09.pdf', 
                                               page, cropped_dir)

           print(single_page)