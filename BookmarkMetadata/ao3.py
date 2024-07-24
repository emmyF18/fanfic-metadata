import BookmarkMetadata.const
import re
import collections

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

def ao3MetadataFromList(work_ids):    #this is for processing a full list
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

def ao3MetadataFromID(work_id) -> list:  #get metadata from a single story      
    api = AO3()   
    try:
        work = api.work(id=idNumber) 
        print('Grabbing metadata for '+ work.title + ' ID ' + str(idNumber))
        metadata = [work.title, stripCharacters(work.author), stripCharacters(work.fandoms), stripCharacters(work.characters), stripCharacters(work.relationship), stripHTML(work.summary), stripCharacters(work.additional_tags), stripCharacters(work.rating), stripCharacters(work.warnings), work.words, work.url]
        writer.writerow(metadata)
        time.sleep(5) # 5 sec waiting period per ao3 TOS
    except:
        print((str(idNumber))+ ' not found')