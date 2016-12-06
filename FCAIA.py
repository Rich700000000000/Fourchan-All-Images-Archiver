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

#In 5.2, I added a UserAgent to hopefully combat the rate limiting.
def getPageSoup(pageurl):
	user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"
	req = urllib.request.Request(pageurl, headers={'User-Agent': user_agent})
	content = urllib.request.urlopen(req).read()
	soup = (BeautifulSoup(content))
	return soup

#From now on, all the values will be stored in arrays. At some point it's going to dump to a log
#file, and this will help.
def getNameNumUrls(pgs):
	fileName   = []
	fileNumber = []
	fileURL    = []
	#So yeah, I completely remade the extractor function, 
	for link in pgs.find_all('a', {'target': '_blank'}):
	    realFilenameString = (str(link))  
	    if ("fileThumb") not in realFilenameString:
		    if ("i.4cdn.org") in realFilenameString:
		       #Connects all the values. 
		       fileName.append(realFilenameString.split('">')[1][:-4])
		       fileNumber.append(realFilenameString.split("rg/")[1].split(".")[0].split("/")[1])
		       fileURL.append(realFilenameString.split('" t')[0][8:].replace("//", "https://")[1:])
	return fileName, fileNumber, fileURL


#A filecount function I got from StackOverflow.
def filecount(DIR): return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

#The completed fucnction for constructing 4chan folders. 
def makeChanDir(soup):
    name = (soup.title.string).strip()
    boardOld,threadRaw,dis,chan = name.split(" - ")
    board = boardOld.replace("/", " ").upper()
    alphabet = string.ascii_letters + string.digits + ("'[];=+~()#&"",.!-_ ")
    thread = ''
    for char in threadRaw: 
        if char in alphabet:
           thread+=char
           newName = ("Site-[ 4chan ] - Board-[" + board + "] - Thread-[ " + thread +" ]")
    return newName

def main():
	#The actual constructor, to make the folders.
	try: 
	   url = sys.argv[1]
	except IndexError:
	   print ("Error: No URL Found")
	   raise SystemExit

	soup = getPageSoup(url)
	newName = makeChanDir(soup)
	dcwd = ((os.getcwd()) + "/" + newName)
	if os.path.exists(dcwd):
	   fileInt = filecount(dcwd)
	else:
	   fileInt = 0 
	   os.makedirs(dcwd)

	fileName, fileNumber, fileURL = getNameNumUrls(soup)
	#Sets up the numbering, even if the program restarts.
	threadCount = len(fileName)
	if fileInt == 0:
	   loopCount = (fileInt)
	   newStart = True
	elif fileInt > 3:
	   loopCount = (fileInt - 1)
	   newStart = False


	#The Already downloaded Images
	print("Folder Name: " + str(newName))
	print("AD Images:   " + str(fileInt))
	#And the new downloader, as well:
	while loopCount < threadCount:



	      print("Image:       " + (str(loopCount + 1)) + "/" + (str(threadCount)))


	      fileNameTemp        =  fileName[loopCount]
	      fileNumberTemp      =  fileNumber[loopCount]
	      fileURLTemp         =  fileURL[loopCount]



	      print("File Name:   " + fileNameTemp)
	      print("File Number: " + fileNumberTemp)
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
	      
	      loopCount += 1
 
main()
