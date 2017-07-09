# !/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""Removes punctuation from file.

Usage:
    removeStopwords.py [--category=<index> --text=<index>] (--all|-e) FILE
    removeStopwords.py [--category=<index> --text=<index>] -c STOPFILE FILE
    removeStopwords.py -h | --help

Options:
    --category=<index>      Category index [default: 0].
    --text=<index>          Text index [default: 1].
    --all                   Remove all stopwords given by NLTK-portuguese.
    -c, --customized        Option to include a TXT file with stopwords.
    -e, --extended          Stopword list build according to previous studies.
                            Extra words: "tap", "portugal", "tapportugal"
    STOPFILE                TXT file. One stopword per line.
    FILE                    CSV file. Where the first row is the category and
                            the second is the message. No headers required.
    -h, --help              Show this.

"""


import csv
import sys
import unicodedata

from docopt import docopt
from nltk.corpus import stopwords


def is_string_not_empty(s):
    """Verifies if the given string s is empty

    """
    return bool(s and s.strip())


def print_csv(category, text):
    """Prints the given category and text in a csv format.

    Example:
    CATEGORY1,"TEXT1"

    """
    if is_string_not_empty(text):
        print ("{category},\"{text}\""
               .format(category=category, text=text.strip()))


def remove_stopwords(text, list_stopwords):
    """Removes the stopwords from a given text. The attribute list_stopwords
    is a list containg stopwords.

    """
    list_text_without_stopwords = list()
    for word in text.lower().split():
        if word not in list_stopwords:
            list_text_without_stopwords.append(word)
    return create_string(list_text_without_stopwords)


def create_string(list_words):
    """Given a list of words this function creates a string.

    """
    new_string = ""
    for word in list_words:
        new_string += word + " "
    return new_string[:-1]


def get_stopwords():
    """Returns a stopword list according with the settings on the command line
    3 options available: --all
                         --customized
                         --extended

    """
    if arguments["--extended"]:
        pt_set = set(stopwords.words('portuguese'))
        pt_set = normalize_set(pt_set)
        pt_set.add("tap")
        pt_set.add("portugal")
        pt_set.add("tapportugal")
        return pt_set
    elif arguments["--all"]:
        pt_set = set(stopwords.words('portuguese'))
        return normalize_set(pt_set)
    elif arguments["--customized"]:
        stopwords_file = arguments["STOPFILE"]
        stopwords_set = set()
        with open(stopwords_file, "rb") as f:
            try:
                for line in f:
                    stopwords_set.add(line.strip())
            except IOError as e:
                sys.exit('file %s: %s' % (stopwords_file, e))
        return normalize_set(stopwords_set)


def normalize_set(set2normalize):
    """Removes diacritics from sets, i.e. words are normalized to use english
    alphabet.

    """
    set_complete = set(set2normalize)
    for word in set2normalize:
        tmp_word = remove_accents(word.encode('utf-8'))
        if tmp_word not in set_complete:
            set_complete.add(tmp_word)
    return set_complete


def remove_accents(text):
    """Removes diacritics from a given text.

    """

    nfkd_form = unicodedata.normalize('NFKD', text)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def main():
    category_row = int(arguments["--category"])
    text_row = int(arguments["--text"])
    filename = arguments["FILE"]
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            lstop = get_stopwords()
            for row in reader:
                text_without_stopwords = remove_stopwords(text=row[text_row],
                                                          list_stopwords=lstop)
                print_csv(category=row[category_row],
                          text=text_without_stopwords)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main()
