# !/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""Replaces number for dummies or delete the numbers. Only the selected
options are converted to dummies. The all the other numbers are deleted.

Usage:
    replace_numbers.py [--category=<index> --text=<index>] [-dflum] FILE
    replace_numbers.py [--category=<index> --text=<index>] -R FILE
    replace_numbers.py -h | --help

Options:
    --category=<index>      Category index [default: 0].
    --text=<index>          Text index [default: 1].
    -d, --date              Convert dates into dummies.
                                Example:
                                    11/3/2015 -> TAGDATENUMBER
    -f, --flight            Convert flight numbers into dummies.
                                Example:
                                    TP1123 -> TAGFLIGHTNUMBER
    -l, --delays            Convert delays into dummies.
                                Example:
                                    40m -> TAGDELAYNUMBER
    -m, --money             Convert money into dummies.
                                Example:
                                    404eur -> TAGMONEYNUMBER
    -u, --hours             Convert hours into dummies.
                                Example:
                                    15:40h -> TAGHOURNUMBER
    -R, --remove            Remove all numbers.
    FILE                    CSV file. Where the first row is the category
                            and the second is the message. No headers.
    -h, --help              Show this.

"""

import csv
import re
import sys

from docopt import docopt


def is_string_not_empty(s):
    return bool(s and s.strip())


def print_csv(category, text):
    if is_string_not_empty(text):
        print ("{category},\"{text}\""
               .format(category=category, text=text.strip()))


def replace_numbers(text):
        if arguments["--remove"]:
            # this function below removes all numbers in the text
            text = ' '.join(s for s in text.split() if not any(c.isdigit() for c in s))
            return re.sub('^[0-9 ]+', '', text)
        else:
            if arguments["--money"]:
                # this regex could be improved. It does not recognize
                # numbers with commas.
                text = re.sub(r" ?\d+ ?(€|eur|euro|euros|\$|dol|dolar|dolares|£|libra|libras)\b",
                              " TAGMONEYNUMBER ", text)
            else:
                text = re.sub(r" ?\d+ ?(€|eur|euro|euros|\$|dol|dolar|dolares|£|libra|libras)\b",
                              "", text)
            if arguments["--flight"]:
                text = re.sub(r"\btp ?\d{1,4}\b",
                              " TAGFLIGHTNUMBER ", text)
            else:
                text = re.sub(r"\btp ?\d{1,4}\b", "", text)
            if arguments["--hours"]:
                text = re.sub(r" ?\d+ ?[:|h|,] ?\d+( ?|m|h)\b",
                              " TAGHOURNUMBER ", text)
            else:
                text = re.sub(r" ?\d+ ?[:|h|,] ?\d+( ?|m|h)\b", "", text)
            if arguments["--date"]:
                text = re.sub(r" ?\d+ ?/ ?\d+ ?/ ?\d+\b",
                              " TAGDATENUMBER ", text)
            else:
                text = re.sub(r" ?\d+ ?/ ?\d+ ?/ ?\d+\b", "", text)
            if arguments["--delays"]:
                text = re.sub(r" ?\d+ ?(minutos|minuto|m|min|hora|horas|h)\b",
                              " TAGDELAYNUMBER ", text)
            else:
                text = re.sub(r" ?\d+ ?(minutos|minuto|m|min|hora|horas|h)\b",
                              "", text)

            text = ' '.join(s for s in text.split() if not any(c.isdigit() for c in s))
            text = re.sub('^[0-9 ]+', '', text)
            return text


def main():
    category_row = int(arguments["--category"])
    text_row = int(arguments["--text"])
    filename = arguments["FILE"]
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                text_replaced_numbers = replace_numbers(row[text_row])
                print_csv(row[category_row], text_replaced_numbers)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main()
