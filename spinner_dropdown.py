# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 14:03:39 2012

@author: tvgoller
"""

from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.lang import Builder


import webbrowser
import os
import pickle


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
    link = [division['link'] 
        for division in all_stats 
            if (division['sex'] == sex_choice 
                and division['age'] == int(age_choice) 
                and division['division'] == division_choice)][0]
    print link
    webbrowser.open_new_tab(link)

class build_filter_screen(Screen):
    global boys_girls_spinner
    global age_spinner
    global division_spinner
    b = BoxLayout(orientation='vertical')
    boys_girls_spinner = build_spinner(sex_choice, ('Boys', 'Girls'))
    b.add_widget(boys_girls_spinner)
    
    age_list = list(set([str(division['age']) for division in all_stats]))
    age_list.sort(key=lambda x: int(x))
    age_spinner = build_spinner(age_choice, age_list)
    b.add_widget(age_spinner)
    
    division_spinner = build_spinner(division_choice, list([division['division'] for division in all_stats]))
    b.add_widget(division_spinner)

    boys_girls_spinner.bind(text=save_sex_selected_value)
    age_spinner.bind(text=save_age_selected_value)
    division_spinner.bind(text=save_division_selected_value)
    
    open_browser_button = Button(text='View Results')
    b.add_widget(open_browser_button)
    open_browser_button.bind(on_press=open_webpage)
    set_spinner_values()

class stats_screen(Screen):
    pass    

class AccordionApp(App):
    def build(self):
        root = ScreenManager()
        root.add_widget(build_filter_screen(name='Screen1'))
        root.add_widget(stats_screen(name='Screen2'))        

        
        return root
        
if __name__ == '__main__':
    all_stats = load_data()
    load_saved_choices()
    AccordionApp().run()