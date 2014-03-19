import csv
import MySQLdb as db
import time
import re
import os, sys
import pytz
sys.path.append('/var/www/MediVol/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from inventory.models import Box
from catalog.models import Category
from datetime import datetime

NO_EXPIRATION = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)

#Title: CSV Importer 
#Description: Takes an existing CSV file containing inventory information and loads 
#the information into a MySQL Database 
#Author: Medivol - An RIT Senior Project

def get_box_size(box_size_weight):
    #print(box_size_weight)
    UNKNOWN_BOX_SIZE = "U"
    if (box_size_weight == ""): 
        return UNKNOWN_BOX_SIZE
    elif (re.match("^[LS] ", box_size_weight)):
        return box_size_weight[:1]
    elif (re.match("^[LS]-", box_size_weight)):
        return box_size_weight[0]
    elif (re.match("^\?\?", box_size_weight) or re.match("^\d", box_size_weight)):
        return UNKNOWN_BOX_SIZE
    elif (re.match("^[LS]\d{2}\.\d\Z", box_size_weight)):
        return box_size_weight[0]
    elif (re.match("^[LS]\d{2}lbs\Z", box_size_weight)):
        return box_size_weight[0]
    else:
        print ("The box size " + box_size_weight + " was not handeled right")
        return UNKNOWN_BOX_SIZE

def get_box_weight(box_size_weight):
    if (box_size_weight == ""): 
        return None

    splitString = None

    if(re.match("^\d{1,2}(\.\d)? lbs\.\Z", box_size_weight) is not None):
        return str(box_size_weight[:2])
    elif(re.match("^[LS] - \d{1,2} lbs\.\Z", box_size_weight) is not None):
        return box_size_weight.split(" ")[2]
    elif(re.match("^[LS]\d{1,2}lbs\Z", box_size_weight) is not None):
        return str(box_size_weight[1:3])
    elif(re.match("^[LS] - \d{1,2}\.\d lbs\.\Z", box_size_weight) is not None):
        return box_size_weight.split(" ")[2]
    elif(re.match("^[LS] -  \d{1,2}\.\d lbs\.\Z", box_size_weight) is not None):
        return box_size_weight.split(" ")[3]
    elif(re.match("^\?\? - \d{1,2} lbs\.\Z", box_size_weight) is not None):
        return box_size_weight.split(" ")[2]
    elif(re.match("^\?\? - \d{1,2}\.\d lbs\.\Z", box_size_weight) is not None):
        return box_size_weight.split(" ")[2]
    elif(re.match("^[LS] - \?\?", box_size_weight) is not None):
        return None
    elif(re.match("^[LS] \d{1,2}\.\d\Z", box_size_weight)):
        return box_size_weight.split(" ")[1]
    elif(re.match("^[LS] - \d{2}\.\d lbs\Z", box_size_weight)):
        return box_size_weight.split(" ")[2]
    elif(re.match("^[LS] \d{2}\.\d lbs\Z", box_size_weight)):
        return box_size_weight.split(" ")[1]
    elif(re.match("^[LS]\d{2}\.\d\Z", box_size_weight)):
        return box_size_weight[1:]
    elif(re.match("^[LS] \d{2} lbs\Z", box_size_weight)):
        return box_size_weight.split(" ")[1]
    elif(re.match("^[LS]-\d{2}lbs\Z", box_size_weight)):
        return box_size_weight[2:4]
    elif(re.match("^[LS] \d{2}lbs\Z", box_size_weight)):
        return (box_size_weight[2:4])
    elif(re.match("^[LS] \d{2}\.\dlbs\Z", box_size_weight)):
        return (box_size_weight[2:6])
    elif(re.match("^[LS]\-\d{2}\.\dlbs\Z", box_size_weight)):
        return (box_size_weight[2:6])
    elif(re.match("^[LS]\-\d{2}\.\dlbs\.\Z", box_size_weight)):
        return (box_size_weight[2:6])
    elif(re.match("^[LS] \-\d{2}\.\dlbs\Z", box_size_weight)):
        return (box_size_weight[3:7])
    elif(re.match("^[LS] \-\d{2}lbs\Z", box_size_weight)):
        return (box_size_weight[3:5])
    elif(re.match("^[LS] \d\.\d lbs\Z", box_size_weight)):
        return (box_size_weight[2:5])
    elif(re.match("^[LS] \d{2} lbs\.\Z", box_size_weight)):
        return (box_size_weight[2:4])
    elif(re.match("^[LS] \- \d{2}lbs\Z", box_size_weight)):
        return (box_size_weight[4:6])
    elif(re.match("^[LS] \d{2}\.\dLBS\Z", box_size_weight)):
        return (box_size_weight[2:6])
    elif(re.match("^[LS]  \d{2}\.\dlbs\Z", box_size_weight)):
        return (box_size_weight[3:7])
    elif(re.match("^\?\? \- \d{2}lbs\Z", box_size_weight)):
        return (box_size_weight[5:7])
    elif(re.match("^\?\? \- \d{2}\.\dlbs\Z", box_size_weight)):
        return (box_size_weight[5:9])
    elif(re.match("^[LS] \- \d{2}lbs\.\Z", box_size_weight)):
        return (box_size_weight[4:6])
    elif(re.match("^[LS] \- \d{2}\.\dlbs\Z", box_size_weight)):
        return (box_size_weight[4:8])
    elif(re.match("^[LS] \dlbs\Z", box_size_weight)):
        return (box_size_weight[2:3])
    #elif(re.match("^[LS] \dlbs\Z", box_size_weight)):
    #    print (box_size_weight[2:3])
    #    return None
    else: 
        print ("The weight " + box_size_weight + " was not handeled right")
        return None  

    boxSize = splitString[0].strip()
    boxWeight = splitString[1].lower().replace('lbs', '').replace(' .', '').strip()

    if ("?" in boxSize or boxSize == ""):
        boxSize = "U" 

    if ("?" in boxWeight or boxWeight == ""): 
        boxWeight = None

    #return boxSize 
    return boxWeight

