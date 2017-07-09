# !/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""Removes terms shorter than N size from CSV file.

Usage:
    removeTermsShorterThan.py [--category=<index> --text=<index>] (-l=<k> | --length=<k>) FILE
    removeTermsShorterThan.py -h | --help

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


def is_string_not_empty(s):
    return bool(s and s.strip())


def print_csv(category, text):
    if is_string_not_empty(text):
        print ("{category},\"{text}\""
               .format(category=category, text=text.strip()))


def remove_short_words(k, old_string):
    new_string = ' '.join([w for w in old_string.split() if len(w) > k])
    return new_string


def main():
    reload(sys)
    sys.setdefaultencoding("utf8")
    category_row = int(arguments["--category"])
    text_row = int(arguments["--text"])
    filename = arguments["FILE"]
    length = int(arguments["--length"])
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                text = remove_short_words(length, row[text_row])
                category = row[category_row]
                print_csv(category, text)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


if __name__ == "__main__":
    arguments = docopt(__doc__)
    # print(arguments)
    main()
