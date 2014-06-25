import openpyxl
import csv
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert XLSX files to CSV.')
    parser.add_argument('--sheet', '-s', dest='sheet' , type=str, help='Sheet name in XLSX to export.')
    parser.add_argument('File', type=str, help='XLSX to export.')
    args = parser.parse_args()
    
    if (args.sheet):
        wb = openpyxl.load_workbook(filename = args.File, use_iterators = True)
        sh = wb.get_sheet_by_name(name = args.sheet)
        if sh:
            lst = args.File.split('.')
            lst.pop()
            csvfile = ''.join(lst)
            csvfile += '-Sheet-' + args.sheet + '.csv'
            with open(csvfile, 'w', newline='') as f:
                c = csv.writer(f)
                for r in sh.iter_rows():
                    c.writerow([cell.internal_value for cell in r])
        else:
            #TODO if there are no sheets specified, try to process all of them
            #as separate files
            print("Sheet " + args.sheet + " missing! Exiting...")
            exit