#This is the importer method which establishes a connection with the MySQL Database and 
#tries to perform an import of a CSV file.
def importer(filepath):
    starttime = time.time()
    #Python complains without the rU(universal new line) option when opening the CSV file so this needs to be there. 
    csvData = csv.reader(file(filepath, 'rU'), delimiter = ',', dialect=csv.excel_tab)

    #for each row in the csv file add a row to the databasa column 
    rownum = 1 
    for row in csvData: 
        if (rownum != 1):
            validatedRow = validate_import_row(row, rownum)
            if (validatedRow != None):  
                box = Box(box_id=validatedRow[0], box_size=validatedRow[1], weight=validatedRow[2], 
                    old_contents=validatedRow[3], old_expiration=validatedRow[4], entered_date=validatedRow[5], 
                    reserved_for=validatedRow[6], shipped_to=validatedRow[7], box_date=validatedRow[8], 
                    audit=validatedRow[9], box_category=Category.objects.get(letter=validatedRow[10]), 
                    initials='old', old_box_flag=True)
                box.save() 
        rownum += 1

    endtime = time.time()
    totaltime = endtime - starttime #To have some insight into the total import time, it is not totally accurate but a good estimate.

    return("Import complete of " + filepath + "\nImport Statistics:\nImported " + str(rownum) + " rows\nTotal time " +\
          str(totaltime))

