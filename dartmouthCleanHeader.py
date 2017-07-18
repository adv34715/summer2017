
# coding: utf-8

# # To use this code correctly, make sure:
# # 1) the input path is excel file.
# # 2) there is/are 1 or 2 row(s) of headers. 
# # Notice that after processing, the original file is replaced.

import pandas as pd
import csv
import xlrd
import os

def checkHeader(header,i):
    #print(i,header[i])
    if i < 0:
        return('')
    elif header[i] != '':
        return(header[i])
    else:
        i -= 1
        return(checkHeader(header,i))


def findHeader(path):
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path,ragged_rows=True)
    
    if book.nsheets == 1:
        print("================Processing the file %s================"%path)
        # get the first worksheet
        sheet = book.sheet_by_index(0)
        
        col_num = sheet.ncols # number of columns
        print("There are %d columns." %col_num)
        
        # find which row is the last row of header
        for i in range(5):
            #print(i,len(first_sheet.row_values(i)))
            if len(sheet.row_values(i)) == col_num:
                break
        
        skip_rows = list(range(i))
        last_header = sheet.row_values(i)
        
        # to see if there are 2 row of headers
        if len(sheet.row_values(i-1))>2:
            new_header = []
            first_header = sheet.row_values(i-1)
            first_header += ['']*(col_num - len(first_header))
            for c in range(col_num):
                header_first = checkHeader(first_header,c)
                header_last = last_header[c]
                if header_last == '':
                    new_header.append(''.join((header_first,header_last)))
                else:
                    new_header.append('-'.join((header_first,header_last)))
        else:
            new_header = last_header
        
        xls = pd.read_excel(path,skiprows=skip_rows)
        xls.columns = new_header
        xls.to_excel(path,index=False)
        print("%s is done." %path)
    else:
        print(path)

for (dirpath, dirnames, filenames) in os.walk('/Users/yimengz/Downloads'):
    for filename in filenames:
        if filename.endswith('.xls'): 
            findHeader(filename)



