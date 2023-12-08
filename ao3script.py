from bs4 import BeautifulSoup, Tag
import ao3
import time
import csv
import re
import requests
from ao3 import utils
from ao3 import AO3

def cleanUpCsv(fileName):
    file = open(fileName, 'a')
    reader = csv.reader(file)
    writer = csv.writer(file)


def metadataFromURL(url):
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
        time.sleep(10)

def metadataFromID(inputfileName, outputFileName):
    header = ['Title', 'Author', 'Fandoms', 'Relationships', 'Summary', 'Characters', 'Additional Tags', 'Rating', 'Warnings', 'Work Url']
    inputFile = open(inputfileName)
    work_ids = []
    for work_id in inputFile:
        work_id = work_id.strip()
        work_ids.append(work_id)
    print("Found " + str(len(work_ids)) + " work ids")
    inputFile.close()
    outputFile = open(outputFileName, 'a')
    api = AO3()
    writer = csv.writer(outputFile)
    for idNumber in work_ids:
        work = api.work(id=idNumber)
        # try:
        print('Grabbing metadata for '+ work.title)
        #should try to find out way to check for any of these being null
        metadata = [work.title, work.author, work.fandoms, work.relationship, work.summary, work.additional_tags, work.rating, work.warnings, work.url]  #, work.characters
        # except AttributeError:
        #     metadata = [work.title, work.author, work.fandoms, work.relationship, work.summary, work.additional_tags, work.rating, work.warnings, work.url]  #, work.characters
        #     print('Grabbing metadata for '+ work.title)
        writer.writerow(metadata)
        #print('5 second waiting period after writing metadata')
        time.sleep(5)
    outputFile.close()
    print('all work id\'s processed')

def getWorkIDs(url):
    page = requests.get(url)
    regexWorks = re.compile(r'/works/[0-9]{8}') #work ids are 8 characters long
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.findAll('a',href=regexWorks)
    newSet = set()
    for link in links:
        workid = link.get("href")
        newSet.add(workid[7:15]) # removing duplicates and making sure we only get the ids
        time.sleep(5)
    finalLinks = list(newSet)
    print('Getting work ids for ' + str(len(finalLinks)) + ' links')
    file = open('work_ids.txt', 'a')
    for workid in finalLinks:
        file.write(workid+ "\n")
        print('adding work id: '+ workid + ' to file')


fileName = 'work_ids.txt'
getWorkIDs(url='')
metadataFromID(inputfileName=fileName, outputFileName='fanficlist.csv')