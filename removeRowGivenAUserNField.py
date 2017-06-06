# !/usr/bin/python
# coding=utf-8

# Python2.7
import csv
import sys
import os
import xlrd
import xlwt
import xlsxwriter


def outputFileName(file_name, user_name, file_extension):
    func_name = "-rmUser"
    return str(file_name) + str(func_name) + str(user_name) + str(file_extension)


# Creates a new CSV file with all the modifications made.
def workCSV(file_path, file_encoding, field_id, user_name):
    file_name, file_extension = os.path.splitext(file_path)
    file = open(file_path, 'rb')
    reader = csv.reader(file, delimiter=',', quotechar='\"')
    # New file
    file_new = open(outputFileName(file_name, user_name, file_extension), 'wb')
    writer = csv.writer(file_new, delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

    for row in reader:
        list_2_write = getListRowCSV(row, field_id, user_name)
        if list_2_write:
            writer.writerow(list_2_write)
    return outputFileName(file_name, user_name,file_extension)


# Creates a new XLS file with all the modifications made.
def workXLS(file_path, sheet_id, file_encoding, field_id, user_name):
    file_name, file_extension = os.path.splitext(file_path)
    workbook = xlrd.open_workbook(file_path, encoding_override = file_encoding)
    workbook_new = xlwt.Workbook(encoding = file_encoding)

    if sheet_id is None:
        worksheet = workbook.sheet_by_index(0)
        worksheet_new = workbook_new.add_sheet(str(u"Sheet 1"))
    else:
        worksheet = workbook.sheet_by_name(sheet_id)
        worksheet_new = workbook_new.add_sheet(str(sheet_id))

    for row in range(worksheet.nrows):
        list_2_write = getListRowExcel(worksheet, row, field_id, user_name)
        if list_2_write:
            for col in range(worksheet.ncols):
                worksheet_new.write(row, col, list_2_write[col])

    workbook_new.save(outputFileName(file_name, user_name,file_extension))
    return outputFileName(file_name, user_name,file_extension)


# Creates a new XLSX file with all the modifications made.
def workXLSX(file_path, sheet_id, file_encoding, field_id, user_name):
    file_name, file_extension = os.path.splitext(file_path)
    workbook = xlrd.open_workbook(file_path, encoding_override = file_encoding)
    workbook_new = xlsxwriter.Workbook(outputFileName(file_name, user_name,file_extension))
    if sheet_id is None:
        worksheet = workbook.sheet_by_index(0)
        worksheet_new = workbook_new.add_worksheet(str(u"Sheet 1"))
    else:
        worksheet = workbook.sheet_by_name(sheet_id)
        worksheet_new = workbook_new.add_worksheet(str(sheet_id) )
    for row in range(worksheet.nrows):
        list_2_write = getListRowExcel(worksheet, row, field_id, user_name)
        if list_2_write:
            for col in range(worksheet.ncols):
                worksheet_new.write(row, col, list_2_write[col])
    workbook_new.close()
    return outputFileName(file_name, user_name,file_extension)


# Returns an empty list if the USER_NAME is found in the FIELD_ID
# If the USER_NAME is not found in the FIELD_ID it returns a list contain every element of the ROW
def getListRowExcel(worksheet, row, field_id, user_name):
    row_list = list()
    cell_value = worksheet.cell(row, field_id).value
    if str(cell_value).lower() == str(user_name).lower():
        return list()
    else:
        for col in range (worksheet.ncols):
            row_list.append(worksheet.cell(row,col).value)
        return row_list


# Returns an empty list if the USER_NAME is found in the FIELD_ID
# If the USER_NAME is not found in the FIELD_ID it returns a list contain every element of the ROW
def getListRowCSV(row, field_id, user_name):
    row_list = list()
    cell_value = row[field_id]
    if str(cell_value).lower() == str(user_name).lower():
        return list()
    else:
        for cell in row:
            row_list.append(cell)
        return row_list


def main():
    # python prog.py file.(xls|xlsx) sheet_name encoding field
    # python prog.py file.csv encoding field
    # field starts at 0
    reload(sys)
    sys.setdefaultencoding('utf8')
    file_path = sys.argv[1]
    file_name, file_extension = os.path.splitext(file_path)

    if u".xls" == file_extension or u".xlsx" == file_extension:
        if len(sys.argv) == 6:
            sheet_id = sys.argv[2]
            file_encoding = sys.argv[3]
            field_id = sys.argv[4]
            user_name = sys.argv[5]
        else:
            print "Error arguments! file sheet-name encoding field(number) username"
            i = 0
            for elem in sys.argv:
                i += 1
                print "Element {counter} : {element}".format(counter=i,element=elem)
            return 0

        if ".xls" == file_extension:
            print workXLS(file_path, sheet_id, file_encoding, int(field_id), user_name)
        elif ".xlsx" == file_extension:
            print workXLSX(file_path, sheet_id, file_encoding, int(field_id), user_name)

    elif u".csv" == file_extension:
        if len(sys.argv) == 5:
            file_encoding = sys.argv[2]
            field_id = sys.argv[3]
            user_name = sys.argv[4]
        else:
            print "Error arguments! file encoding field(number) username"
        print workCSV(file_path, file_extension, int(field_id), user_name)

    return 0

if __name__ == "__main__":
    main()
