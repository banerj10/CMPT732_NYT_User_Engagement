from os import walk
import os
import boto3
import json
import time

session = boto3.Session()
s3 = boto3.resource('s3')

def read_filename_articles():
    f = []
    for (dirpath, dirnames, filenames) in walk('./articles'):
        f.extend(filenames)
        break
    return f

def read_filename_comments():
    f = []
    for (dirpath, dirnames, filenames) in walk('./comments'):
        f.extend(filenames)
        break
    return f

def s3_dump(directory_name,folder_name):
    
    global s3
    for directory_names in directory_name: 
        data = open('./'+folder_name+ '/'+str(directory_names), 'rb')
        s3.Bucket('dataknyts-nyt-dump').put_object(Key=folder_name+"/"+directory_names, Body=data)
        data.close()
        os.remove('./'+folder_name+'/'+str(directory_names))
    
while(True):
    print("Reading articles")
    directory_name = read_filename_articles()

    if len(directory_name) != 0:
        s3_dump(directory_name,'articles')
    else:
        print("Articles directory empty")

    print("Reading Comments")
    directory_name = read_filename_comments()
    
    if len(directory_name) != 0:
        s3_dump(directory_name,'comments')
    else:
        print("Comments directory empty")

    time.sleep(100)