#This method runs a validation on all the column data of a row in a CSV file 
#If the column is deemed valid then it will be added to a list that is returned 
#for the Importer method to use it to insert into the MySQL Database  
#The indexing of the row variable passed in is in accordance with the excel 
#headers in the old excel based storage of the inventory. 
def validate_import_row(row, rownum):
    validRow = [None]*11
    #print("Validating Row...")

    boxSizeWeight = row[1]
    #Check if row does not need to be further processed  
    if (row[0] == ""):
        #print("Row %s is missing a box id and needs to be removed from the import file." % (rownum))
        validRow = None
    elif(row[1] == '' and row[2] == '' and row[3] == ''):
        print("Row %s is missing fields and will not be processed for validation. Error 1" % (rownum))
        validRow = None
    #elif("?" in boxSizeWeight and row[2] == '' or "?" in row[2]):
    #    print("Row %s is missing fields and will not be processed for validation. Error 2\n" % (rownum))
    #    validRow = None
    else : 
        #Box Field Validated Above 
        if(" " in row[0]):
            validRow[0] = row[0].split(" ")[0]
            print(row[0] + " needed spliting")
        else:
            validRow[0] = row[0]

        #Validating BoxSizeWeightField
        validRow[1] = get_box_size(row[1])
        validRow[2] = get_box_weight(row[1])
    
        #Validating Box Contents Field 
        if ("?" not in row[2]):
            validRow[3] = row[2]
        else: 
            validRow[3] = ""
    
        if (row[2] != ""): 
            validRow[3] = row[2]

        #Validating Expiration Field
        if ("NO EXP" in row[3].upper() or row[3].strip() == ""):
            #TODO Split NO_EXP and unknow exp
            validRow[4] = NO_EXPIRATION
        else: 
            validRow[4] = validate_and_convert_date(row[3])
    
        #Validating Entered Field 
        validRow[5] = validate_and_convert_date(row[4])
    
        #No validation checking for reserved for
        validRow[6] = row[5]
    
        #No validation checking for Shipped To for
        validRow[7] = row[6]
    
        #Validating Date Field 
        validRow[8] = validate_and_convert_date(row[7])

        #TODO read from documents instead
        validRow[9] = 1

        #Set the category to the first letter in the id
        validRow[10] = validRow[0].strip('0123456789')
        if (validRow[10] == "AA" or validRow[10] == "BB" or validRow[10] == "CC" or validRow[10] == "DD"):
            validRow[10] = 'Y'
            validRow[0] = 'Y'+validRow[0][2:]

        #print("Row Validation Complete\n")
        #print(validRow)

    return validRow 

