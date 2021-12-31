import xlrd
import os
import numpy as np
import pandas as pd

xls_files = os.listdir(os.getcwd() + '/xls')
other_store_operating_expenses = []

for i in range(len(xls_files)):
    file_name = xls_files[i]
    if file_name == '.DS_Store':
        continue
    
    f = os.getcwd() + '/xls/' + file_name
    book = xlrd.open_workbook(f)
    sheet = book.sheet_by_name("results of operations")
    
    row_count = sheet.nrows
    col_count = sheet.ncols

    for cur_row in range(0, row_count):
        for cur_col in range(0, col_count):
            cell = sheet.cell(cur_row, cur_col)
            if cell.value == "Other store operating expenses":
                value = sheet.cell(cur_row, cur_col + 3)
                other_store_operating_expenses.append(value)
    #         print(cell.value, cell.ctype)

print(other_store_operating_expenses)
