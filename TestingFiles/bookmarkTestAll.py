from datetime import datetime
import collections
import itertools
import re
import time
from bs4 import BeautifulSoup, Tag
import requests

sess = requests.Session()
bookmarkURL = 'https://archiveofourown.org/users//bookmarks?page=%d'
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
file = open('work_ids4.txt', 'a')
for workid in bookmarks:
    file.write(workid+ "\n")
file.close()