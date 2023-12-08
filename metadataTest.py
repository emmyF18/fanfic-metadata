import ao3
import time
import csv
from ao3 import utils
from ao3 import AO3

inputFile = open("work_idsTest.txt")
work_ids = []
for work_id in inputFile:
    work_id = work_id.strip()
    work_ids.append(work_id)
print("Found " + str(len(work_ids)) + " work ids")
#print(work_ids)
inputFile.close()
# outputFile = open(outputFileName, 'a')
api = AO3()
# writer = csv.writer(outputFile)
for idNumber in work_ids:
     work = api.work(id=idNumber)
     #print(work.title)
     #print(work.author)
     metadata = [work.title, work.author, work.fandoms, work.relationship, work.summary, work.additional_tags, work.rating, work.warnings, work.words, work.url]  #, work.characters
     print('Grabbing metadata for '+ work.title)
     time.sleep(3)