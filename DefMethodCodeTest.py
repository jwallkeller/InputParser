import sys
import os
from datetime import datetime
import re
import filecmp

## Person is an object with the attributes:
## firstName
## lastName
## middleInitial
## gender
## favoriteColor
## dateOfBirth
class Person:
    def __init__(self, firstName, lastName, middleInitial, gender, favoriteColor, dateOfBirth):
        self.firstName = firstName
        self.lastName = lastName
        self.middleInitial = middleInitial
        self.gender = gender
        self.favoriteColor = favoriteColor
        self.dateOfBirth = dateOfBirth

## changeGenderOutput takes the gender letter that is provided and changes it to the corresponding word to be returned
## Input Parameters: gender
## Returns: newGender
def changeGenderOutput(gender):
    if gender == "F":
        newGender = "Female"
    elif gender == "M":
        newGender = "Male"
    return newGender

## printOutput takes a sorted list of entries and outputs to the command line and to a file in the correct format
## Input Parameters: entries, outputFile
def printOutput(entries):
    for person in entries:
        print(person.lastName,person.firstName, person.gender, person.dateOfBirth, person.favoriteColor)

if len( sys.argv ) <= 1: ## check if no arguments were passed
    print("ERROR: No arguments provided")
    print("Please provide the path to the input directory")
elif len( sys.argv ) > 2: ## check if too many arguments were passed
    print("ERROR: Too many arguments provided")
    print("Please only provide the path to the input directory")
elif len( sys.argv ) > 1:
    pathToInputFolder = sys.argv[1]

    entries = []

    ## check if directory exists
    if os.path.isdir(pathToInputFolder):
        folder_content = os.listdir(pathToInputFolder)
        ## check if directory is empty
        if len(folder_content) == 0 :
            print("WARNING: Input Directory is empty.")
        else:
            for filename in folder_content:
                ## check if the input files are valid text files
                if '.txt' not in filename:
                    print(filename, "is not a valid file.")
                else:
                    pathToFile = pathToInputFolder + '/' + filename
                    textFile = open(pathToFile, 'r')

                    while True:
                        line = textFile.readline().strip()
                        if not line:
                            break

                        ## check that line matches expected format of comma text file
                        if re.match(r"^[a-zA-Z]+[,]\s[a-zA-Z]+[,]\s[a-zA-Z]+[,]\s[a-zA-Z]+[,]\s([1-9]|1[0-2])[/]([1-9]|[12][0-9]|3[01])[/]\d{4}$",line):
                            entry = line.split(', ')
                            p = Person(entry[1], entry[0], "", entry[2], entry[3], entry[4])
                            entries.append(p)
                        ## check that line matches expected format of pipe text file
                        elif re.match(r"^[a-zA-Z]+\s[|]\s[a-zA-Z]+\s[|]\s[a-zA-Z]\s[|]\s[a-zA-Z]\s[|]\s[a-zA-Z]+\s[|]\s([1-9]|1[0-2])-([1-9]|[12][0-9]|3[01])-\d{4}$",line):
                            entry = line.split(' | ')
                            p = Person(entry[1], entry[0], entry[2], entry[3], entry[4], entry[5].replace('-','/'))
                            ## change gender from letter to word
                            p.gender = changeGenderOutput(p.gender)
                            entries.append(p)
                        ## check that line matches expected format of space text file
                        elif re.match(r"^[a-zA-Z]+\s[a-zA-Z]+\s[a-zA-Z]\s[a-zA-Z]\s([1-9]|1[0-2])-([1-9]|[12][0-9]|3[01])-\d{4}\s[a-zA-Z]+$",line):
                            entry = line.split(' ')
                            p = Person(entry[1], entry[0], entry[2], entry[3], entry[5], entry[4].replace('-','/'))
                            ## change gender from letter to word
                            p.gender = changeGenderOutput(p.gender)
                            entries.append(p)
                        ## if no expect format is detected
                        else:
                            print("ERROR: Invalid delimeter detected for", line, "in", filename)

                    textFile.close()

            ## check if any entries were added to the list
            if len(entries) > 0:
                ## sort the entries list by gender first and then lastName
                sortedGenderEntries = sorted(entries, key=lambda x: (x.gender, x.lastName))
                print("Output 1:")
                printOutput(sortedGenderEntries)
                print("")

                ## sort the entries list by birthday first and then lastName
                birthdayEntries = sorted(entries, key=lambda x: (datetime.strptime(x.dateOfBirth, "%m/%d/%Y"), x.lastName))
                print("Output 2:")
                printOutput(birthdayEntries)
                print("")

                ## sort the entries list by last name is descending order
                reverseLastNameEntries = sorted(entries, key=lambda x: x.lastName, reverse=True)
                print("Output 3:")
                printOutput(reverseLastNameEntries)
            else:
                print("No valid entries found.")
    else:
        print("ERROR: Input directory does not exist.")
        print("Pleae provide a valid input directory")





