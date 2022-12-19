#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 16:38:11 2022

@author: aforsey
"""

import pickle5 as pickle
import json
import os

def get_spec(file):
    participant_specs = {}
    with open(file, 'rb') as f:
        pratice_episodes, defining_episodes, example_episodes,  game_spec = pickle.load(f)
        print(game_spec)
        return game_spec
                        
                        
directory = 'DATA/Pilot Game Specs/'

for file in os.listdir(directory):
    if not file == ".DS_Store":
        print(file)
        out_file = open("DATA/json_files/"+file+"_obs.json", "w")
        game_spec = get_spec(directory+file)
        json.dump(game_spec, out_file)
        out_file.close()                           


        