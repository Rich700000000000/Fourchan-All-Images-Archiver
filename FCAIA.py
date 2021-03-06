#!/usr/bin/env python3
#The lybraries required for this code: The first three are downloaders, the fourth for the file io, 5 & 6 are handleers and sys is for the command line input.
import os
import re
import sys
import time
import shutil
import urllib
import string
import os.path
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

#In 5.2, I added a UserAgent to hopefully combat the rate limiting.
def getPageSoup(pageurl):
	user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/81.0.4044.138 Chrome/81.0.4044.138 Safari/537.36"
	req = urllib.request.Request(pageurl, headers={'User-Agent': user_agent})
	content = urllib.request.urlopen(req).read()
	soup = (BeautifulSoup(content, "lxml"))
	return soup

#From now on, all the values will be stored in arrays. At some point it's going to dump to a log
#file, and this will help.
def getNameNumUrls(soup):
	ltm_a = []
	ltm_b = []
	ltm_c = []
	for link in soup.find_all('div', {'class': 'fileText'}):
		ltm_a.append(link.a['href'])
		try:
			ltm_b.append(link.a['title'])
		except AttributeError: # element does not have .name attribute
			ltm_b.append(link.a.text)
		except KeyError: # element does not have a class
			ltm_b.append(link.a.text)
		fn = (re.findall(r'\d{5,20}', (link.a['href'])))[0]
		ltm_c.append(fn)


	return ltm_b, ltm_c, ltm_a 


#A filecount function.
def filecount(DIR):
	return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

#The completed fucnction for constructing 4chan folders. 
def makeChanDir(soup):
#    name = (soup.title.string).strip()
    nameA = (soup.title.string)
    name = nameA.strip()
    boardOld,threadRaw,dis,chan = name.split(" - ")
    board = boardOld.replace("/", " ").upper()
    alphabet = string.ascii_letters + string.digits + ("'[];=+~()#&"",.!-_ ")
    thread = ''
    for char in threadRaw: 
        if char in alphabet:
           thread+=char
#           newName = ("Site-[ 4chan ] - Board-[" + board + "] - Thread-[ " + thread +" ]")
           newName = ("Site-[ 4chan ] - Board-[ {} ] - Thread-[ {} ]".format(board, thread))
    return newName

#Returns a list of all of the arguments.
def getAllArgs(howOut="return"):
	allArgs = sys.argv
	allArgs = allArgs[1:]


	if howOut == "print": 
		print (len(allArgs))
		for i in allArgs: print (i)
	elif howOut == "return":
		return allArgs

#Main program function, downloads images and puts them into folders.
def everything(url):
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


	#The already downloaded Images
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


	      fileNameFinal = (fileNumberTemp + "___ON[" + fileNameTemp + "]" + extTR)

	      
	      print ("File:        " + fileNameFinal)


	      try:
	        response = requests.get("https:" + fileURLTemp, stream=1)
	        with open((os.path.join(dcwd, fileNameFinal)), 'wb') as out_file:
	          print ("Downloading: " + fileNameFinal)
	          shutil.copyfileobj(response.raw, out_file)
	        del response
	        print ("Downloaded:  " + fileNameFinal + "\n")
	      except OSError:
	       print ("Error on image: {}\n".format(fileNameFinal))
	      except urllib.error.URLError:
	       print ("Network Error on image: {}\n".format(fileNameFinal))
	      except Exception:
	       print ("Exception on image: {}\n".format(fileNameFinal))


	      
	      loopCount += 1

	return newName, threadCount

#Main function. Loops over all passed thread urls.
def main():
	r = getAllArgs()
	for n, i in enumerate(r):
		print ("Page {}: {}".format(n, i))
		e,t = everything(i)
	print ("{} files in: '{}'".format(t,e))

if __name__ == "__main__":
	main()
