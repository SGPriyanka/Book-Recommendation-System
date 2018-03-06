import os
import csv
import pandas as pd



path = "/Users/training set/"
#modify the path according to your path
for subdir, dirs, files in os.walk(path):
    books=files
    with open('/Users/out.csv', "w",encoding = "utf-8") as output:  #modify th path to store the file 
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(['book_names'])
        for val in books:
            if val.endswith(".txt"): 
                writer.writerow([val])


           


