import os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

'''
A simple web scraper script writes a squash schedule 
to a importable calender document for google calender
'''

def get_matches(pageSoup):
    '''
    gets all the matches on page table
    '''
    gameTable = pageSoup.table
    rows = gameTable.find("tbody").find_all("tr")
    match_list = []

    for row in rows:
        match = {}
        date = row.find("td", {"class" : "column-1"}).get_text().split()[1::]
        home_team = row.find("td", {"class" : "column-2"}).get_text()
        vis_team = row.find("td", {"class" : "column-4"}).get_text()
        match["date"] = date
        match["teams"] = [home_team, vis_team]
        if(date):
            match_list.append(match)

    return match_list

def parse_page(url ="http://www.squashcenter.se/lagsquash/division-7/"):
    '''
    simply parses a given url with bs4
    '''
    # get page
    uClient = uReq(url)
    pageHtml = uClient.read()
    uClient.close()

    # parse html
    return soup(pageHtml, "html.parser")

def find_teams(pageSoup):
    '''
    parses out teams in given page
    accoring to the tags for teams
    '''
    mydivs = pageSoup.findAll("div", {"class": "wpb_text_column wpb_content_element"})
    team_list = []
    for d in mydivs:
        team = {"teamName" : "",
                "players" : {} 
               }

        if(d.findAll("h3")):
            team["teamName"] = d.findAll("h3")[0].get_text()

        contacts = d.findAll("p")[2::]
        totContact = []
        for pres in contacts:
            if(pres):
                totContact.append(pres.get_text().split("<\br>")[0].split("\n"))
        
        finContact = [item for sublist in totContact for item in sublist]

        for i, h4 in enumerate(d.findAll("h4")):
            team["players"][h4.get_text()] = {}
            phone = finContact[2*i]
            mail = finContact[2*i + 1]
            team["players"][h4.get_text()]["phone"] = phone
            team["players"][h4.get_text()]["mail"] = mail

        if(team["teamName"] != ""):
            team_list.append(team)
    
    return team_list


def get_matches_and_teams():
    poi = parse_page()
    teams = find_teams(poi)
    matches = get_matches(poi)
    return teams, matches

def get_all_matches_for_team(toi = "Kimstad Industriplåt AB"):
    teams, matches = get_matches_and_teams()
    moi = [m for m in matches if(toi in m["teams"])]
    ordered_team_list = []
    for m in moi:
        team = [t for t in m["teams"] if( toi != t)][0]
        for tz in teams:
            if(team == tz["teamName"]):
                ordered_team_list.append(tz)
    return moi, ordered_team_list


def main():
    get_all_matches_for_team()

if __name__ == '__main__':
    main()
