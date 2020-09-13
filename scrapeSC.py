import os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


'''

A simple web scraper script writes a squash schedule 
to a importable calender document for google calender

'''

div7 = "http://www.squashcenter.se/lagsquash/division-7/"

# TODO: make function  <13-09-20, oscar> #
uClient = uReq(div7)
pageHtml = uClient.read()
uClient.close()

pageSoup = soup(pageHtml, "html.parser")
gameTable = pageSoup.table
rows = gameTable.find("tbody").find_all("tr")
print(rows)
# print(pageSoup.table)

for row in rows:
    cells = row.find_all("td")
    rn = ""
    for el in cells:
        if el:
            rn += el.get_text() + " "
        else:
            print("Empty element")
    if(rn):
        print("This is a row  : ", rn)


class team:


class game:



def game_to_event(game):
    
