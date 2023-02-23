#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 16:15:06 2023

@author: aforsey
"""
import os
import getopt, sys 
import pandas as pd
import pickle
import json 
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from inference_by_participant import perform_inference


def process_participant_scores(ID):
    if ID ==1: file ="game_play20221213_173622"
    elif ID ==2: file ="game_play20221214_222820"
    elif ID ==3: file = "game_play20221214_204143"
    elif ID ==4: file = "game_play20221213_165753"
    elif ID ==5: file ="game_play20221213_123158"
    elif ID ==6: file = "game_play20221213_115806"
    elif ID ==7: file = "game_play20221212_160939"
    elif ID ==8: file = "game_play20221213_125553"
    elif ID ==9: file = "game_play20221212_124446"
    elif ID ==10: file = "game_play20221212_121643"
    
    directory = os.getcwd()+ '/DATA/game_play'
    with open(directory+'/'+file, 'rb') as f:
        practice_episodes, game_play = pickle.load(f)
        
        games = {}
        
        for game in game_play.keys():
            if (game != "order"):# and (game.split(' ')[1].split('_')[0] != 'game1'): #key pertains to game, "order" only key that doesn't 
                game_name = game.split(' ')[1].split('_')[0]
                episode_list = game_play[game]['episodes']
                episode_scores = [0]
                total_game_score = 0 
                counter = 0 
                for i,episode in enumerate(episode_list):
                  #  ep_score = 0 
                  #  print(episode)
                    
                    for j, clicked_box in enumerate(episode['clicked_boxes']):
                        if j>=2:
                            counter +=1
                            total_game_score += clicked_box['click_score']
                            if counter % 5 == 0:
                            
                                #every 10 clicks, record score 
                               # total_game_score += clicked_box['total_score']
                                episode_scores.append(total_game_score)  
                                
                        
                games[game_name]=pd.DataFrame({
                              'participant_ID': [ID]*len(episode_scores),
                              'game': [game_name]*len(episode_scores),
                              'clicks': [*range(0,counter+1,5)],
                              'score': episode_scores
                              })
        return games,file
  
# g1_clicks = participant_data.loc[participant_data['game'] == 'game1']
# g2_clicks = participant_data.loc[participant_data['game'] == 'game2']
# g3_clicks = participant_data.loc[participant_data['game'] == 'game3']
# g4_clicks = participant_data.loc[participant_data['game'] == 'game4']

def read_model_data(participant_data, file):
    game_list =  ["game1", "game2", "game3", "game4"]
    priors = [0.5,0.5,0.5,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333]
    normalized_priors = [float(i)/sum(priors) for i in priors]
    model_dfs={}
    #outer_folder = /DATA/inference_json_files/{file}/"
    outer_folder = os.getcwd()+ f'/DATA/inference_json_files/{file}/'
    
    for game_name in game_list: 
        upper_bound = participant_data[game_name]['clicks'].iloc[-1] #gets number of total clicks from participant data
        game_df = pd.DataFrame(index = [*range(0,upper_bound+1,5)], columns=[*range(0,123)])
        game_df.loc[0] = normalized_priors
        for i in range(5,upper_bound+1,5):
            json_file = outer_folder+game_name+f'/{file}_{game_name}_slice{i}_inference.json'
            f = open(json_file)
            imported = json.load(f)
            game_df.loc[i] = imported
    
        model_dfs[game_name] = game_df
    return model_dfs
    

def plot_participant(ID,participant_data, model_data):
    

    #GAME 1 (MODEL THINKS 79 - confirmed correct: click green for either, id79)
    fig, (a1,a2) = plt.subplots(2, 1)
    fig.tight_layout(pad=1.0)
    game_one_colors = ['red']*123
    game_one_colors[79]= 'green'
    p_g1_clicks = participant_data['game1'].plot(x= 'clicks', y='score', ax=a1, title=f'P{ID} Game 1', legend=False, xlabel='', ylabel='Participant Score', marker='.')
    model_data['game1'].plot(legend=False, ax=a2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.', color=game_one_colors)
    a1.grid(lw=0.2)
    a2.grid(lw=0.2)

    # #GAME 2 (model thinks 122 - confirmed correct: click blue when black and white when green, id122)
    fig, (b1,b2) = plt.subplots(2, 1)
    fig.tight_layout(pad=1.0)
    game_two_colors = ['red']*123
    game_two_colors[122]= 'green'
    p_g2_clicks = participant_data['game2'].plot(x= 'clicks', y='score', ax=b1, title=f'P{ID} Game 2', legend=False, xlabel='', ylabel='Participant Score', marker='.')
    model_data['game2'].plot(legend=False, ax=b2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.', color=game_two_colors)
    b1.grid(lw=0.2)
    b2.grid(lw=0.2)


    # # #GAME 3 (MODEL thinks 8 - confirmed correct: click green then blue while black, id8)
    fig, (c1,c2) = plt.subplots(2, 1)
    fig.tight_layout(pad=1.0)
    game_three_colors = ['red']*123
    game_three_colors[8]='green'
    p_g3_clicks = participant_data['game3'].plot(x= 'clicks', y='score', ax=c1, title=f'P{ID} Game 3 ', legend=False, xlabel='', ylabel='Participant Score', marker='.')
    model_data['game3'].plot(legend=False, ax=c2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.', color=game_three_colors)
    c1.grid(lw=0.2)
    c2.grid(lw=0.2)


    # #GAME 4 (MODEL thinks 111 - confirmed correct: click blue, green, red for either bg, id111) 
    #DIFF FOR P10, GAME SPEC WAS: BRR -->(model thinks 108- CORRECT, brr under either background, id108)
    
    fig, (d1,d2) = plt.subplots(2, 1)
    fig.tight_layout(pad=1.0)
    game_four_colors = ['red']*123
    if ID==10: game_four_colors[108]='green'
    else: game_four_colors[111]='green'
    p_g4_clicks = participant_data['game4'].plot(x= 'clicks', y='score', ax=d1, title=f'P{ID}  Game 4', legend=False, xlabel='', ylabel='Participant Score', marker='.')
    model_data['game4'].plot(legend=False, ax=d2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.', color=game_four_colors)
    d1.grid(lw=0.2)
    d2.grid(lw=0.2)

    plt.show(block=True)                
                
#if __name__ == "__main__":
    # options = "p:"
    # long_options= ["Participant="]
    # args = sys.argv[1:]
    # try: 
    #     arguments,vals = getopt.getopt(args, options, long_options)
    # except getopt.error as err:
    #     print(str(err))
        
   # ID = vals[0] #check this

for i in range(1,11):
    participant_data, file = process_participant_scores(i)
    model_dfs = read_model_data(participant_data, file)
    plot_participant(i,participant_data, model_dfs)
    
    
    #print(participant_data["game1"]['clicks'].iloc[-1])
    #print(participant_data)
   # model_data = perform_inference(file, participant_data) #need participant data as input to get number of clicks
    # plot_participant(participant_data, model_data)
    
    
                
                
                