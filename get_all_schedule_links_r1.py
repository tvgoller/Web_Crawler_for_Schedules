# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 13:32:46 2012

@author: goller
"""
import mechanize
import re
from bs4 import BeautifulSoup

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

for link in schedule_links:
    r = br.open(link)
    page_data = r.get_data()
    soup = BeautifulSoup(page_data)
