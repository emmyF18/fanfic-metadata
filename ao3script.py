import ao3
import requests
import time
import csv

from ao3 import utils
header = ['Title', 'Author', 'Fandoms', 'Relationships', 'Summary', 'Characters', 'Additional Tags', 'Rating', 'Warnings' 'Work Url']
urlInput = str(input())
urlList = urlInput.split()
for url in urlList:
    workid = utils.work_id_from_url(url)
    from ao3 import AO3
    api = AO3()
    work = api.work(id=workid)
    metadata = [work.title, work.author, work.fandoms, work.relationship, work.summary, work.characters, work.additional_tags, work.rating, work.warnings, work.url]
    file = open('fanficlist.csv', 'a')
    writer = csv.writer(file)
    #writer.writerow(header)
    writer.writerow(metadata)
    file.close()
    time.sleep(5)
