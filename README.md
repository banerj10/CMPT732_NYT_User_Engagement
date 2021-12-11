## Overview

This project was done for SFU's CMPT 732 (Big Data I) course, with the goal of analyzing reader engagement for articles published in the New York Times (NYT). This was achieved by using NYT article and comment metadata for the years 2017-2021 to create visualizations to depict metrics and trends related to user engagement. 

[The visualizations can be seen here](https://dataknyts-nyt.herokuapp.com/).

Notes on how to run the code can be found in RUNNING.md, and a more detailed overview can be found in the project report (under Documents).

## Structure

```
.
|-- Code
    |--Data Collection
        |-- Sample_Data
            |-- d579c8_comments_2020_7.json
            |-- dc8751_articles_2020_7.json
        |-- dumper.py
        |-- keys.txt
        |-- scraper.py
    |--ETL
        |-- etl.py
        |-- location_csv.csv
    |--Visualization
        |-- app.py
        |-- Assets
            |-- app.css
            |-- favicon.ico
        |-- s3connector.py
        |-- visualizations.py
    |--requirements.txt
|-- Documents
    |-- Project Proposal
    |-- Project Report
|-- README.md
|-- RUNNING.md
```

## Data Knyts Team Members

- Anirban Banerjee (aba177)
- Ayush Raina (ara95)
- Tanmay Jain (tja34)
- Siddhartha Haldar (sha285)



