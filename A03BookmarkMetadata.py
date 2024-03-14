from bs4 import BeautifulSoup, Tag
import ao3
import time
import csv
import re
import requests
from ao3 import utils
from ao3 import AO3
from datetime import datetime
import collections
import itertools
import os

webHeaders = {'User-agent': 'Mozilla/5.0 (compatible; unofficial AO3 API; Bot;)'}
csvHeader = ['Title', 'author', 'Fandom', 'Characters', 'Paring', 'Summary', 'Additional Tags', 'Rating', 'Warnings', 'Words', 'Work Url']
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

def metadataFromID(inputfileName, outputFileName):
    inputFile = open(inputfileName)
    work_ids = []
    for work_id in inputFile:
        work_id = work_id.strip()
        work_ids.append(work_id)
    print("Found " + str(len(work_ids)) + " work ids")
    inputFile.close()
    outputFile = open(outputFileName, 'a')
    writer = csv.writer(outputFile)
    writer.writerow(csvHeader)
    # if(os.path.exists(outputFileName)):
    #     outputFile = open(outputFileName, "a")
    #     writer = csv.writer(outputFile)       
    # else:
    #     outputFile = open(outputFileName, 'o')
    #     writer = csv.writer(outputFile)
    #     writer.writerow(csvHeader)
    api = AO3()    
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
    if os.path.exists(inputfileName):
        os.remove(inputfileName)

def getRestrictedMetadata(inputfileName, outputFileName): #TODO: it would be great to get the log-in feature working at some point so this is not needed
    inputFile = open(inputfileName)
    work_ids = []
    for work_id in inputFile:
        work_id = work_id.strip()
        work_ids.append(work_id)
    print("Found " + str(len(work_ids)) + " work ids")
    inputFile.close()
    outputFile = open(outputFileName, 'a')
    api = AO3()
    for idNumber in work_ids:
        try:
            work = api.work(id=idNumber) 
            print('Grabbing metadata for '+ work.title + ' ID ' + str(idNumber))
            metadata = [work.title, stripCharacters(work.author), stripCharacters(work.fandoms), stripCharacters(work.characters), stripCharacters(work.relationship), stripHTML(work.summary), stripCharacters(work.additional_tags), stripCharacters(work.rating), stripCharacters(work.warnings), work.words, work.url]
            #writer.writerow(metadata)
            time.sleep(5) # 5 sec waiting period per ao3 TOS
        except:  
            outputFile = open(outputFileName, 'a').write('https://archiveofourown.org/works/'+str(idNumber)+ "\n")
            print((str(idNumber))+ ' not found')
            pass
    print('all work id\'s processed')  

def getWorkIDs(username,fileName,page_no):
    sess = requests.Session()
    bookmarkURL = 'https://archiveofourown.org/users/'+username+'/bookmarks?page=%d'
    bookmarks = []
    req = sess.get(bookmarkURL % page_no)
    soup = BeautifulSoup(req.text, features='html.parser')

    ol_tag = soup.find('ol', attrs={'class': 'bookmark'})
    for li_tag in ol_tag.findAll('li', attrs={'class': 'blurb'}):
        try:
            for h4_tag in li_tag.findAll('h4', attrs={'class': 'heading'}):
                for link in h4_tag.findAll('a'):
                    if ('works' in link.get('href')) and not ('external_works' in link.get('href')):
                        work_id = link.get('href').replace('/works/', '')
                        bookmarks.append(work_id)
                        print('found work id ' + work_id)
        except KeyError: #deleted works
            if 'deleted' in li_tag.attrs['class']:
                pass
            else:
                raise       
        time.sleep(3)
    print('found ' + str(len(bookmarks)) + ' bookmarks')            
    file = open(fileName, "x")
    for workid in bookmarks:
        file.write(workid+ "\n")
    file.close()        

def getSeriesLinks(username, fileName):
    sess = requests.Session()
    bookmarkURL = 'https://archiveofourown.org/users/'+username+'/bookmarks?page=%d'
    bookmarks = []
    num_works = 0
    for page_no in itertools.count(start=1):
        print("Finding page: \t" + str(page_no) + " of bookmarks. \t" + str(num_works) + " bookmark ids found.")
        req = sess.get(bookmarkURL % page_no)
        soup = BeautifulSoup(req.text, features='html.parser')
        file = open(fileName, 'a')
        ol_tag = soup.find('ol', attrs={'class': 'bookmark'})
        for li_tag in ol_tag.findAll('li', attrs={'class': 'blurb'}):
            num_works = num_works + 1
            try:
                for h4_tag in li_tag.findAll('h4', attrs={'class': 'heading'}):
                    for link in h4_tag.findAll('a'):
                        if ('series' in link.get('href')) and not ('external_works' in link.get('href')):
                            work_id = link.get('href').replace('/series/', '')
                            bookmarks.append(work_id)
                            print('found work id ' + work_id)
                            file.write(f'https://archiveofourown.org/series/{work_id}' +'\n')
            except KeyError: #deleted works
                if 'deleted' in li_tag.attrs['class']:
                    pass
                else:
                    raise
        try:
            next_button = soup.find('li', attrs={'class': 'next'})
            if next_button.find('span', attrs={'class': 'disabled'}):
                break
        except:
            # In case of absence of "next"
            break        
        time.sleep(5)
    print('found ' + str(len(bookmarks)) + ' series bookmarks')
    file.close()

def getAllBookmarks(username, fileName):
    sess = requests.Session()
    bookmarkURL = 'https://archiveofourown.org/users/'+username+'/bookmarks?page=%d'
    bookmarks = []
    num_works = 0
    for page_no in itertools.count(start=1):
        print("Finding page: \t" + str(page_no) + " of bookmarks. \t" + str(num_works) + " bookmarks ids found.")
        req = sess.get(bookmarkURL % page_no)
        soup = BeautifulSoup(req.text, features='html.parser')

        ol_tag = soup.find('ol', attrs={'class': 'bookmark'})
        for li_tag in ol_tag.findAll('li', attrs={'class': 'blurb'}):
            num_works = num_works + 1
            try:
                for h4_tag in li_tag.findAll('h4', attrs={'class': 'heading'}):
                    for link in h4_tag.findAll('a'):
                        if ('works' in link.get('href')) and not ('external_works' in link.get('href')):
                            work_id = link.get('href').replace('/works/', '')
                            bookmarks.append(work_id)
                            print('found work id ' + work_id)
            except KeyError: #deleted works
                if 'deleted' in li_tag.attrs['class']:
                    pass
                else:
                    raise
            print(num_works)    
        try:
            next_button = soup.find('li', attrs={'class': 'next'})
            if next_button.find('span', attrs={'class': 'disabled'}):
                break
        except:
            # In case of absence of "next"
            break        
        time.sleep(5)
    print('found ' + str(len(bookmarks)) + ' bookmarks')            
    file = open(fileName, 'a')
    for workid in bookmarks:
        file.write(workid+ "\n")
    file.close()  


pageNumber = 1
IDFileName = 'BookmarkIDs.txt'
getWorkIDs(username='',fileName=IDFileName,page_no=pageNumber)
#getAllBookmarks('','allBookmarks.txt')
metadataFromID(inputfileName=IDFileName, outputFileName='MetadataPage'+ str(pageNumber) +'.csv')
#getRestrictedMetadata(inputfileName='allBookmarks2.txt', outputFileName='Resricted.txt')
#getSeriesLinks('','seriesLinks.txt')