#This methods check for two date formats of mm/dd/yyyy and mm/yyyy. 
#If the input matches any of the two formats then it will convert that into a valid
#MySQL datetime string
def validate_and_convert_date(date):
    date = date.replace(' ', '')
    validatedDate = None
    mm_dd_yyyy = re.match("^\d{1,2}\/\d{1,2}\/\d{4}\Z", date) #Testing by regular expression here for format of mm/dd/yyyy
    mm_yyyy = re.match("^\d{1,2}\/\d{4}\Z", date) #Testing by regular expression here for format of mm/yyyy
    yyyy_yyyy = re.match("^\d{4}\W+\d{4}\Z", date) #matches the format yyyy-yyyy
    yyyy = re.match("^\d{4}\Z", date)
    leads_m_d_yyyy = re.match("^\d\/\d\/\d{4}", date)
    leads_m_dd_yyyy = re.match("^\d\/\d{2}\/\d{4}", date)
    leads_mm_d_yyyy = re.match("^\d{2}\/\d\/\d{4}", date)
    bad_data_only_numbers = re.match("^\d*\Z", date)
    bad_data_ddcd = re.match("^\d{2},\d\Z", date)
    date_c_date = re.match("^\d/\d{4},\d/\d{4}\Z", date)
    exp_m_yyyy = re.match("^exp\d/\d{4}\Z", date)
    exp_mm_yyyy = re.match("^exp\d{2}/\d{4}\Z", date)
    earliest_m_yyyy = re.match("^earliest\d/\d{4}\Z", date)
    earliest_mm_yyyy = re.match("^earliest\d{2}/\d{4}\Z", date)
    earliestexp_mm_yyyy = re.match("^earliestexp\d{2}/\d{4}\Z", date)
    hashtag = re.match("^#+\Z", date)
    sterileexp_mm_yyyy = re.match("^sterileexp\d{2}/\d{4}\Z", date)
    noexp = re.match("^noexp\Z", date)
    na = re.match("^NA\Z", date)

    if(date is None or date.strip() is "" or "Clinton" in date):
        validatedDate = NO_EXPIRATION
    elif (mm_dd_yyyy is not None):
        formattedDate = date.split("/")
        validatedDate = datetime(int(formattedDate[2]),int(formattedDate[0]),int(formattedDate[1]), 0, 0, 0, 0, pytz.UTC)
    elif (mm_yyyy is not None):  
        formattedDate = date.split("/")
        validatedDate = datetime(int(formattedDate[1]),int(formattedDate[0]), 1, 0, 0, 0, 0, pytz.UTC)
    elif (yyyy_yyyy is not None):
        validatedDate = datetime(int(date[:4]), 1, 1, 0, 0, 0, 0, pytz.UTC)
    elif (yyyy is not None):
        validatedDate = datetime(int(date), 1, 1, 0, 0, 0, 0, pytz.UTC)
    elif(leads_m_d_yyyy is not None):
        validatedDate = datetime(int(date[4:8]), int(date[:1]), int(date[2:3]), 0, 0, 0, 0, pytz.UTC)
    elif(leads_m_dd_yyyy is not None):
        validatedDate = datetime(int(date[5:9]), int(date[:1]), int(date[2:4]), 0, 0, 0, 0, pytz.UTC)
    elif(leads_mm_d_yyyy is not None):
        validatedDate = datetime(int(date[5:9]), int(date[:2]), int(date[3:4]), 0, 0, 0, 0, pytz.UTC)
    elif(bad_data_only_numbers is not None):
        validatedDate = None
    elif(bad_data_ddcd is not None):
        validatedDate = None
    elif(date_c_date is not None):
        validatedDate = datetime(int(date[2:6]), int(date[0]), 1, 0, 0, 0, 0, pytz.UTC)
    elif(exp_m_yyyy is not None):
        validatedDate = datetime(int(date[5:]), int(date[3]), 1, 0, 0, 0, 0, pytz.UTC)
    elif(exp_mm_yyyy is not None):
        validatedDate = datetime(int(date[6:]), int(date[3:5]), 1, 0, 0, 0, 0, pytz.UTC)
    elif(earliest_m_yyyy is not None):
        validatedDate = datetime(int(date[10:]), int(date[8]), 1, 0, 0, 0, 0, pytz.UTC)
    elif(earliest_mm_yyyy is not None):
        validatedDate = datetime(int(date[11:]), int(date[8:10]), 1, 0, 0, 0, 0, pytz.UTC)
    elif(earliestexp_mm_yyyy is not None):
        validatedDate = datetime(int(date[14:]), int(date[11:13]), 1, 0, 0, 0, 0, pytz.UTC)
    elif(hashtag is not None):
        validatedDate = None
    elif(sterileexp_mm_yyyy is not None):
        validatedDate = datetime(int(date[13:]), int(date[10:12]), 1, 0, 0, 0, 0, pytz.UTC)
    elif(noexp is not None):
        validatedDate = NO_EXPIRATION
    elif(na is not None):
        validatedDate = NO_EXPIRATION
    else:
        #TODO figure out if any of this case exist
        print("This date was not handeled right: " + date)
        validatedDate = NO_EXPIRATION

    return validatedDate

def main():
    boxes = Box.objects.all()
    boxes.delete()
    for arg in sys.argv[1:]: #the script is the first arguement so we ignore it
        if (".csv" in arg): #Check if file is of csv format otherwise don't try to parse it
            print("\nStarting " + arg + " Import to MySQL Database") 
            importer(arg)
        else: 
            print("WARNING - File is of not .csv format, skipping parse.")

#Specifying entry point to the script
if __name__ == '__main__':
    main()
