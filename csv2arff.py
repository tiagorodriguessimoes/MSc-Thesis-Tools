# !/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""Transforms a csv file into a arff file (WEKA). It is expected a csv file
    with two columns only. Developed for Master's Thesis: Automating the
    Response Processes in TAP PORTUGAL’s Social Networks.

Usage:
    csv2arff.py [--category=<index> --text=<index>] FILE
    csv2arff.py -h | --help

Options:
    --category=<index>      Category index [default: 0].
    --text=<index>          Text index [default: 1].
    FILE                    CSV file. CSV should contain headers.
    -h, --help              Show this.

"""

import csv
import sys
from os.path import basename

from docopt import docopt


def print_arff_header(relation_name, set_category):
    """
        Prints a formatted arff header.

    Example:
    @relation   xyz
    @attribute  text1       string
    @attribute  category1   {A, B, C}
    @data
    A, "this is the first string"

    :param relation_name: string with the relation name
    :param set_category: set containing the categories

    """
    string_category = ", ".join(str(elem) for elem in set_category)

    print("@relation {relation_name}"
          .format(relation_name=relation_name))
    print("@attribute {attribute_name} {attribute_type}"
          .format(attribute_name="category",
                  attribute_type="{" + string_category + "}"))
    print("@attribute {attribute_name} {attribute_type}"
          .format(attribute_name="text",
                  attribute_type="string"))
    print("@data")


def print_arff_row(category, text):
    """
        Print the content into the arff

    Example:
    CATEGORY1, "TEXT1"

    :param category: string / char
    :param text:

    """
    print("{category},\"{text}\"".format(category=category.upper(), text=text))


def main():
    filename = arguments["FILE"]
    with open(filename, "rb") as f:
        reader = csv.reader(f)
        set_category = set()
        try:
            for row in reader:
                """Retrieve category names.
                """
                category_row = int(arguments["--category"])
                set_category.add(row[category_row].upper())
            print_arff_header(relation_name=basename(filename),
                              set_category=set_category)
            f.seek(0)
            for row in reader:
                """Print all the categories followed by the text.
                """
                category_row = int(arguments["--category"])
                text_row = int(arguments["--text"])
                print_arff_row(category=row[category_row],
                               text=row[text_row])
        except csv.Error as e:
            sys.exit("file %s, line %d: %s" % (filename, reader.line_num, e))


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main()
