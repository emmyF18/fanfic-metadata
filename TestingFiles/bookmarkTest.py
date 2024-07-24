from datetime import datetime
import collections
import itertools
import re
import time
from bs4 import BeautifulSoup, Tag
import requests

sess = requests.Session()
bookmarkURL = 'https://archiveofourown.org/users//bookmarks?page=%6'
bookmarks = []
req = sess.get(bookmarkURL)
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
file = open('work_idsTest.txt', 'a')
for workid in bookmarks:
    file.write(workid+ "\n")
file.close()