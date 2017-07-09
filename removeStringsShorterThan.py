# !/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""Removes terms shorter than N size from CSV file.

Usage:
    removeStringsShorterThan.py [--category=<index> --text=<index>] (-l=<k> | --length=<k>) FILE
    removeStringsShorterThan.py -h | --help

Options:
    --category=<index>          Category index [default: 0].
    --text=<index>              Text index [default: 1].
    -l=<k>, --length=<k>        Minimum size a term can have to remain in the
                                file.
    FILE                        CSV file. Where the first row is the category
                                and the second is the message. No headers
                                required.
    -h, --help                  Show this.

"""


import csv
import sys

from docopt import docopt


def print_csv(category, text, k):
    """

    :param category:
    :param text: string
    :param k: size
    :return:
    """
    if not is_shorter_than(k, text):
        print ("{category},\"{text}\""
               .format(category=category, text=text.strip()))


def is_shorter_than(k, text):
    """

    :param k: size
    :param text: string
    :return:
    """
    if len(text.split()) < k:
        return True
    else:
        return False


def main():
    category_row = int(arguments["--category"])
    text_row = int(arguments["--text"])
    filename = arguments["FILE"]
    length = int(arguments["--length"])
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                text = row[text_row]
                category = row[category_row]
                print_csv(category, text, length)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main()
