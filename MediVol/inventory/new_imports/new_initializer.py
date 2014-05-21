import os, sys
sys.path.append('/var/www/MediVol/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")

import csv
import pytz
from datetime import datetime
import re

from catalog.models import Category, BoxName, Item
from inventory.models import Box, Contents

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
    if re.match("^[LS] - +\d{1,2}(\.\d)? lbs\.?\Z", data.strip()):
        return data.strip()[0]
    elif data.strip() == '':
        return 'U'
    else:
        print '[ERROR] Could not import size: ' + data
        global ERROR_COUNT
        ERROR_COUNT = ERROR_COUNT + 1
        return 'U'

def get_box_weight(data):
    if re.match("^[LS] - +\d{1,2}(\.\d)? lbs\.?", data.strip()):
        return float(data.split('-')[1].strip().split(' ')[0])
    elif data.strip() == '':
        return 0.0
    else:
        print '[ERROR] Could not import weight: ' + data
        global ERROR_COUNT
        ERROR_COUNT = ERROR_COUNT + 1
        return 0.0

def add_item(item, box_name_text):
    try:
        box_name = BoxName.objects.get(name=box_name_text)
    except:
        print '[ERROR] BoxName not found'
    try:    
        item = Item.objects.get(name=item, box_name=box_name)
    except:
        item = Item(name=item, box_name=box_name)
        item.save()
    return item

def get_items(data):
    if re.match("^.*:.*\Z", data.strip()) is not None:
        global ERROR_COUNT
        box_name_text = data.split(":")[0].strip()
        try:
            box_name = BoxName.objects.get(name=box_name_text)

        except:
            return data

        items = data[len(box_name_text)+2:].strip()
        if re.match("^(.*;)*.*\Z", items):
            item_list = items.split(";")
            finished_items = []
            for item in item_list:
                if re.match('^\d+ [a-z A-Z/&:\'\.]+\Z', item.strip()):
                    cleaned_item = ' '.join(item.strip().split(' ')[1:])
                    finished_items.append(add_item(cleaned_item, box_name_text))
                elif re.match('^[a-z A-Z/&:\'\.\-"]+\Z', item.strip()):
                    cleaned_item = item.strip()
                    finished_items.append(add_item(cleaned_item, box_name_text))
                elif re.match('^[a-z A-Z/&:\'\.\-"]+ [Xx]\d+\Z', item.strip()):
                    cleaned_item = ' '.join(item.strip().split(' ')[:-1])
                    finished_items.append(add_item(cleaned_item, box_name_text))
                elif re.match('^[a-z A-Z/&:\'\.\-"]+ \(\d+\)\Z', item.strip()):
                    cleaned_item = ' '.join(item.strip().split(' ')[:-1])
                    finished_items.append(add_item(cleaned_item, box_name_text))
                else:
                    return items
                return finished_items
        else:
            print '[ERROR] reading line ' + data
            ERROR_COUNT = ERROR_COUNT + 1
            return None

    else:
        return data

def get_date(data):
    if re.match('^\d{1,2}/\d{4}\Z', data.strip()) is not None:
        formattedDate = data.strip().split("/")
        validatedDate = datetime(int(formattedDate[1]),int(formattedDate[0]),1, 0, 0, 0, 0, pytz.UTC)
        return validatedDate
    elif re.match('^No EXP\Z',data.strip()):
        return None
    elif re.match('^No Exp\Z', data.strip()):
        return None
    elif re.match('^\Z', data.strip()):
        return None
    elif data.strip() == 'EXPIRED':
        return datetime(2000, 1, 1, 0, 0, 0, 0, pytz.UTC)
    else:
        print '[ERROR] Could not import date: ' + data
        global ERROR_COUNT
        ERROR_COUNT = ERROR_COUNT + 1
        return UNKNOWN_EXPIRATION

def importer(file_name):
    print("\nStarting " + file_name + " Import to MySQL Database") 

    errors = ''
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
        line_data = [line[0],get_category(line[0]), get_box_size(line[1]), get_box_weight(line[1]), get_items(line[2]), get_date(line[3])]

        valid = True
        for data in line_data[:-1]:
            if data is None:
                valid = False
                break
        if valid:
            if type(line_data[4]) is list and line[0] != '':
                try:
                    box = Box(box_id=line_data[0], box_category=line_data[1], box_size=line_data[2], weight=line_data[3], old_expiration=line_data[5], old_box_flag=True)
                    box.save()
                    for item in line_data[4]:
                        box_contents = Contents(box_within=box, item=item)
                        box_contents.save()
                except:
                    global ERROR_COUNT
                    ERROR_COUNT = ERROR_COUNT + 1
                    #print '[ERROR] save failed'
                    print 'HERE: ' + str(line)
                    errors = errors + (','.join(line) + '\n')
            else:
                try:
                    box = Box(box_id=line_data[0], box_category=line_data[1], box_size=line_data[2], weight=line_data[3], old_expiration=line_data[5], old_contents=line_data[4], old_box_flag=True)
                    box.save()
                except:
                    global ERROR_COUNT
                    ERROR_COUNT = ERROR_COUNT + 1
                    #print '[ERROR] save failed'
                    print 'HERE: ' + str(line)
                    errors = errors + (','.join(line) + '\n')

        global READ_LINE_COUNT
        READ_LINE_COUNT = READ_LINE_COUNT + 1
        #print line_data
    print 'Finished new data import'
    return errors


def main():
    boxes = Box.objects.all()
    boxes.delete()
    error_print_out = open('Errors.txt', 'w')
    errors = ''


    for arg in sys.argv[1:]: #the script is the first arguement so we ignore it
        if (".csv" in arg): #Check if file is of csv format otherwise don't try to parse it
            errors = errors + importer(arg)
        else: 
            print("WARNING - File is of not .csv format, skipping parse.")
    print 'There were ' + str(ERROR_COUNT) + ' errors encountered importing'
    print 'There were ' + str(READ_LINE_COUNT) + ' new lines imported'
    print 'There were ' + str(UNREAD_LINE_COUNT) + ' old lines not imported'
    error_print_out.write(errors)

#Specifying entry point to the script
if __name__ == '__main__':
    main()
