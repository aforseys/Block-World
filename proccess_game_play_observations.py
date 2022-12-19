#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 11:47:00 2022

@author: aforsey
"""
import os 
import json
import pickle
from game_scoring_functions import game1_score, game2_score, game3_score, game4_score

def color_2_string(color):
    if color == (0, 255, 0): return "green"
    elif color == (255, 0, 0): return "red"
    else: return "blue"
    
def bg_2_string(env_white):
    if env_white: return "white"
    else: return "black"

def update_reward(reward):
    #only want reward of 1 and 0, getting rid of -3 reward
    if reward == -3:
        return 0 
    return reward 

def process_observations(file):
    with open(file, 'rb') as f:
        practice_episodes, game_play = pickle.load(f)
        games = {}
        for g in game_play.keys():
            if g != "order":
                game_name = g.split(' ')[1].split('_')[0]
                game = game_play[g]
                episodes = game_play[g]['episodes']
                observations = []
        
        
                for i, episode in enumerate(episodes):
                    for j, clicked_box in enumerate(episode['clicked_boxes']):
                
                        if j >= 2: #currently not accounting for first 2 clicks in episode (if no history)
                            click = {'action': color_2_string(clicked_box['color']),
                             'bg': bg_2_string(clicked_box['env_white_before']),
                             'a1': color_2_string(episode['clicked_boxes'][j-2]['color']),
                             'a2': color_2_string(episode['clicked_boxes'][j-1]['color']),
                             'bg1': bg_2_string(episode['clicked_boxes'][j-2]['env_white_before']),
                             'bg2': bg_2_string(episode['clicked_boxes'][j-1]['env_white_before']),
                             'reward': update_reward(clicked_box['click_score'])
                         }
                            observations.append(click)
                    
                games[game_name] = observations
                    
        return games
    
directory = 'DATA/game_play/'

for file in os.listdir(directory):
    if not file == ".DS_Store":
        out_file = open("DATA/json_files/"+file+"_obs.json", "w")
        games = process_observations(directory+file)
        json.dump(games, out_file)
        out_file.close()   
