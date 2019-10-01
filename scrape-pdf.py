#import PyPDF2
# import tabula as tb
#import re

# pdftotext
 
import pdftotext
import re

transcript_dir = "transcript-scrapper/pdf-files/"
# 'Page: \d of \d\n (.+?), (\w+)?'

# regular expression to extract semester on left hand side

# Load your PDF
with open(transcript_dir + 'transcripts09.pdf', "rb") as f:
    pdf = pdftotext.PDF(f)

    name = re.search(r'Page: +\d +of +\d\n (.+?), (\w+)?', pdf[0]).group(0)

    left_semester = re.findall(r'\n +([A-Z][a-z]+ \d{4})', pdf[0])
    left_grades = re.findall(r'\nLAW +(\d+) +([\w| ]+)  +?(\d)[.]\d\d +(.{1,2})', pdf[0])
    left_new_lines = re.findall(r'\nLAW|\n +Term', pdf[0])
    right_new_lines = re.findall(r'\nLAW|\n +Term', pdf[0])
    
    
    print(left_new_lines)

# How many pages?
# print(len(pdf))

# Iterate over all the pages
# for page in pdf:
#     print(page)

# Read some individual pages

#print(repr(pdf[0]))
# print(pdf[1])

# Read all the text into one string
#print("".join(pdf[0]))

# ---------------------------------



# transcript_dir = "transcript-scrapper/pdf-files/"

# left_column = [62.865, 47.025, 518.265, 351.945]
# right_column = [62.865, 855.521, 518.265, 653.895]

# full_area = [0,792,612,0]

# left_pdf = tb.read_pdf(transcript_dir + 'transcripts17.pdf', area = right_column, 
#                       guess = False, stream = True,
#                       pages = 1)
                       
# print(left_pdf)

# -----------------------------------------------


# # pdf file object
# pdfFileObj = open(transcript_dir + 'transcripts09.pdf', 'rb')

# # pdf reader object
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# # number of pages in pdf
# #print(pdfReader.numPages)

# # a page object
# pageObj = pdfReader.getPage(19)

# # extracting text from page.
# # this will print the text you can also save that into String

# text = pageObj.extractText()

# # remove excess whitespace (only keep one sapce)
# text = " ".join(text.split())

# # extract name
# name = re.search(r'Page: \d of \d (.+?), (\w+)?', text)

# #print(text)
# print(name.group(1))
# print(name.group(2))