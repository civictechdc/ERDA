#!/usr/bin/env python

import openpyxl
import csv
import argparse
import sys
import glob
from collections import defaultdict, OrderedDict
import pandas as pd
import csv


def writeCSV(dataframe, filename):
    with open(filename, 'w') as f:
        c = csv.writer(f)
        for row in sheet.iter_rows():
            c.writerow([cell.value for cell in row])



def import_erda_files(data_path):
    '''Imports all Excel files in the specified directory.'''
    file_names = glob.glob(data_path + "/*.csv")
    all_data_frames = pd.DataFrame(columns=["Date", "Dispatch Time (HH:MM:SS)", "Location", "Response Time (HH:MM:SS)", "Unit"])
    for file_name in file_names:
        dataSet = pd.read_csv(file_name)
        # print(dataSet.head())
        all_data_frames = pd.concat([all_data_frames, dataSet])
    print(all_data_frames.describe())
    print("Writing to file: " + data_path + "fullSet/fullERDAdata.csv")
    all_data_frames.to_csv(data_path + "fullSet/fullERDAdata.csv")


def usage():
    '''Prints a help string.'''
    print("usage: mergeAndClean.py <dirname>")

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        import_erda_files(sys.argv[1])
    else:
        usage()

