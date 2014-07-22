#!/usr/bin/env python

import openpyxl
import csv
import argparse

def writeCSV(filename, sheet, sheetname):
    if sheet:
        csvfile = filename
        csvfile += '-Sheet-' + sheetname + '.csv'
        with open(csvfile, 'w', newline='') as f:
            c = csv.writer(f)
            for row in sheet.iter_rows():
                c.writerow([cell.value for cell in row])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert XLSX files to CSV.')
    parser.add_argument('--sheet', '-s', dest='sheet' , type=str, help='Sheet name in XLSX to export.')
    parser.add_argument('File', type=str, help='XLSX to export.')
    args = parser.parse_args()
    
    wb = openpyxl.load_workbook(filename = args.File, use_iterators = True)
    lst = args.File.split('.')
    lst.pop()
    csvfile = ''.join(lst)
    
    if (args.sheet):
        sheet = wb.get_sheet_by_name(name = args.sheet)
        writeCSV(csvfile, sheet, args.sheet)
    else:
        for sheetname in wb.get_sheet_names():
            sheet = wb.get_sheet_by_name(name = sheetname)
            writeCSV(csvfile, sheet, sheetname)