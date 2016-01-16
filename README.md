Script to download all the images in a 4chan thread.

Warning: I've never used Git before, so if I accidentally screw up and wipe out everything send me a message to get it resolved.

Use:

        python3 FCAIA.py http://boards.4chan.org/g/thread/52438119/edc-every-day-carry

To Do:

* Make it incorporate the original file names into the image names.
* Make it turn the folder into an archive, storage only.
* Make it turn the folder into an archive, lossless compression.
* Make it save a copy of the actual thread, either saved as PDF or XML.
   - wget
   - wkhtmltopdf
   - princexml

Possible Features:

* Complete trawling of whole boards or even all of 4chan, not just one thread.
* Automated keyword regognition, ie: "Download all threads with 'Taylor Swift' in the title"
* Encrypting the archives. 
* Rudimentary image recognition?
