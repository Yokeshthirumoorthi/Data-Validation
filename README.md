# Data-Validation
This project provides code to assert and test the correctness of data

### Data
This project uses [a listing of all Oregon automobile crashes on the Mt. Hood Hwy (Highway 26) during 2019](https://docs.google.com/spreadsheets/d/1EuDUHu6GCdnjVfYJEXLXFYKygtVc0UJVUH_UkIrk0DI). This data is provided by (Oregon Department of Transportation)[https://www.oregon.gov/odot].

Here is the available documentation for this data: [description of columns](https://drive.google.com/file/d/1dsqtr_tuE8BK3mwBYGiWpRayYTIJE2Mt), [Oregon Crash Data Coding Manual](https://www.oregon.gov/ODOT/Data/documents/CDS_Code_Manual.pdf).


### How To Run This Project

1. Setup virtual environment
```bash
    virtualenv venv
    source venv/bin/activate
```

2. Download the csv data as crashdata.csv. And run
```bash
    python3 ./reader.py
```