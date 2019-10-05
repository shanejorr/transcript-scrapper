#import PyPDF2
# import tabula as tb
#import re

# pdftotext
 
import pdftotext
import re
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
        while re.match(r"\nLAW", left_new_lines[i]):
            semesters.append(semester)
            i += 1
        # we're at this point if the line did not have a class
        # we need to add a number to the line iterator so it skips the line without
        # a class
        i += 1
        
    return semesters

transcript_dir = "transcript-scrapper/pdf-files/"

# regular expression to extract semester on left hand side

# Load your PDF
with open(transcript_dir + 'transcripts09.pdf', "rb") as f:
    pdf = pdftotext.PDF(f)

    name = re.search(r'Page: +\d +of +\d\n (.+?), (\w+)?', pdf[0])

    left_semester = re.findall(r'\n +([A-Z][a-z]+ \d{4})',pdf[0])
    left_grades = re.findall(r'\nLAW +(\d+) +(.+?)  +?(\d)[.]\d\d +(.{1,2})', pdf[0])
    left_new_lines = re.findall(r'\nLAW|\n +Term', pdf[0])
    right_new_lines = re.findall(r'\nLAW|\n +Term', pdf[0])
    #a = re.findall(r'\nLAW +(\d+) +([\w| ]+)  +?(\d)', pdf[0])
    
    semesters = left_classes_per_semester(left_new_lines, left_semester)
    
    df = pd.DataFrame(left_grades, columns=['class_num', 'class_name', 'credits', 'grade'])
    
    df['name_last'] = name.group(1)
    df['name_first'] = name.group(2)
    df['semester'] = semesters
    
    print(df)
    
    #print(semesters)