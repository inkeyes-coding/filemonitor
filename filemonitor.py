import os
import shutil
import re

# Path containing files to be processed
startPath = "/Users/justin/demo/start/"
# Path containing directories for files to be sorted into
tvEndPath = "/Users/justin/demo/end/tv/"
# Path containing directories for files to be sorted into
movieEndPath = "/Users/justin/demo/end/movies/"
# Array of all files in the starting path
allFiles = os.listdir(startPath)


# Function to seperate and process the name of the of the content
def parse_name(inputFileName):
    # Checks if the file name contains a season id
    if re.search('(?i)S[0-9][0-9]E[0-9][0-9]', inputFileName):
        # If so, grab show name text before season id
        name = re.search('^(.*?)[Ss][0-9][0-9]', inputFileName)
    else:
        # Otherwise, grab movie name text before date
        name = re.search('^(.*?)[1-2][0-9][0-9][0-9]', inputFileName)

    # Replace all non-word chars with spaces and put that into a new string
    parsedName = re.sub('[^0-9a-zA-Z ]+', ' ', str(name.group(1)))
    # Remove any trailing space characters
    parsedName = parsedName.rstrip()
    # Force lowercase
    parsedName = parsedName.lower()
    # Capitalize the first char of each word
    parsedName = parsedName.title()

    # returns the processed show or movie name
    return parsedName


# Function to seperate and process the season or date of the of the content
def parse_numerics(inputFileName):
    # Checks if the file name contains a season id
    if re.search('(?i)S[0-9][0-9]E[0-9][0-9]', inputFileName):
        # If true, strip out just season id and return it into the form of "Season X(X)"
        season = re.search('(?i)S[0-9][0-9]', inputFileName)
        season = season.group(0)
        if season[1] == "0":
            season = season[0] + "eason " + season[2]
        else:
            season = season[0] + "eason " + season[1] + season[2]
        return season
    else:
        # Otherwise, strip out the date and return it
        date = re.search('[1-2][0-9][0-9][0-9]', inputFileName)
        date = date.group(0)
        return date


# Function responsible for checking if paths exist, creating paths, and moving files.
def move_files(parsedName, numerics, inputFileName):
    # Verify file is a tv show
    if re.search('Season', numerics):
        # Generate the path text for the "show name" and "show season" directories
        showPath = tvEndPath + parsedName
        seasonPath = showPath + "/" + numerics

        # If the show name directory doesn't exist, create it
        if not os.path.exists(showPath):
            os.makedirs(showPath)

        # If the show season directory doesn't exist, create it
        if not os.path.exists(seasonPath):
            os.makedirs(seasonPath)

        # Move the file to the correct show/season directory
        shutil.move(startPath + inputFileName,
                    seasonPath + "/" + inputFileName)

    # Otherwise the file is a movie
    else:
        # Generate the path text for the "movie name" directory
        moviePath = movieEndPath + parsedName + " " + numerics

        # If the movie name directory doesn't exist, create it
        if not os.path.exists(moviePath):
            os.makedirs(moviePath)

        # Move the file to the correct directory
        shutil.move(startPath + inputFileName, moviePath + "/" + inputFileName)


# Main program:
# This loop iterates over each file name found in the allFiles array.
# For each file name, it parses the name and date/season info and them moves the file based on that data.
for j in allFiles:
    move_files(parse_name(j), parse_numerics(j), j)
