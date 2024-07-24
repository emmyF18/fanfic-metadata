import requests
from bs4 import BeautifulSoup
from requests import codes

class SoupRequests:
    username = ''
    def __init__(self):
        self.session = requests.Session()
    def login(self, username, password):
        return
    def getWorkIDs(self,username,fileName,page_no) -> list:
        sess = self.session
        bookmarkURL = f'https://archiveofourown.org/users/{username}/bookmarks?page={page_no}'
        bookmarks = []
        req = sess.get(bookmarkURL)
        soup = BeautifulSoup(req.text, features='html.parser')

        ol_tag = soup.find('ol', attrs={'class': 'bookmark'})
        for li_tag in ol_tag.findAll('li', attrs={'class': 'blurb'}):
            try:
                for h4_tag in li_tag.findAll('h4', attrs={'class': 'heading'}):
                    for link in h4_tag.findAll('a'):
                        if ('works' in link.get('href')):
                            work_id = link.get('href').replace('/works/', '')
                            bookmarks.append(work_id)
                            print('found work id ' + work_id)
            except KeyError: #deleted works
                if 'deleted' in li_tag.attrs['class']:
                    pass
                else:
                    raise  
        return bookmarks
    def getAllBookmarks(self, username,fileName) -> list:
        sess = self.session
        bookmarks = []
        num_works = 0
        for page_no in itertools.count(start=1):
            bookmarkURL = f'https://archiveofourown.org/users/{username}/bookmarks?page={page_no}'
            print("Finding page: \t" + str(page_no) + " of bookmarks. \t" + str(num_works) + " bookmarks ids found.")
            req = sess.get(bookmarkURL)
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
