# !/usr/bin/python
# coding=utf-8

# Python2.7
""" Functions that might be useful for text preprocessing.
"""
import HTMLParser
import itertools
import re
import unicodedata
import string


def remove_accents(input_string):
    nfkd_form = unicodedata.normalize('NFKD', input_string)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def remove_quote_symbols(input_string):
    str_message = input_string.replace("'", " ")
    str_message = str_message.replace("\'", " ")
    str_message = str_message.replace("´", " ")
    str_message = str_message.replace("`", " ")
    str_message = str_message.replace("\"", " ")
    return str_message


def remove_url(input_string):
    return re.sub(r"https?://([a-z0-9A-Z]+(:[a-zA-Z0-9]+)?@)?[-a-z0-9A-Z\-]+(\.[-a-z0-9A-Z\-]+)*((:[0-9]+)?)(/[a-zA-Z0-9;:/\.\-_+%~?&@=#\(\)]*)?", '', input_string)


def html_parser(input_string):
    html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(input_string)


def standardize_emoji(input_string):
    emoji_happy = " tag_happy_emoji "
    emoji_sad = " tag_sad_emoji "
    str_message = input_string.replace(":)", emoji_happy)
    str_message = str_message.replace(":-)", emoji_happy)
    str_message = str_message.replace(":d", emoji_happy)
    str_message = str_message.replace(":\'d", emoji_happy)
    str_message = str_message.replace(":p", emoji_happy)
    str_message = str_message.replace(";)", emoji_happy)
    str_message = str_message.replace("<3", emoji_happy)
    str_message = str_message.replace(":(", emoji_sad)
    str_message = str_message.replace(":/", emoji_sad)
    str_message = str_message.replace(";(", emoji_sad)
    str_message = str_message.replace(":\'(", emoji_sad)
    return str_message


def remove_twitter_stuff(input_string):
    entity_prefixes = ['@', '#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = input_string.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    str_message = ' '.join(words)
    return str_message


def remove_email(input_string):
    return re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b", r'',
                  input_string)


# Looooove -> Loove
def standardize_words(input_string):
    return ''.join(''.join(s)[:2] for _, s in itertools.groupby(input_string))
