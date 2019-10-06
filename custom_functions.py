import re
from PyPDF2 import PdfFileWriter,PdfFileReader
import pdftotext
import pandas as pd

def left_classes_per_semester(left_new_lines, left_semester):
    """
    This function stores a string of the semeters name, with the number of times
    the string is stored equaling the number of classes the student took in the
    semester.  The output will then be added to a datafram column to signify
    the semester of the class.
    """
    
    i = 0  # initialize iterator for all lines
    semesters = [] # initialize list to store strins of semesters
    # initialize dictionary with key of semester name / value of number of classes
    semester_counts = {} 
    
    # iterate through each semester
    for semester in left_semester:
        # iterate through each line and check to see if the line has a class
        # if the line has a class, add the semester name to the semester list
        # and move to the next line
        while re.match(r"\n {0,1}LAW", left_new_lines[i]):
            semesters.append(semester)
            i += 1
        # we're at this point if the line did not have a class
        # we need to add a number to the line iterator so it skips the line without
        # a class
        i += 1
        
    return semesters
    
def cut_pdf(file_input, crop_lowerLeft, crop_lowerRight, page_num, file_output):
    """
    This function cuts the transcripts in the middle.
    
    File Input: file name of transcripts
    crop_lowerLeft: lower left coordinate in points of new boundary
    crop_lowerLeft: lower right coordinate in points of new boundary
    page_num: page number within pdf
    file_output: pdf file name of output file
    """
    
    # read in pdf file
    writer = PdfFileWriter()
    pdf_file = PdfFileReader(open(file_input,"rb"))
    page = pdf_file.getPage(page_num)
    
    # crop file
    page.cropBox.setLowerLeft(crop_lowerLeft)
    page.cropBox.setUpperRight(crop_lowerRight)
    
    # add cropped file to writer object
    writer.addPage(page)
    
    # write out file
    with open(file_output, "wb") as out_f:
        writer.write(out_f)
        
def extract_grades(input_file, right_side):
    
    # Load your PDF
    with open(input_file, "rb") as f:
        
        pdf = pdftotext.PDF(f)
    
        semester = re.findall(r'\n +([A-Z][a-z]+ \d{4})',pdf[0])
        grades = re.findall(r'\n {0,1}LAW +(\d+) +(.+?)  +?(\d)[.]\d\d +(.{1,2})', pdf[0])
        new_lines = re.findall(r'\n {0,1}LAW|\n +Term', pdf[0])
        semesters = left_classes_per_semester(new_lines, semester)
        
        df = pd.DataFrame(grades, columns=['class_num', 'class_name', 'credits', 'grade'])
  
        # semesters will be separated into semster and year post processing
        df['semester'] = semesters
        
        # the right side includes the name, so if we are scraping the right side
        # pull the name and include it in the dataframe
        if right_side:
            
            name = re.search(r' \d{4}\n +(.+?, \w+)', pdf[0])
 
            # name will be separated into first and last post-processing
            df['name'] = name.group(1)
        
    return df