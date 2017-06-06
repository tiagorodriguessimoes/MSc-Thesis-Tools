# !/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8
"""Transforms a csv file into a arff file. It is expected a csv file with two
    columns only.

Usage:
    csv2arff.py [--category=<index> --text=<index>] FILE
    csv2arff.py -h | --help

Options:
    --category=<index>      Category index [default: 0].
    --text=<index>          Text index [default: 1].
    FILE                    CSV file. CSV should contain headers.
    -h, --help              Show this.

"""

from docopt import docopt
from os.path import basename
import csv
import sys
encoding = "utf-8"


def print_arff_header(relation_name, set_category):
    """Prints a formated arff header.
    relation_name       string with the relation name.
    set_category        set containing the categories.

    This print has 2 attibutes.
    Attribute 1: text
    Attribute 2: category

    Example:
    @relation   xyz
    @attribute  text1       string
    @attribute  category1   {A, B, C}
    @data

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
    """Print the content

    Example:
    CATEGORY1, "TEXT1"

    """

    print "{category},\"{text}\"".format(category=category.upper(), text=text)


def main():
    reload(sys)
    sys.setdefaultencoding("utf8")
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
