# STVD-PMS
 This repo is used to extract the metadata from TV channels

# Data loader

Download data from the link: https://drive.google.com/drive/folders/1wvL6HJwhUpC1QFqRUHy1WuobupTNrCR1?usp=sharing 

Move the folder 'data' into the project directory.

# Natural Language Text Processing with XML

The first step is to extract all of the TV programs during from at 06:00 AM to 02:00 AM of a next day. However, the TV program could be error-prone due to the nameing convention and it requires some filter rules as follows:
- Ignore the program having duration is less then five minutes (<5 mins>);
- Filter out any two programs are overlapped.

Sepcifically, given a list of the xml files, the collection.csv file will be generated as following.

- Input: the list of XML file with filenames formatted yyyy-mm-dd_HHMMSS.xml
- Ouput: The list of TV programs that provided for each day based on the name of the XML file.

For example: 

Input: The file 2022-01-01_100000.xml

Ouput: List of TV programs which its starts FROM at 06:00:00 01-01-2022 TO at 02:00:00 02-01-2022

Notes: Using SHA-1 hash function for robustness of TV titles.

