import boto3
import sys
import os
import pandas as pd
import io

access_id = ""#ADD YOUR OWN ACCESS KEY
access_key = ""#ADD YOUR OWN SECRET KEY

s3_client =boto3.client('s3')
s3_bucket_name='dataknyts-nyt-dump'
s3 = boto3.resource('s3',
                    aws_access_key_id= access_id,
                    aws_secret_access_key=access_key)
bucket = s3.Bucket(s3_bucket_name)

#print(bucket.objects)
def read_file(s3_bucket_name,file_path):
    obj = s3.Object(s3_bucket_name,file_path)
    data=obj.get()['Body'].read()
    return pd.read_csv(io.BytesIO(data), header=0, delimiter=",", low_memory=False)

def load_objects():
    files_dict = {}
    for x in bucket.objects.filter(Prefix = 'graph/'):#section_name_count/5/part-00000-007a5986-e51d-4b26-b7f1-d5397a583bf3-c000.csv'):
        if ".csv" in x.key:
            splits = x.key.split("/")
            key = splits[1]
            if files_dict.get(key) == None:
                files_dict[key] = {}
            if key == 'emotions':
                files_dict[key] = read_file(s3_bucket_name,x.key)
            else:
                files_dict[key][splits[2]] = read_file(s3_bucket_name,x.key)
    return files_dict

