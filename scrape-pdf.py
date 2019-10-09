import re
import pandas as pd
import custom_functions as cf
import glob
import pdftotext

transcript_dir = "transcript-scrapper/pdf-files/"
cropped_dir = "transcript-scrapper/cropped_pdf/"
scrapper_dir = "transcript-scrapper/scrapper-output/"

# keep transcript files to iterate through
transcript_files = glob.glob(transcript_dir + "*.pdf")

#with open(transcript_files[2], "rb") as f:
#    pdf = pdftotext.PDF(f)
#cf.cut_pdf(transcript_files[2], (0, 0), (612, 350), 64, cropped_dir + "outL.pdf")
#sem = cf.extract_grades(cropped_dir + "outL.pdf", True)

#print(sem)

#with open(transcript_dir + "outL.pdf", "rb") as f:
#    pdf = pdftotext.PDF(f)
#    print(repr(pdf[0]))



# iterate over each yearly transcript file
for file in transcript_files:
    
    # initialize dataframe to store multiple pages
    multi_page = pd.DataFrame()
           
    # find out how many pages are in the file, so we know how many to iterate through
    with open(file, "rb") as f:
        pdf = pdftotext.PDF(f)

    # iterate through each page
    for page in range(len(pdf)):
           
        # extracting text from single page
        single_page = cf.extract_whole_page(file, page, cropped_dir)
          
        # combine data frame of grades from single student with master 
        # data frame from whole class
        multi_page = pd.concat([multi_page, single_page])

        print(file)
        print(single_page)
          
    # after extracting all pages from class do the following:
    # 1: add class year to data frame
    # save dataframe fof class year's grades as csv file
    
    # find class year by extracting two digit year from file name
    year = re.search(r'[0-9][0-9]', file).group(0)
    
    # add class year as column to data frame
    multi_page['class_year'] = 2000 + int(year)
    
    # write out dataframe
    scrapper_file = scrapper_dir + "scrapper_output" + year + ".csv"
    
    multi_page.to_csv(scrapper_file)