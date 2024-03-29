# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 14:03:39 2012

@author: tvgoller
"""

from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.app import App

from kivy.uix.popup import Popup

from kivy.network.urlrequest import UrlRequest

import os
import pickle
import urllib

saved_choices_file = 'previous_choices.pkl'
all_stats = None
sex_choice = None
age_choice = None
division_choice = None
boys_girls_spinner = None
age_spinner = None
division_spinner = None

def load_data():
    with open('all_stats.pkl', 'rb') as input:
        return pickle.load(input)

def load_saved_choices():
    global sex_choice
    global age_choice
    global division_choice
    if os.path.exists(saved_choices_file):
        with open(saved_choices_file, 'rb') as saved_output_file:
            (sex_choice, age_choice, division_choice) = pickle.load(saved_output_file)
    
def save_choices():
    global sex_choice
    global age_choice
    global division_choice
    with open(saved_choices_file, 'wb') as saved_input_file:
        pickle.dump((sex_choice, age_choice, division_choice), saved_input_file)


def set_spinner_values():
    global sex_choice
    global age_choice
    global all_stats
    global age_spinner
    global division_list
    age_list = list(set([str(division['age']) for division in all_stats if division['sex'] == sex_choice]))
    age_list.sort(key=lambda x: int(x))
    age_spinner.values = age_list
    if age_spinner.text not in age_list:
        age_spinner.text = age_list[0]
    
    division_list = list([division['division'] for division in all_stats if (division['sex'] == sex_choice and division['age'] == int(age_choice))])
    division_spinner.values = division_list
    if division_spinner.text not in division_list:
        division_spinner.text = division_list[0]
        
      
def build_spinner(saved_value, values):
    default_text = saved_value if saved_value is not None else values[0]

    spin = Spinner(
        # default value showed
        text=default_text,
        # available values
        values=values,
        # just for positioning in our example
        size_hint=(None, None),
        size=(100, 44),
        pos_hint={'center_x': .5, 'center_y': .5}
    )
    return spin

def save_sex_selected_value(spinner, text):
    global sex_choice
    sex_choice = text
    save_choices()
    set_spinner_values()

def save_age_selected_value(spinner, text):
    global age_choice
    age_choice = text
    save_choices()
    set_spinner_values()

def save_division_selected_value(spinner, text):
    global division_choice
    division_choice = text
    save_choices()

def open_webpage(button):
    global all_stats
    global sex_choice
    global age_choice
    global division_choice
    print sex_choice
    print age_choice
    print division_choice 
    link = 'http://timvgo.appspot.com/uysa/default/call/json/scoreboard/' \
        + urllib.quote(sex_choice) \
        + '/' \
        + urllib.quote(age_choice) \
        + '/'  \
        + urllib.quote(division_choice) 
    print link
    req = UrlRequest(link, open_scoreboard_popup)
    #webbrowser.open_new_tab(link)

def open_scoreboard_popup(req, result):
    if result == ['ERROR']:
        return
    teams = [(team['name'],team['scores']['PTS']) for team in result]
    num_teams = len(teams)
    content = BoxLayout(orientation='vertical')
    grid = GridLayout(cols=2)
    scoreboard_str = sex_choice + " " + age_choice + " " + division_choice
    
    for x in xrange(num_teams):
        team_str = teams[x][0]
        btn = Button(text=team_str, font_size=10)
        grid.add_widget(btn)
        team_str = str(teams[x][1])
        btn = Label(text=team_str, font_size=10, size_hint_x=None, width=65)
        grid.add_widget(btn)
        #btn.bind(on_release=popup.open)

    content.add_widget(grid)
    content_cancel = Button(text='Cancel', size_hint_y=None, height=40)
    content.add_widget(content_cancel)
    popup = Popup(title=scoreboard_str,
                  size_hint=(None, None), size=(300, 450),
                  content=content)
    content_cancel.bind(on_release=popup.dismiss)

    popup.open()
    
class AccordionApp(App):
    def build(self):        
        global boys_girls_spinner
        global age_spinner
        global division_spinner
        root = BoxLayout(orientation='vertical')        

        boys_girls_spinner = build_spinner(sex_choice, ('Boys', 'Girls'))
        root.add_widget(boys_girls_spinner)
        
        age_list = list(set([str(division['age']) for division in all_stats]))
        age_list.sort(key=lambda x: int(x))
        age_spinner = build_spinner(age_choice, age_list)
        root.add_widget(age_spinner)
        
        division_spinner = build_spinner(division_choice, list([division['division'] for division in all_stats]))
        root.add_widget(division_spinner)
    
        boys_girls_spinner.bind(text=save_sex_selected_value)
        age_spinner.bind(text=save_age_selected_value)
        division_spinner.bind(text=save_division_selected_value)
        
        open_browser_button = Button(text='View Results')
        root.add_widget(open_browser_button)
        open_browser_button.bind(on_press=open_webpage)
        set_spinner_values()

        
        return root
        
if __name__ == '__main__':
    all_stats = load_data()
    load_saved_choices()
    AccordionApp().run()