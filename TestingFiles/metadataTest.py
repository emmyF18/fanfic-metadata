import ao3
import time
import csv
import re
from ao3 import utils
from ao3 import AO3

cleanregx = re.compile('<.*?>') 
def stripCharacters(input):
    result = str(input)
    replacements = [('\'', ''), ('[', ''), (']', '')]
    for char, replacement in replacements:
        if char in result:
            result = result.replace(char, replacement)
    return result
    
def stripHTML(html):
  cleantext = re.sub(cleanregx, '', raw_html)
  return cleantext


inputFile = open("work_idsTest.txt")
work_ids = []
for work_id in inputFile:
    work_id = work_id.strip()
    work_ids.append(work_id)
print("Found " + str(len(work_ids)) + " work ids")
#print(work_ids)
inputFile.close()
outputFile = open('fanficlistTest.csv', 'a')
api = AO3()
writer = csv.writer(outputFile)
metadata = []
for idNumber in work_ids:
    work = api.work(id=idNumber)
    metadata = [work.title, stripCharacters(work.author), work.fandoms, work.characters, work.relationship, work.summary, work.additional_tags, work.rating, work.warnings, work.words, work.url]
    print('Grabbing metadata for '+ work.title)
    time.sleep(3)
    writer.writerow(metadata)
