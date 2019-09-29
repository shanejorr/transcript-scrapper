import PyPDF2
import tabula as tb
import re

transcript_dir = "transcript-scrapper/pdf-files/"

left_column = [62.865, 47.025, 518.265, 351.945]
right_column = [62.865, 855.521, 518.265, 653.895]

full_area = [0,792,612,0]

left_pdf = tb.read_pdf(transcript_dir + 'transcripts09.pdf', area = left_column, 
                       guess = False, stream = True,
                       pages = 1)
                       
print(left_pdf)


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