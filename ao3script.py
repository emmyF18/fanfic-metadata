from bs4 import BeautifulSoup, Tag
import ao3
import time
import csv
import re
import requests
from ao3 import utils
from ao3 import AO3

webHeaders = {'User-agent': 'Mozilla/5.0 (compatible; unofficial AO3 API; Bot;)'}
csvHeader = ['Title', 'Author', 'Fandoms', 'Characters', 'Relationships', 'Summary', 'Additional Tags', 'Rating', 'Warnings', 'Words', 'Work Url']
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

def metadataFromUrlsList():
    urlInput = str(input())
    urlList = urlInput.split()
    for url in urlList:
        workid = utils.work_id_from_url(url)
        api = AO3()
        work = api.work(id=workid)
        metadata = [work.title, stripCharacters(work.author), stripCharacters(work.fandoms), stripCharacters(work.characters), stripCharacters(work.relationship), stripHTML(work.summary), stripCharacters(work.additional_tags), stripCharacters(work.rating), stripCharacters(work.warnings), work.words, work.url]
        file = open('fanficlist.csv', 'a')
        writer = csv.writer(file)
        writer.writerow(metadata)
        file.close()
        time.sleep(5)

def metadataFromID(inputfileName, outputFileName):
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
    writer.writerow(csvHeader) #TODO: write this only if file is empty
    for idNumber in work_ids:
        try:
            work = api.work(id=idNumber) 
            print('Grabbing metadata for '+ work.title + ' ID ' + str(idNumber))
            metadata = [work.title, stripCharacters(work.author), stripCharacters(work.fandoms), stripCharacters(work.characters), stripCharacters(work.relationship), stripHTML(work.summary), stripCharacters(work.additional_tags), stripCharacters(work.rating), stripCharacters(work.warnings), work.words, work.url]
            writer.writerow(metadata)
            time.sleep(5) # 5 sec waiting period per ao3 TOS
        except:
            print((str(idNumber))+ ' not found')
            pass
    outputFile.close()
    print('all work id\'s processed')

def getWorkIDs(url,fileName):
    #page = requests.get(url)
    page = requests.get(url,headers=webHeaders)
    regexWorks = re.compile(r'/works/[0-9]+') #work ids are 8 characters long TODO:improve this
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.findAll('a',href=regexWorks)
    newSet = set()
    for link in links:
        workid = link.get("href")
        newSet.add(workid[7:15]) # removing duplicates and making sure we only get the ids
    finalLinks = list(newSet)
    print('Getting work ids for ' + str(len(finalLinks)) + ' links')
    file = open(fileName, 'a')
    for workid in finalLinks:
        file.write(workid+ "\n")
        print('adding work id: '+ workid + ' to file')

def getSeriesLinks(url,fileName):
    #page = requests.get(url)
    page = requests.get(url,headers=webHeaders)
    regexWorks = re.compile(r'/series/[0-9]+')
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.findAll('a',href=regexWorks)
    newSet = set()
    for link in links:
        workid = link.get("href").replace('/bookmarks', '')
        newSet.add(workid)
    finalIds = list(newSet)
    file = open(fileName, 'a')
    for id in finalIds:
        file.write(f'https://archiveofourown.org{id}')
    #print('Getting series ids for ' + str(len(finalIds)) + ' links')
    # file = open(fileName, 'a')
    # for workid in finalLinks:
    #     file.write(workid+ "\n")
    #     print('adding series id: '+ workid + ' to file')


fileName = 'work_id1.txt'
getWorkIDs(url='https://archiveofourown.org/users//bookmarks?page=1',fileName=fileName)
metadataFromID(inputfileName=fileName, outputFileName='fanficlist1.csv')
