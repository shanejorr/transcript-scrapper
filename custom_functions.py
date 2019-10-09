import re
import os
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
        
def extract_grades(input_file, left_side):
    
    """
    Extract the grades from a single side of a pdf page
    input_file: pdf file to input (side of a full pdf file)
    left_side: boolean, whether it is the left side of the file, which contains the name;
                if True, name will be added to data frame
                
    return: dataframe of grades
    """
    
    # Load your PDF
    with open(input_file, "rb") as f:
        
        pdf = pdftotext.PDF(f)
    
        semester = re.findall(r'\n +([A-Z][a-z]+ \d{4}|Transfer Work)',pdf[0])
        grades = re.findall(r'\n {0,1}LAW +(\w{3}) +' # class number
                            r'(.+?) +?' # class name
                            r'(\d{1,2})[.]\d\d' # number of credit hours
                            r'(.*)', # class letter grade 
                            pdf[0])
        new_lines = re.findall(r'\n {0,1}LAW|\n +Term|\n *---', pdf[0])
        semesters = left_classes_per_semester(new_lines, semester)
        
        df = pd.DataFrame(grades, columns=['class_num', 'class_name', 'credits', 'grade'])

        # some classes don't have semesters (law review / moot court)
        # add 'no semester' value to end of semester list for the difference
        # in length between the number of total classes in the dataframe 
        # and number of semester classes, if the two are different
        if len(df) != len(semesters):

            # calculate the number of no semester classes
            num_no_semester = len(df) - len(semesters)
            
            # create list with phrase 'no semester' for this length
            no_semester = ['no semester'] * num_no_semester

            # add this list to the end of the semeter list
            semesters.extend(no_semester)
        
        # semesters will be separated into semster and year post processing
        df['semester'] = semesters
        
        # the left side includes the name, so if we are scraping the right side
        # pull the name and include it in the dataframe
        if left_side:
            
            name = re.search(r' \d{4}\n +(.+?, \w+)', pdf[0])
 
            # name will be separated into first and last post-processing
            df['name'] = name.group(1)
        
    return df
    
def extract_whole_page(input_file, page_num, cropped_dir):
    
    # split pdf into right and left sectins and output results
    cut_pdf(input_file, (0, 0), (612, 350), 
            page_num, cropped_dir + "outL.pdf")   
    cut_pdf(input_file, (0, 350), (612, 792), 
            page_num, cropped_dir + "outR.pdf")    
    
    # read in right and left sections, extract text, and form into a dataframe
    dfR = extract_grades(cropped_dir + "outL.pdf", True)
    dfL = extract_grades(cropped_dir + "outR.pdf", False)
    
    # combine right and left dataframes
    df = pd.concat([dfR, dfL], axis=0).reset_index(drop=True)
    
    # pdfs from the left side will not have names, there value will be missing in the df
    # forward fill missing name values
    df['name'] = df['name'].fillna(method='ffill')
    
    # remove left and right cropped pdf files
    for file in ["outR.pdf", "outL.pdf"]:
        os.remove(cropped_dir + file)
    
    return df