import os, sys
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")

import csv
import pytz
from datetime import datetime
import re

from catalog.models import Category, BoxName
from inventory.models import Box

ERROR_COUNT = 0
UNREAD_LINE_COUNT = 0
READ_LINE_COUNT = 0
UNKNOWN_EXPIRATION = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)

def get_category(data):
    try:
        letter = data[0]
        category = Category.objects.get(letter=letter)
    except:
        global ERROR_COUNT
        ERROR_COUNT = ERROR_COUNT + 1
        category = Category.objects.get(letter='Y')
    return category

def get_box_size(data):
    if re.match("^[LS] - +\d{1,2}\.\d lbs\.{0,1}", data.strip()):
        return data.strip()[0]
    else:
        print '[ERROR] Could not import size: ' + data
        global ERROR_COUNT
        ERROR_COUNT = ERROR_COUNT + 1
        return 'U'

def get_box_weight(data):
    if re.match("^[LS] - +\d{1,2}\.\d lbs\.{0,1}", data.strip()):
        return float(data.split('-')[1].strip().split(' ')[0])
    else:
        print '[ERROR] Could not import weight: ' + data
        global ERROR_COUNT
        ERROR_COUNT = ERROR_COUNT + 1
        return 0.0

def get_items(data):
    if re.match("^.*:.*\Z", data.strip()) is not None:
        box_name_text = data.split(":")[0].strip()
        try:
            box_name = BoxName.objects.get(name=box_name_text)
            
        except:
            print '[ERROR] Could not import items: ' + data
            global ERROR_COUNT
            ERROR_COUNT = ERROR_COUNT + 1
            return None

        print box_name

def get_date(data):
    if re.match('^\d{1,2}/\d{4}\Z', data.strip()) is not None:
        formattedDate = data.strip().split("/")
        validatedDate = datetime(int(formattedDate[1]),int(formattedDate[0]),1, 0, 0, 0, 0, pytz.UTC)
        return validatedDate
    elif re.match('^No EXP\Z',data.strip()):
        return None
    elif re.match('^\Z', data.strip()):
        return None
    else:
        print '[ERROR] Could not import date: ' + data
        global ERROR_COUNT
        ERROR_COUNT = ERROR_COUNT + 1
        return UNKNOWN_EXPIRATION

def importer(file_name):
    print("\nStarting " + file_name + " Import to MySQL Database") 

    csvData = csv.reader(file(file_name, 'rU'), delimiter = ',', dialect=csv.excel_tab)
    csvArray = []
    for line in csvData:
        csvArray.append(line)

    print 'Starting old data import'
    global UNREAD_LINE_COUNT
    line_count = 1
    for line in csvArray[line_count:]:
        line_count += 1
        if line == ['-----']:
            print 'Finished with old data'
            break
        else: 
            UNREAD_LINE_COUNT = UNREAD_LINE_COUNT + 1
            #print line

    print 'Starting new data import'
    for line in csvArray[line_count:]:
        line_data = [get_category(line[0]), get_box_size(line[1]), get_box_weight(line[1]), get_items(line[2]), get_date(line[3])]
        global READ_LINE_COUNT
        READ_LINE_COUNT = READ_LINE_COUNT + 1
        #print line_data
    print 'Finished new data import'


def main():
    boxes = Box.objects.all()
    boxes.delete()
    for arg in sys.argv[1:]: #the script is the first arguement so we ignore it
        if (".csv" in arg): #Check if file is of csv format otherwise don't try to parse it
            importer(arg)
        else: 
            print("WARNING - File is of not .csv format, skipping parse.")
    print 'There were ' + str(ERROR_COUNT) + ' errors encountered importing'
    print 'There were ' + str(READ_LINE_COUNT) + ' new lines imported'
    print 'There were ' + str(UNREAD_LINE_COUNT) + ' old lines not imported'

#Specifying entry point to the script
if __name__ == '__main__':
    main()