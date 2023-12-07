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
    #header = ['Title', 'Author', 'Fandoms', 'Relationships', 'Summary', 'Characters', 'Additional Tags', 'Rating', 'Warnings', 'Work Url']
    inputFile = open(inputfileName)
    work_ids = inputFile.readlines()
    inputFile.close()      
    outputFile = open(outputFileName, 'a')
    api = AO3()
    writer = csv.writer(outputFile)
    for idNumber in work_ids:        
        work = api.work(id=idNumber)
        try:
            metadata = [work.title, work.author, work.fandoms, work.relationship, work.summary, work.characters, work.additional_tags, work.rating, work.warnings, work.url]
            print('Grabbing metadata for '+ work.title)
        except AttributeError: 
            metadata = [work.title, work.author, work.fandoms, '', work.summary, work.characters, work.additional_tags, work.rating, work.warnings, work.url]  
            print('Grabbing metadata for '+ work.title)
        writer.writerow(metadata)
        print('5 second waiting period')
        time.sleep(5)    
    outputFile.close()    

def getWorkIDs(url):
    page = requests.get(url)
    regexWorks = re.compile(r'/works/[0-9]{8}')
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.findAll('a',href=regexWorks)
    newSet = set()
    for link in links:
        workid = link.get("href")
        newSet.add(workid[7:15])
        print('adding work id for: '+ link.text)
        time.sleep(5)
    finalLinks = list(newSet)
    print('Getting work ids for ' + len(finalLinks) + ' links')
    file = open('work_ids.txt', 'a')
    for workid in finalLinks:
        file.write(workid+ "\n")
        #print('adding work id: '+ workid + ' to file')
        time.sleep(5)


fileName = 'work_ids.txt'
metadataFromID(inputfileName=fileName, outputFileName='fanficlist.csv')