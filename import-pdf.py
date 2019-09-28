"""
This script imports all the pdf transcripts from an Amazon s3 bucket.
"""

import boto3
import os

bucket_name = 'elon-transcripts'

s3 = boto3.client('s3')

# pull all information from buckets
bucket_files = s3.list_objects_v2(Bucket=bucket_name)['Contents']

# extract only object names from buckets (example: transcript09.pdf)
# this name will be used to pull the pdf and save as the file name
bucket_objects = [x['Key'] for x in bucket_files]

# import all transcripts from s3
for obj_name in bucket_objects:
    # create file name to save on local computer that is combination of 
    # full file path and objec name
    file = "transcript-scrapper/pdf-files/" + obj_name
    # download file
    s3.download_file(bucket_name, obj_name, file)