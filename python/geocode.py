import openpyxl
import csv
import argparse
import sys
import glob
from collections import defaultdict, OrderedDict
import pandas as pd
import csv
import re

def regex_cases(address):
	''' if it has an address as the first letters, parse this way '''
	if (  re.search("[0-9].+X)", address)):
		print(address)
	''' if it has two NE/NW/SE/SW, split and parse as a cross street '''


def import_erda_file(data_path):
    '''Imports all Excel files in the specified directory.'''
    # print(data_path)
    file_name = glob.glob(data_path + "/*.csv")
    # print(file_name[0])
    all_data_frames = pd.read_csv(file_name[0])
    ''' input the whole row to regex_addresses  '''
    regex_cases(all_data_frames['Location'])



def usage():
    '''Prints a help string.'''
    print("usage: buildcsv.py <dirname>")
    print("where <dirname> is the path to the fullERDAdata.csv, not including the file name")



if __name__ == "__main__":
    if (len(sys.argv) == 2):
        import_erda_file(sys.argv[1])
    else:
        usage()


