#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 22:20:03 2022

@author: aforsey
"""
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


#Make a df for each game which contains participants as columns and clicks as
#rows 
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

directory = os.getcwd()+ '/DATA/game_play'

# file = 'game_play20221213_173622'
score_intervals = [*range(10,91,10)]
frames = []
participant_ID=0

for file in os.listdir(directory):
    print(file)
    with open(directory+'/'+file, 'rb') as f:
        practice_episodes, game_play = pickle.load(f)
        
        for game in game_play.keys():
            if (game != "order") and (game.split(' ')[1].split('_')[0] != 'game1'): #key pertains to game, "order" only key that doesn't 
                game_name = game.split(' ')[1].split('_')[0]
                episode_list = game_play[game]['episodes']
                interval_counter = 0 
                episode_scores = []
                total_game_score = 0 
                for i,episode in enumerate(episode_list):
                  #  ep_score = 0 
                  #  print(episode)
                    
                    if i == 0:
                        game_start = episode['start_time']
                    for j, clicked_box in enumerate(episode['clicked_boxes']):
                        box_time = (clicked_box['click_time'] - game_start)/1000
                        
                        if interval_counter == len(score_intervals)-1:
                            break
                        
                        if box_time > score_intervals[interval_counter]:
                            if j == 0:
                                score = episode_list[i-1]['clicked_boxes'][j-1]['total_score']
                        #        ep_score += score
                                total_game_score += score 
                            else:
                                score = episode['clicked_boxes'][j-1]['total_score'] 
                        
                                #ep_score += score
                                total_game_score += score 

                            episode_scores.append(total_game_score)
                            interval_counter +=1
               #     total_game_score += ep_score 
                        
                #account for game ending right before 90, 
                #count score from last click of last episode as final point
                if len(episode_scores) != len(score_intervals):
                        
                    final_score = episode_list[-1]['clicked_boxes'][-1]['click_score'] + total_game_score
                    episode_scores.append(final_score)

                        
                frames.append(pd.DataFrame({
                              'participant_ID': [participant_ID]*len(score_intervals),
                              'game': [game_name]*len(score_intervals),
                              'time': score_intervals,
                              'score': episode_scores
                              }))
                
                print(game_name)
                print(game_play[game]['inferred_spec'])
                print('')
                
    participant_ID += 1

result = pd.concat(frames, ignore_index =True)
print(result)

x= result.groupby(['game', 'time'])

means = x['score'].mean()
errors = x['score'].std()

# print(x)
# print(means)
# print(errors)

fig, ax = plt.subplots()
next(ax._get_lines.prop_cycler)
means.groupby('game').plot(x = 'score', y = 'time', marker='.', yerr=errors, capsize=4, rot=0)

#ax.set_xticks(score_intervals)
ax.set_xticklabels([*range(0,101,10)])
ax.set_xlabel('Time')
ax.set_ylabel('Score')
ax.yaxis.set_minor_locator(MultipleLocator(10))
fig.legend(labels=['Game 2', 'Game 3', 'Game 4'])
ax.set_title('Average Game Score over Time')
plt.grid(lw=0.2)
plt.show()

                
                
                
                