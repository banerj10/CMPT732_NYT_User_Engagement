All files related to implementing the project can be found under the Code
directory. The entire project has been implemented in Python.

1) Download the repository and navigate to the Code directory under the
   root of the repo.

2) Create a new virtual environment named env using the command 
   python -v venv env. Activate the environment using the command
   source ./env/bin/activate.

3) The requirements.txt file lists all the packages requirements and 
   dependencies for running the project. These can be installed using
   pip install -r requirements.txt.

4) There are three directories, each categorised by their function. No
   arguments are required for running any of the scripts within these
   directories.

5) Set up an AWSCLI in the local machine. Instructions can be found at
   https://docs.aws.amazon.com/cli/index.html. 

6) To give your python environment access to AWS S3, you need to have 
   access keys, which can be found in the administrative security
   settings of your AWS acccount. Instructions can be found in the AWS 
   user guide.
   
7) Navigate to the Data_Collection directory and run dumper.py, followed
   scraper.py. The scraper code requires at least 10 NYT API keys to run,
   and will take around 4 days to run. If this is not desired, sample data
   has been provided in the Sample_Data subdirectory. The architecture for
   the article/comment data can be found in our public bucket at
   https://s3.console.aws.amazon.com/s3/buckets/dataknyts-nyt-dump?region=us-west-2
   (you will need to be loggin in to your AWS account).

8) Navigate to the ETL directory and run etl.py using spark-submit. Before 
   running, please add your AWS access key and secret key in the location
   specified in the code. Please change the bucket name accordingly.

9) Navigate to the Visualization directory and run app.py. This requires
   s3connector.py to have the AWS access keys mentioned in step (7).
