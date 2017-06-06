# !/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8
"""Transforms a XLS file into a CSV file. It is expected a XLS file with two
    columns only without headers.

Usage:
    xls2csv.py [--category=<index> --text=<index>] [--sheet=<index>] FILE
    xls2csv.py -h | --help

Options:
    --category=<index>      Category index [default: 0].
    --text=<index>          Text index [default: 1].
    --sheet=<index>         Sheet index [default: 0].
    FILE                    CSV file. CSV should contain headers.
    -h, --help              Show this.

"""

from docopt import docopt
import sys
import xlrd
encoding = "utf-8"

def print_csv_row(category, text):
        print "{category},\"{text}\"".format(category=category.upper(), text=text)

def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    filename = arguments["FILE"]
    category_row = int(arguments["--category"])
    text_row = int(arguments["--text"])
    sheet_index = int(arguments["--sheet"])

    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(sheet_index)
    for rx in range(sheet.nrows):
        category = sheet.cell_value(rowx=rx, colx=category_row).decode(encoding)
        category = category.encode(encoding)
        text = sheet.cell_value(rowx=rx, colx=text_row).decode(encoding)
        text = text.encode(encoding)
        print_csv_row(category=category, text=text)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main()
