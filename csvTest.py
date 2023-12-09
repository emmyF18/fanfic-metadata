import ao3
import time
import csv
import re
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
  cleantext = re.sub(cleanregx, '', html)
  return cleantext

metadata = []
outputFile = open('fanficlistTest.csv', 'a')
writer = csv.writer(outputFile)
idNumber = 51531781
api = AO3()
work = api.work(id=idNumber)
metadata = [work.title, stripCharacters(work.author), stripCharacters(work.fandoms), stripCharacters(work.characters), stripCharacters(work.relationship), stripHTML(work.summary), stripCharacters(work.additional_tags), stripCharacters(work.rating), stripCharacters(work.warnings), work.words, work.url]
writer.writerow(metadata)