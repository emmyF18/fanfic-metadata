import requests
import time

reg = requests.get("https://archiveofourown.org/works/31628549")
fileName = "fanfics.txt"
file = open(fileName, 'w')
file.write(reg.text)
file.close()
time.sleep(5)


# print(reg.text)