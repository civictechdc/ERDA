#!/usr/bin/env python

import openpyxl
import csv
import argparse
import sys

def writeCSV(filename, sheet, sheetname):
    if sheet:
        lst = filename.split('.')
        lst.pop()
        csvfile = ''.join(lst)
        csvfile += '-Sheet-' + sheetname + '.csv'
        with open(csvfile, 'w', newline='') as f:
            c = csv.writer(f)
            for row in sheet.iter_rows():
                c.writerow([cell.value for cell in row])
    else:
        print(filename + ": " + sheetname + " sheet could not be found! Continuing...", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert XLSX files to CSV. Use \'--\' to separate sheet names and XLSX file names.')
    parser.add_argument('-s', '--sheets', dest='sheets',nargs="*", type=str, help='Sheet name in XLSX to export.')
    parser.add_argument('Files', type=str, nargs="+" ,help='XLSX files to export.')
    args = parser.parse_args()
    for xlsxFilename in args.Files:
        wb = openpyxl.load_workbook(filename = xlsxFilename, use_iterators = True)

        csvfile = xlsxFilename
        if (args.sheets):
            for sheetname in args.sheets:
                sheet = wb.get_sheet_by_name(name = sheetname)
                writeCSV(csvfile, sheet, sheetname)
        else:
            for sheetname in wb.get_sheet_names():
                sheet = wb.get_sheet_by_name(name = sheetname)
                writeCSV(csvfile, sheet, sheetname)