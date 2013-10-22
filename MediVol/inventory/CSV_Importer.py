import csv
import MySQLdb as db
import time
import re
import sys
import os, sys
sys.path.append('/var/www/MediVol/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediVol.settings")
from django.db import models
from inventory.models import Box

NO_EXPIRATION = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime("01 01 1970", "%m %d %Y"))

#Title: CSV Importer 
#Description: Takes an existing CSV file containing inventory information and loads 
#the information into a MySQL Database 
#Author: Medivol - An RIT Senior Project

#This is the importer method which establishes a connection with the MySQL Database and 
#tries to perform an import of a CSV file.
def importer(filepath):
    starttime = time.time()
    #Python complains without the rU(universal new line) option when opening the CSV file so this needs to be there. 
    csvData = csv.reader(file(filepath, 'rU'), delimiter = ',', dialect=csv.excel_tab)

    print("Starting CSV File Import to MySQL Database")

    #for each row in the csv file add a row to the databasa column 
    rownum = 1 
    for row in csvData: 
        if (rownum != 1):
            validatedRow = validate_import_row(row, rownum)
            if (validatedRow != None):  
                print (validatedRow[9])
                box = Box(box_id=validatedRow[0], box_size=validatedRow[1], weight=validatedRow[2], contents=validatedRow[3],
                    expiration=validatedRow[4], entered_date=validatedRow[5], reserved_for=validatedRow[6], shipped_to=validatedRow[7],
                    box_date=validatedRow[8], audit=validatedRow[9])
                box.save() 
        rownum += 1

    endtime = time.time()
    totaltime = endtime - starttime #To have some insight into the total import time, it is not totally accurate but a good estimate.
    
    print("Import complete")
    print ("Import Statistics:")
    print ("Imported " + str(rownum) + " rows")
    print ("Total time " + str(totaltime))

#This method runs a validation on all the column data of a row in a CSV file 
#If the column is deemed valid then it will be added to a list that is returned 
#for the Importer method to use it to insert into the MySQL Database  
#The indexing of the row variable passed in is in accordance with the excel 
#headers in the old excel based storage of the inventory. 
def validate_import_row(row, rownum):

    validRow = [None]*10
    print("Validating Row...")

    boxSizeWeight = row[1]

    #Check if row does not need to be further processed  
    if (row[0] == ""):
        print("Row %s is missing fields and will not be processed for validation. \n" % (rownum))
        validRow = None
    elif(row[1] == '' and row[2] == '' and row[3] == ''):
        print("Row %s is missing fields and will not be processed for validation. \n" % (rownum))
        validRow = None
    elif("?" in boxSizeWeight and row[2] == '' or "?" in row[2]):
        print("Row %s is missing fields and will not be processed for validation. \n" % (rownum))
        validRow = None
    else : 
        #Box Field Validated Above 
        validRow[0] = row[0]

        #Validating BoxSizeWeightField
        splitString = None

        if (boxSizeWeight == ""): 
            validRow[1] = "U"
            validRow[2] = "0.0"
        else:
            if ("-" in boxSizeWeight): 
                splitString = boxSizeWeight.split('-')
            else: 
                splitString = boxSizeWeight.split(' ')  
    
            boxSize = splitString[0].strip()
            boxWeight = splitString[1].replace('lbs', '').replace(' .', '').strip()
    
            if ("?" in boxSize or boxSize == ""):
                boxSize = "" 
    
            if ("?" in boxWeight or boxWeight == ""): 
                boxWeight = 0
        
            validRow[1] = boxSize 
            validRow[2] = boxWeight
    
        #Validating Box Contents Field 
        if ("?" not in row[2]):
            validRow[3] = row[2]
        else: 
            validRow[3] = ""
    
        if (row[2] != ""): 
            validRow[3] = row[2]

        #Validating Expiration Field
        if ("NO EXP" in row[3] or row[3] == ""):
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

        print("Row Validation Complete\n")
        print(validRow)

    return validRow 

#This methods check for two date formats of mm/dd/yyyy and mm/yyyy. 
#If the input matches any of the two formats then it will convert that into a valid
#MySQL datetime string
def validate_and_convert_date(date):

    validatedDate = None
    match = re.match("^\d+\W+\d+\W+\d+\Z", date) #Testing by regular expression here for format of mm/dd/yyyy
    match2 = re.match("^\d+\W+\d+\Z", date) #Testing by regular expression here for format of mm/yyyy

    if (match is None):
        #TODO figure out if any of this case exist
        validatedDate = NO_EXPIRATION
    else:
        formattedTime = time.strptime(date, "%m/%d/%Y")
        validatedDate = time.strftime('%Y-%m-%d %H:%M:%S', formattedTime) #Convert to mysql datetime

    if (match2 is not None):  
        formattedTime = time.strptime(date, "%m/%Y")
        validatedDate = time.strftime('%Y-%m-%d %H:%M:%S', formattedTime) #Convert to mysql datetime

    return validatedDate

def main():
    for box in Box.objects.all():
        box.delete()
    counter = 0 
    for arg in sys.argv: 
        if (counter != 0): #Skip the first index of the argument list because it is the script name
            if (".csv" in arg): #Check if file is of csv format otherwise don't try to parse it 
                importer(arg)
            else: 
                print("WARNING - File is of not .csv format, skipping parse.")
        counter+=1

#Specifying entry point to the script
if __name__ == '__main__':
    main()