# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 08:31:29 2012

@author: tvgoller
"""

from datetime import datetime

def overall_info(data):
    wins = data.count(3)
    draws = data.count(1)
    losses = data.count(0)
    forfeit = data.count(-3)
    points = wins*3 + draws + forfeit*-3
    return dict(W=wins,D=draws,L=losses,F=forfeit,PTS=points)
    
def web_date_parse(web_date_str):
    website_date_format = 'Bracket - %A, %B %d, %Y'
    return(datetime.strptime(web_date_str,website_date_format).date())

def web_time_parse(web_time_str):
    website_time_format = '%I:%M %p'
    try:
        parsed_time = datetime.strptime(web_time_str,website_time_format)
    except:
        return None
    else:
        return parsed_time.time()
    
def reported_score(web_score):
    digits_str = ''.join(c for c in web_score if c.isdigit())
    if len(digits_str) > 0:
        return int(digits_str)
    else:
        return None
    
#def game_location(web_game_loc):
    
    
if __name__ == '__main__':
    import random
    random_data = [random.choice([0,1,3,'CS',-3]) for r in range(random.randint(0,10))]
    print random_data
    all_info = overall_info(random_data)
    for key,value in all_info.items():
        print key + " = " + str(value)
        
    sample_dates = ('Bracket - Saturday, August 25, 2012','Bracket - Friday, September 28, 2012')
    for current_date in sample_dates:
        web_date_parse(current_date)
        
    sample_times = ('05:30 PM', '10:30 AM', '    --    ')
    for current_time in sample_times:
        web_time_parse(current_time)
        
    sample_scores = ('1', '1F', '', '0', 'CS', '3'
    )
    for game_score in sample_scores:
        print reported_score(game_score)
        
