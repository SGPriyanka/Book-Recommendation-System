
import os
import csv
import pandas as pd

path = "/Users/user _dataset/" #modify the path to access the user data
for subdir, dirs, files in os.walk(path):
    books=files
    with open('/Users/usrdata.csv', "w",encoding = "utf-8") as output: #modify the path to store the csv_file
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(['book_names'])
        for val in books:
            if val.endswith(".txt"): 
                writer.writerow([val])


           

