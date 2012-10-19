# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 13:32:46 2012

@author: tvgoller
"""

## easy_install mechanize, easy_install BeautifulSoup4

import mechanize
import re
from bs4 import BeautifulSoup
import pickle
import json
import generate_stats

br = mechanize.Browser()
link = 'http://www.utahyouthsoccer.net/programs/competitionschedule.aspx'

br.open(link)
# Open the boys' schedule
r = br.find_link(text_regex=re.compile("Schedule and Scores"))
br.open(r.absolute_url)

schedule_links = [link.absolute_url for link in br.links(text_regex=re.compile("Schedule & Results"))]
# Open Girls' page
br.open(br.find_link(text_regex=re.compile("^Girls$")).absolute_url)
schedule_links.extend([link.absolute_url for link in br.links(text_regex=re.compile("Schedule & Results"))])

all_page_data = []

##for faster testing of the website data
#with open('data_dump.pkl', 'rb') as file_input:
#    all_page_data = pickle.load(file_input)


getting_scoreboard = True
all_stats = []
#for page_index,page_data in enumerate(all_page_data):
    

for page_index,link in enumerate(schedule_links):
    r = br.open(link)
    page_data = r.get_data()
    #all_page_data.append(page_data)
    soup = BeautifulSoup(page_data)
    
    sex_age_division = soup.find('span',{'title'}).get_text() #gets title for age, sex, division
    
    #special circumstance due to inconsistency of wording on website    
    if 'GU15' in sex_age_division:
        age = 15
        sex = 'Girls'
        division = 'Provisional'
    #for everything else that is not a special circumstance
    else:
        age = [int(s) for s in sex_age_division.split() if s.isdigit()][0]
        sex = 'Boys' if ('Boy' or 'Boys') in sex_age_division else 'Girls'
        division = sex_age_division.split(str(age))[-1].lstrip()

    teams = []
    division_scores = []
    print age,sex,division
    
#    find_element_tables = soup.findAll('td', attrs={'class':'tbody', 'nowrap':''})
#    for team in find_element_tables:
#            print team.get_text()

    page = soup.findAll('td', attrs={'class':'tbody', 'nowrap':''})

    while True:
        if len(page)==0:
            break
        getting_team = True
        club_info = page.pop(0)
        team_name = page.pop(0).get_text().split(':')[1][1:]
        goal_diff = None
        goals_against = None
        goals_for = None
        scores = []
        while getting_team:
            cur_score = page.pop(0)
            if cur_score.find('font', {'color':'blue'}) is not None:
                goal_diff = int(cur_score.get_text()[1:-1])
                getting_team = False
            else:
                s = generate_stats.reported_score(cur_score.get_text())
                scores.append(s)
        overall_scores = generate_stats.overall_info(scores)
        goals_against = int(page.pop(0).get_text()[1:-1])
        goals_for = int(page.pop(0).get_text()[1:-1])
        info = {'name':team_name, 'diff':goal_diff, 'against': goals_against, 'for':goals_for, 'scores': overall_scores}
        teams.append(info)
        if (len(page)==0) or (len(page[0].get_text()) > 1 and page[0].get_text()[0] == u'\xa0'):
            break

    while len(page) > 0:
        game_number = page.pop(0)
        venue = page.pop(0)
        time = page.pop(0)
        field = page.pop(0)
        group = page.pop(0)
        home_team = page.pop(0)
        home_score = page.pop(0)
        vs = page.pop(0)
        away_team = page.pop(0)
        away_score = page.pop(0)
        location = 'http://uysa.affinitysoccer.com/tour/public' + venue.attrs['onclick'].split(',')[0].split('(')[-1].split("'")[1][2:]
        time = generate_stats.web_time_parse(time.get_text()[1:-1])
        info = {'venue':venue.get_text(), 'location':location, 'time':time, 'home_team': home_team.get_text(), 'home_score': home_score.get_text(), 'away_team': away_team.get_text(), 'away_score': away_score.get_text()}
        division_scores.append(info)
  
    all_stats.append({'link': schedule_links[page_index], 'age':age, 'sex':sex,'division':division,'teams':teams,'scores':division_scores})

with open('all_stats.pkl', 'wb') as output:
    pickle.dump(all_stats, output)
with open('cpg_test.json', 'wb') as json_output:
    json.dump(all_stats, json_output)
[(team['name'], team['scores']) for division in all_stats if (division['sex'] == 'Girls' and division['age'] == 14) for team in division['teams'] if 'Avalanche' in team['name']]
#r = br.open(schedule_links[0])
#page_data = r.get_data()
#soup = BeautifulSoup(page_data)

##do this first to get local information to test data faster than going to the actual website
#with open('data_dump.pkl', 'wb') as file_output:
#    pickle.dump(all_page_data,file_output)