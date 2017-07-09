# !/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""Removes punctuation from CSV file.

Usage:
    removesPunct.py [--category=<index> --text=<index>] --stay <p> FILE
    removesPunct.py [--category=<index> --text=<index>] --all FILE
    removesPunct.py -h | --help

Options:
    --category=<index>          Category index [default: 0].
    --text=<index>              Text index [default: 1].
    --stay                      Punctuation to remain in the file.
    --all                       Remove all punctuation.
    FILE                        CSV file. Where the first row is the category
                                and the second is the message. No headers
                                required.
    -h, --help                  Show this.

"""


import csv
import string
import sys

from docopt import docopt


def is_string_not_empty(s):
    return bool(s and s.strip())


def verify_input_punctuation_exists(s):
    for item in s:
        if item not in string.punctuation:
            return False
    return True


def print_csv(category, text):
    if is_string_not_empty(text):
        print ("{category},\"{text}\""
               .format(category=category, text=text.strip()))


def remove_punctuation(text):
    if arguments["--all"]:
        return text.translate(None, string.punctuation)
    elif arguments["--stay"]\
     and verify_input_punctuation_exists(arguments["<p>"]):
        exclude = set(string.punctuation)
        exclude = exclude-set(arguments["<p>"])
        return ''.join(char for char in text if char not in exclude)


def main():
    category_row = int(arguments["--category"])
    text_row = int(arguments["--text"])
    filename = arguments["FILE"]
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                print_csv(category=row[category_row],
                          text=remove_punctuation(row[text_row]))
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main()
