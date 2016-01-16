
#The lybraries required for this code: The first three are downloaders, the fourth for the file io, 5 & 6 are handleers and sys is for the command line input.
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import shutil
import urllib
import time
import os
import sys
#Forgot to add this.
import string

#Gets the command line input and turns it into a url.
url = sys.argv[1]

#In 5.2, I added a UserAgent to hopefully combat the rate limiting.
user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"
req = urllib.request.Request(url, headers={'User-Agent': user_agent})
content = urllib.request.urlopen(req).read()
soup = BeautifulSoup(content)


#Makes the folder, a suprisingly complex process. I should probably turn this into a function at some point.
nameA = (soup.title.string)
name = nameA.strip()
board,thread,dis,chan = name.split(" - ")
fixedBoard = board.replace("/", "_")
#Removed an excess ")" that was causing an error.
alphabet = string.ascii_letters + string.digits + "'[];=+~()#&,.!-_ "
newthread = ''
for char in thread: 
    if char in alphabet:        
        newthread+=char
newName = (newthread + " - " + fixedBoard + " - " + chan)

#A filecount function I got from StackOverflow.
def filecount(DIR):
     return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

#Extracts the HTML, and counts the number of "href"s.
link = soup.find_all('a', {'class': 'fileThumb'})      
ltc = (str(link))
picInt = ltc.count("href")
picNum = str(picInt)


#The reworked function for making the folder. 
cwd = (os.getcwd())
dcwd = (cwd + "/" + newName)
if os.path.exists(dcwd):
   fileInt = filecount(dcwd)
else:
   fileInt = 0 
   os.makedirs(dcwd)

print("AD Images:      " + (str(fileInt)))

#The BS4 function that actually extracts and downloads the urls.
for link in soup.find_all('a', {'class': 'fileThumb'}):

    ltm = (link)
    
    lti = ltm["href"]
      
    url = ("http:" + lti)

    filename = url.split('/')[-1] 

    if filename not in os.listdir(dcwd):
       
       fileInt += 1
       fileNum = str(fileInt)
       print("Image Number:   " + fileNum + "/" + picNum)
       
       
       print ("File:           " + filename)
       response = requests.get(url, stream=1)
       
       with open((os.path.join(dcwd, filename)), 'wb') as out_file:
          print ("Downloading:    " + filename)
          shutil.copyfileobj(response.raw, out_file)
       del response
       
       print ("Downloaded:     " + filename + "\n")



       

