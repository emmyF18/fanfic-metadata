import ao3
import requests
import time
import csv
from ao3 import utils
from ao3 import AO3

def cleanUpCsv(string):
    file = open(fileName, 'a')
    reader = csv.reader(file)
    writer = csv.writer(file)

header = ['Title', 'Author', 'Fandoms', 'Relationships', 'Summary', 'Characters', 'Additional Tags', 'Rating', 'Warnings', 'Work Url']
urlInput = str(input())
urlList = urlInput.split()
for url in urlList:
    workid = utils.work_id_from_url(url)
    api = AO3()
    work = api.work(id=workid)
    try:
        metadata = [work.title, work.author, work.fandoms, work.relationship, work.summary, work.characters, work.additional_tags, work.rating, work.warnings, work.url]
    except AttributeError: 
        metadata = [work.title, work.author, work.fandoms, '', work.summary, work.characters, work.additional_tags, work.rating, work.warnings, work.url]
    file = open('fanficlist.csv', 'a')
    writer = csv.writer(file)
    writer.writerow(metadata)
    file.close()
    time.sleep(5)
