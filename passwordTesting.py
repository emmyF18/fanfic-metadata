import requests
import time
import ao3
from ao3 import AO3
from bs4 import BeautifulSoup, Tag


# reg = requests.get("https://archiveofourown.org/works/31628549")
# fileName = "fanfics.txt"
# file = open(fileName, 'w')
# file.write(reg.text)
# file.close()
# time.sleep(5)
api = AO3()
username = ''
password = ''
sess = requests.Session()
page_no = 1
req = sess.post('https://archiveofourown.org/user_sessions', params={'user_session[login]': username, 'user_session[password]': password })
#api.login(username='',password='')
bookmarkURL = 'https://archiveofourown.org/users/'+username+'/bookmarks?page=%d'
req = sess.get(bookmarkURL % page_no)
bookmarks = []
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
file = open('fileTest.txt', "x")
for workid in bookmarks:
    file.write(workid+ "\n")
file.close() 

# api = AO3()
# api.login(username='',password='')
# work = api.work(id=53290729)
# print(work.title)
# print(work.summary)
# print(work.author)

# print(reg.text)