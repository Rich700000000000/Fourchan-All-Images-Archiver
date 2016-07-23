Script to download all the images in a 4chan thread.

Warning: I've never used Git before, so if I accidentally screw up and wipe out everything send me a message to get it resolved.

Use:

        python3 FCAIA.py http://boards.4chan.org/g/thread/52438119/edc-every-day-carry

To Do:

* Make it turn the folder into an archive, storage only.
* Make it turn the folder into an archive, lossless compression.
* Make it save a copy of the actual thread, either saved as PDF or XML.
   - wget
   - wkhtmltopdf
   - princexml

Done:

* Make it incorporate the original file names into the image names.
* Fixed error causing all images to be saved as jpg.
