import csv
import ao3
from ao3 import AO3

outputFile = open('fanficlist2.csv', 'a')
writer = csv.writer(outputFile)
work_ids = [37010935,35474497]
api = AO3()    
for idNumber in work_ids:
    try:
        work = api.work(id=idNumber) 
        print('Grabbing metadata for '+ work.title + ' ID ' + str(idNumber))
        metadata = stripCharacters(work.additional_tags)
        
        #writer.writerow(metadata)
        time.sleep(5) # 5 sec waiting period per ao3 TOS
    except:
        print((str(idNumber))+ ' not found')
        pass
outputFile.close()
