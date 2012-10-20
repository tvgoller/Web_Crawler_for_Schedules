# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 11:40:57 2012

@author: M6500
"""
import pickle

with open('all_stats.pkl', 'rb') as input_file:
    all_stats = pickle.load(input_file)
    s = [division['teams'] for division in all_stats if (division['sex'] == 'Girls' and division['age'] == 14 and division['division'] == 'D1')]
    if len(s)>0:
        print s[0][0]
    