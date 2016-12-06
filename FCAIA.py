#!/usr/bin/env python3

#The lybraries required for this code: The first three are downloaders, the fourth for the file io, 5 & 6 are handleers and sys is for the command line input.
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import shutil
import urllib
import time
import os
import sys
import string
import os.path

#Gets the command line input and turns it into a url.
try: 
   url = sys.argv[1]
except IndexError:
   print ("Error: No URL Found")
   raise SystemExit

#In 5.2, I added a UserAgent to hopefully combat the rate limiting.
user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"
req = urllib.request.Request(url, headers={'User-Agent': user_agent})
content = urllib.request.urlopen(req).read()
soup = (BeautifulSoup(content))


#From now on, all the values will be stored in arrays. At some point it's going to dump to a log
#file, and this will help.
fileName   = []
fileNumber = []
fileURL    = []
 

#So yeah, I completely remade the extractor function, 
for link in soup.find_all('a', {'target': '_blank'}):
    ltm = (link)
    realFilenameString = (str(ltm))  
    if ("fileThumb") not in realFilenameString:
            fileTitle = str(realFilenameString)
            if ("i.4cdn.org") in fileTitle:
               fileString = (fileTitle)
               #Connects all the values. 
               fileName.append(fileString.split('">')[1][:-4])
               fileNumber.append(fileString.split("rg/")[1].split(".")[0].split("/")[1])
               fileURL.append(fileString.split('" t')[0][8:].replace("//", "https://")[1:])


#A filecount function I got from StackOverflow.
def filecount(DIR):
     return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

#The completed fucnction for constructing 4chan folders. 
def makeChanDir(soup):
    nameA = (soup.title.string)
    name = nameA.strip()
    boardOld,threadRaw,dis,chan = name.split(" - ")
    board = boardOld.replace("/", " ").upper()
    alphabet = string.ascii_letters + string.digits + ("'[];=+~()#&,.!-_ ")
    thread = ''
    for char in threadRaw: 
        if char in alphabet:
           thread+=char
           newName = ("Site-[ 4chan ] - Board-[" + board + "] - Thread-[ " + thread +" ]")
    return(newName)


#A filecount function I got from StackOverflow.
def filecount(DIR):
     return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])


#The actual constructor, to make the folders.
newName = makeChanDir(soup)
cwd = (os.getcwd())
dcwd = (cwd + "/" + newName)
if os.path.exists(dcwd):
   fileInt = filecount(dcwd)
else:
   fileInt = 0 
   os.makedirs(dcwd)
 

#Sets up the numbering, even if the program restarts.
threadCount = len(fileName)
if fileInt == 0:
   loopCount = (fileInt)
   newStart = True
elif fileInt <= 3:
   loopCount = 0
   newStart = False
elif fileInt > 3:
   loopCount = (fileInt - 2)
   newStart = False


#The Already downloaded Images
print("AD Images:   " + str(fileInt))



#And the new downloader, as well:
while loopCount < threadCount:



      print("Image:       " + (str(loopCount + 1)) + "/" + (str(threadCount)))


      fileNameTemp    =  fileName[loopCount]
      print("File Name:   " + fileNameTemp)

      fileNumberTemp  =  fileNumber[loopCount]
      print("File Number: " + fileNumberTemp)

      fileURLTemp         =  fileURL[loopCount]
      print("File Url:    " + fileURLTemp)

      extTR = os.path.splitext(fileNameTemp)[1]

      fileNameFinal = (fileNumberTemp + " - ON[" + fileNameTemp + "]" + extTR)

      
      print ("File:        " + fileNameFinal)

      response = requests.get(fileURLTemp, stream=1)


      with open((os.path.join(dcwd, fileNameFinal)), 'wb') as out_file:
          print ("Downloading: " + fileNameFinal)
          shutil.copyfileobj(response.raw, out_file)
      del response
      

      print ("Downloaded:  " + fileNameFinal + "\n")
      

      #For testing purposes. This will be commented out for general use.
      #time.sleep(30)

      loopCount += 1
 

