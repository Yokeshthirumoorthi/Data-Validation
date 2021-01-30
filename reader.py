#!/usr/bin/env python
import pandas as pd

# nrows : int, default None
# nrows is the number of rows of file to read. Its useful for reading pieces of large files
df = pd.read_csv('crashdata.csv', nrows=2)

print(df.to_string()) 