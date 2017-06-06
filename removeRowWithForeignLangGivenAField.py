# !/usr/bin/python
# coding=utf-8

# Python2.7
import csv
import sys
import string as string_lib
import os
import xlrd
import xlwt
import xlsxwriter
import re
from nltk.corpus import stopwords

def outputFileName(file_name, file_extension):
    func_name = "-PT"
    return str(file_name) + str(func_name) + str(file_extension)

# Creates a new CSV file with all the modifications made.
def workCSV(file_path, file_encoding, field_id):
    file_name, file_extension = os.path.splitext(file_path)
    file = open(file_path, 'rb')
    reader = csv.reader(file, delimiter=',', quotechar='\"')
    # New file
    file_new = open(outputFileName(file_name, file_extension), 'wb')
    writer = csv.writer(file_new, delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

    for row in reader:
        list_2_write = getListWithPortugueseRowCSV(row, field_id)
        if list_2_write:
            writer.writerow(list_2_write)
    return outputFileName(file_name, file_extension)

# Creates a new XLS file with all the modifications made.
def workXLS(file_path, sheet_id, file_encoding, field_id):
    file_name, file_extension = os.path.splitext(file_path)
    workbook = xlrd.open_workbook(file_path, encoding_override = file_encoding)
    workbook_new = xlwt.Workbook(encoding = file_encoding)

    worksheet = workbook.sheet_by_name(sheet_id)
    worksheet_new = workbook_new.add_sheet(str(sheet_id))

    for row in range(worksheet.nrows):
        list_2_write = getListWithPortugueseRowExcel(worksheet, row, field_id)
        if list_2_write:
            for col in range(worksheet.ncols):
                worksheet_new.write(row, col, list_2_write[col])

    workbook_new.save(outputFileName(file_name, file_extension))
    return outputFileName(file_name, file_extension)

# Creates a new XLSX file with all the modifications made.
def workXLSX(file_path, sheet_id, file_encoding, field_id):
    file_name, file_extension = os.path.splitext(file_path)

    workbook = xlrd.open_workbook(file_path, encoding_override = file_encoding)
    worksheet = workbook.sheet_by_name(sheet_id)

    workbook_new = xlsxwriter.Workbook(outputFileName(file_name, file_extension))
    worksheet_new = workbook_new.add_worksheet(str(sheet_id))

    for row in range(worksheet.nrows):
        list_2_write = getListWithPortugueseRowExcel(worksheet, row, field_id)
        if list_2_write:
            for col in range(worksheet.ncols):
                worksheet_new.write(row, col, list_2_write[col])
    workbook_new.close()
    return outputFileName(file_name, file_extension)

# Returns a list with the elements of the ROW.
# If the message in the FIELD_ID is not portuguese, it returns an empty list.
def getListWithPortugueseRowExcel(worksheet, row, field_id):
    row_list = list()
    cell_value = worksheet.cell(row, int(field_id)).value
    if isForeignString(cell_value):
        return list()
    else:
        for col in range (worksheet.ncols):
            row_list.append(worksheet.cell(row,col).value)
        return row_list

# Returns a list with the elements of the ROW.
# If the message in the FIELD_ID is not portuguese, it returns an empty list.
def getListWithPortugueseRowCSV(row, field_id):
    row_list = list()
    cell_value = row[int(field_id)]
    if isForeignString(cell_value):
        return list()
    else:
        for cell in row:
            row_list.append(cell)
        return row_list

# Returns True if no word of the STRING is found on LANGUAGES stopword list.
# LANGUAGES = english, french, italian, german and spanish
def isForeignString(string):
    if isinstance(string, basestring):
        for word in separatePunctuation(string).split():
            if word not in string_lib.punctuation:
                if isForeignWord(word):
                    return True
        return False
    else:
        return False

# Returns True if the WORD is not found on LANGUAGES stopword list.
# LANGUAGES = english, french, italian, german and spanish
def isForeignWord(word):
    languages = [u'english', u'french', u'italian', u'german', u'spanish']
    set_stopwords_languages = set()
    for language in languages:
        set_stopwords_languages = set_stopwords_languages.union(getLangWords(language))
    if word.lower() in set_stopwords_languages:
        return True
    else:
        return False

# Returns a set of words in a given LANGUAGE.
# Each set has the stopword list from NLTK plus a custom made stopword list.
# Languages available english, french, italian, german and spanish
# NOTE: Customed made list airport related. Every word that can be mistaken with portuguese is removed.
def getLangWords(language):
    if language == 'english' or language == 'en':
        # >> nltk_stopwords_pt & nltk_stopwords_en
        # >> set([u'me', u'do', u'for', u'no', u'o', u'as', u'a'])
        nltk_stopwords_en = set(stopwords.words('english'))
        remove_stopwords_en_from_nltk = set([u've', u'i', u'me', u'am', u'do', u'for', u'a', u'as', u'no', u'so', u'o', u'ma', u'in', u'd', u'm'])
        nltk_stopwords_en_customized = nltk_stopwords_en.difference(remove_stopwords_en_from_nltk)
        custom_stopwords_en = set([u'hi', u'confirm', u'about', u'airport', u'answer', u'arrival', u'assistance', u'bye', u'cancelled', u'delay', u'delayed', u'departure', u'flies', u'flight', u'have', u'hello', u'help', u'how', u'luggage', u'luggages', u'my', u'overweight', u'pay', u'payment', u'receive', u'said', u'say', u'strike', u'suitcase', u'really', u'thank', u'thanks', u'that', u'this', u'travel', u'true', u'understanding', u'validate', u'very', u'wait', u'weight', u'with', u'you', u'yours'])
        return nltk_stopwords_en_customized | custom_stopwords_en

    elif language == 'french' or language == 'fr':
        # >> nltk_stopwords_pt & nltk_stopwords_en
        # >> set([u'me', u'à', u'tu', u'mais', u'de', u'as', u'que', u'vos', u'eu', u'ou', u'te', u'se', u'nos'])
        nltk_stopwords_fr = set(stopwords.words('french'))
        remove_stopwords_fr_from_nltk = set([  u'me', u'à', u'tu', u'mais', u'de', u'as', u'que', u'vos', u'eu', u'ou', u'te', u'se', u'nos', u'ta', u'qu', u'd', u'en', u'es', u'est', u'ton', u'ma', u'n', u'seras', u'sera', u'ai', u'par', u'ne', u'sa', u'c', u'm', u'mes', u'la', u'le'])
        nltk_stopwords_fr_customized = nltk_stopwords_fr.difference(remove_stopwords_fr_from_nltk)
        custom_stopwords_fr = set([ u'dis', u'dire', u'aéroport', u'répondre', u'arrivée', u'assistance', u'aurevoir', u'annulé ', u'comfirmé ', u'retard', u'retardé ', u'départ', u'voler', u'avoir', u'bonjour', u'aide', u'salut', u'comment', u'bagage', u'bagages', u'surpoids', u'payer', u'payement', u'recevoir', u'grève', u'valise', u'vol', u'remercier', u'merci', u'voyager', u'compréhension', u'valider', u'très', u'attendez', u'nous', u'poid', u'bagage', u'toi', u'vous', u'votre', u'mon', u'non'])
        return nltk_stopwords_fr_customized | custom_stopwords_fr

    elif language == 'italian'  or language == 'it':
        # >> nltk_stopwords_pt & nltk_stopwords_it
        # >> set([u'a', u'e', u'sua', u'tu', u'o', u'da', u'era', u'tua', u'fosse', u'se', u'fui'])
        nltk_stopwords_it = set(stopwords.words('italian'))
        remove_stopwords_it_from_nltk = set([ u'è', u'in', u'a', u'e', u'sua', u'tu', u'o', u'da', u'era', u'tua', u'fosse', u'se', u'fui', u'farei', u'hai', u'le', u'la',u'lo', u'li', u'ti', u'sei', u'sua', u'dei', u'sul',u'tua', u'come', u'c', u'quanta', u'quanto', u'ha', u'ma', u'era', u'vi', u'ai', u'ne', u'dai', u'sono'])
        nltk_stopwords_it_customized = nltk_stopwords_it.difference(remove_stopwords_it_from_nltk)
        custom_stopwords_it = set([ u'circa', u'risposta', u'arrivo', u'assistenza', u'ciao', u'cancellato', u'conferma', u'contattare', u'contattato', u'ritardo', u'ritardato', u'partenza', u'volare', u'volo', u'volare', u'avere', u'ho', u'avete', u'hanno', u'ciao', u'aiuto', u'ciao', u'bagaglio', u'bagagli', u'mio', u'sovrappeso', u'pagare', u'pagato', u'ricevuto', u'detto', u'dire', u'dice', u'sciopero', u'valigia', u'grazie', u'ringrazio', u'grazie', u'quella', u'che', u'questo', u'questa', u'viaggio', u'viaggiare', u'comprensione', u'convalidare', u'molto', u'attesa', u'aspettando', u'noi', u'voi', u'vostro'])
        return nltk_stopwords_it_customized | custom_stopwords_it

    elif language == 'german'  or language == 'de':
        # >> nltk_stopwords_pt & nltk_stopwords_de
        # >> set([u'um', u'das', u'da'])
        nltk_stopwords_de = set(stopwords.words('german'))
        remove_stopwords_de_from_nltk = set([ u'um', u'das', u'da', u'es', u'uns', u'des', u'dem', u'in', u'manchem', u'so'])
        nltk_stopwords_de_customized = nltk_stopwords_de.difference(remove_stopwords_de_from_nltk)
        custom_stopwords_de = set([ u'ungefähr', u'flughafen', u'antwort', u'ankunft', u'unterstützung', u'tschüss', u'storniert', u'bestätigen', u'kontakt', u'verspätung', u'verspätet', u'abflug', u'fliegen', u'flug', u'fliegen', u'haben', u'hallo', u'hilfe', u'hi', u'wie', u'gepäck', u'gepäckstücke', u'mein', u'meine', u'nein', u'übergewicht', u'zahlen', u'bezahlung', u'erhalten', u'gesagt', u'sagen', u'streik', u'koffer'])
        return nltk_stopwords_de_customized | custom_stopwords_de

    elif language == 'spanish' or language == 'es':
        # >> nltk_stopwords_pt & nltk_stopwords_es
        # >> set([u'este', u'est\xe1', u'por', u'seremos', u'estamos', u'esta', u'no', u'tu', u'estas', u'ser\xedamos', u'te', u'a', u'para', u'\xe9ramos', u'de', u'que', u'como', u'nos', u'me', u'e', u'entre', u'o', u'somos', u'era', u'ser\xe1', u'os', u'se', u'fui'])
        nltk_stopwords_es = set(stopwords.words('spanish'))
        remove_stopwords_es_from_nltk = set([u'seríamos', u'serías', u'estarás', u'seréis', u'ante', u'sería', u'estados', u'éramos', u'estará', u'sentidos', u'sentido', u'antes', u'le', u'la', u'lo', u'tu', u'ti', u'estar', u'te', u'porque', u'ya', u'nada', u'de', u'tanto', u'nos', u'estoy', u'estaremos', u'somos', u'desde', u'sentida', u'en', u'estamos', u'todo', u'es', u'estas', u'sobre', u'era', u'les', u'que', u'como', u'eras', u'o', u'serás', u'algo', u'fui', u'os', u'está', u'por', u'por', u'donde', u'contra', u'estado', u'los', u'estás', u'más', u'para', u'ha', u'me', u'seremos', u'este', u'estando', u'sois', u'no', u'sentidas', u'todos', u'estada', u'las', u'a', u'e', u'entre', u'será', u'se' , u'durante', u'esta' ] )
        nltk_stopwords_es_customized = nltk_stopwords_es.difference(remove_stopwords_es_from_nltk)
        custom_stopwords_es = set([u'aeropuerto', u'llegada', u'asitencia', u'adios', u'retraso', u'retrasado', u'salida', u'volar', u'vuelo', u'volar', u'tener', u'hola', u'ayuda', u'hola', u'cómo', u'equipaje', u'equipajes', u'mio', u'recibido', u'dicho', u'decir', u'huelga', u'maleta'])
        return nltk_stopwords_es_customized | custom_stopwords_es

    else:
        return 0

# Return the STRING without punctuation
def separatePunctuation(string):
    list_punctuation = '([:.+^*%\/_,!?(\[\])])'
    string = re.sub(list_punctuation, r' \1 ', string)
    return re.sub('\s{2,}', ' ', string)

def main():
    # python prog.py file.(xls|xlsx) sheet_name encoding field
    # python prog.py file.csv encoding field
    reload(sys)
    sys.setdefaultencoding('utf8')
    file_path = sys.argv[1]
    file_name, file_extension = os.path.splitext(file_path)

    if u".xls" == file_extension or u".xlsx" == file_extension:
        if len(sys.argv) == 5:
            sheet_id = sys.argv[2]
            file_encoding = sys.argv[3]
            field_id = sys.argv[4]
        else:
            print "Error arguments! file sheet-name encoding field(number)"
            return 0

        if ".xls" == file_extension:
            print workXLS(file_path, sheet_id, file_encoding, field_id)
        elif ".xlsx" == file_extension:
            print workXLSX(file_path, sheet_id, file_encoding, field_id)

    elif u".csv" == file_extension:
        if len(sys.argv) == 4:
            file_encoding = sys.argv[2]
            field_id = sys.argv[3]
        else:
            print "Error arguments! file encoding field(number)"
            return 0

        print workCSV(file_path, file_extension, field_id)

    return 0

if __name__ == "__main__":
    main()
