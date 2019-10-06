#import PyPDF2
# import tabula as tb
#import re

# pdftotext


from PyPDF2 import PdfFileWriter,PdfFileReader,PdfFileMerger
import pdftotext
import re
import pandas as pd
import custom_functions as cf



transcript_dir = "transcript-scrapper/pdf-files/"
"""
writer = PdfFileWriter()
pdf_file = PdfFileReader(open(transcript_dir + 'transcripts09.pdf',"rb"))
page_right = pdf_file.getPage(0)


print(page_left.cropBox.getLowerLeft())
print(page_left.cropBox.getLowerRight())
print(page_left.cropBox.getUpperLeft())
print(page_left.cropBox.getUpperRight())
"""

"""
# left side of pdf
page_left.cropBox.setLowerLeft((0, 0))
page_left.cropBox.setUpperRight((612, 350))
writer.addPage(page_left)


page_right.cropBox.setLowerLeft((0, 350))
page_right.cropBox.setUpperRight((612, 792))
#writer.addPage(page_right)
print(list(page_right.pages))
#with open("out.pdf", "wb") as out_f:
#    writer.write(out_f)
"""

# regular expression to extract semester on left hand side

# Load your PDF
with open(transcript_dir + 'transcripts09.pdf', "rb") as f:
    pdf = pdftotext.PDF(f)

    name = re.search(r'Page: +\d +of +\d\n (.+?, \w+)?', pdf[0])

    left_semester = re.findall(r'\n +([A-Z][a-z]+ \d{4})',pdf[0])
    left_grades = re.findall(r'\nLAW +(\d+) +(.+?)  +?(\d)[.]\d\d +(.{1,2})', pdf[0])
    left_new_lines = re.findall(r'\nLAW|\n +Term', pdf[0])
    left_semesters = cf.left_classes_per_semester(left_new_lines, left_semester)
    
    left_df = pd.DataFrame(left_grades, columns=['class_num', 'class_name', 'credits', 'grade'])
    
    # name will be separated into first and last post-processing
    left_df['name'] = name.group(1)
    
    # semesters will be separated into semster and year post processing
    left_df['semester'] = left_semesters
    
    print(left_df)

    #right_new_lines = re.findall(r'\nLAW|\n +Term', pdf[0])
    #right_grades = re.findall(r' LAW +(\d+) +(.+?)  +?(\d)[.]\d\d +(.{1,2})\n', pdf[0])
    #right_semester = re.findall(r'\w +([A-Z][a-z]+ \d{4})\n',pdf[0])