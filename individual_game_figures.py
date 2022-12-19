#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 21:08:47 2022

@author: aforsey
"""

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
import numpy as np

from participant_data import P5_G2_DF, P9_G4_DF, P5_G3_DF, P2_G4_DF, P6_G3_DF, P10_G2_DF, P2_G1_DF, P3_G1_DF


import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

directory = os.getcwd()+ '/DATA/game_play'


#score_intervals = [*range(10,91,10)]
frames = []
participant_ID=0

for file in os.listdir(directory):
    print(file)
    with open(directory+'/'+file, 'rb') as f:
        practice_episodes, game_play = pickle.load(f)
        participant_ID += 1
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
                                
                        
                frames.append(pd.DataFrame({
                              'participant_ID': [participant_ID]*len(episode_scores),
                              'game': [game_name]*len(episode_scores),
                              'clicks': [*range(0,counter+1,5)],
                              'score': episode_scores
                              }))
    
                   

result = pd.concat(frames, ignore_index =True)
#print(result)

p1 = result.loc[result['participant_ID'] == 1]
p2 = result.loc[result['participant_ID'] == 2]
p3 = result.loc[result['participant_ID'] == 3]
p4 = result.loc[result['participant_ID'] == 4]
p5 = result.loc[result['participant_ID'] == 5]
p6 = result.loc[result['participant_ID'] == 6]
p7 = result.loc[result['participant_ID'] == 7]
p8 = result.loc[result['participant_ID'] == 8]
p9 = result.loc[result['participant_ID'] == 9]
p10 = result.loc[result['participant_ID'] == 10]


#p1.pivot_table(index = 'clicks', columns='game', values='score'
#               ).plot(subplots=True)

p2_g1_clicks = p2.loc[p2['game'] == 'game1']
p2_g4_clicks = p2.loc[p2['game'] == 'game4']

p3_g1_clicks = p3.loc[p3["game"] == "game1"]

p5_g2_clicks = p5.loc[p5['game'] == 'game2']
p5_g3_clicks = p5.loc[p5['game'] == 'game3']

p6_g3_clicks = p6.loc[p6['game'] == 'game3']

p9_g4_clicks = p9.loc[p9['game'] == 'game4']

p10_g2_clicks = p10.loc[p10['game'] == 'game2']


#Make plots for both incorrect and correct specifications for each game 

#GAME 2 
fig, (a1,a2) = plt.subplots(2, 1)
fig.tight_layout(pad=1.0)
p5_g2_clicks = p5.loc[p5['game'] == 'game2'].plot(x= 'clicks', y='score', ax=a1, title='P5 Game 2 (Incorrect Scoring Structure Inferred)', legend=False, xlabel='', ylabel='Participant Score', marker='.')
P5_G2_DF.plot(legend=False, ax=a2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.')
a1.grid(lw=0.2)
a2.grid(lw=0.2)

fig, (b1,b2) = plt.subplots(2, 1)
fig.tight_layout(pad=1.0)
p10_g2_clicks = p10.loc[p10['game'] == 'game2'].plot(x= 'clicks', y='score', ax=b1, title='P10 Game 2 (Correct Spcoring Structure Inferred)', legend=False, xlabel='', ylabel='Participant Score', marker='.')
P10_G2_DF.plot(legend=False, ax=b2,  xlabel='Number of Blocks Clicked', ylabel="Hypothesis Probability", marker='.')
b1.grid(lw=0.2)
b2.grid(lw=0.2)


#GAME 1
fig, (c1,c2) = plt.subplots(2, 1)
fig.tight_layout(pad=1.0)
p3_g1_clicks = p3.loc[p3['game'] == 'game1'].plot(x= 'clicks', y='score', ax=c1, title='P3 Game 1 (Correct Scoring Structure Inferred)', legend=False, xlabel='', ylabel='Participant Score', marker='.')
P3_G1_DF.plot(legend=False, ax=c2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.')
c1.grid(lw=0.2)
c2.grid(lw=0.2)

fig, (d1,d2) = plt.subplots(2, 1)
fig.tight_layout(pad=1.0)
p2_g1_clicks = p2.loc[p2['game'] == 'game1'].plot(x= 'clicks', y='score', ax=d1, title='P2 Game 1  (Incorrect Scoring Structure Inferred)', legend=False, xlabel='', ylabel='Participant Score', marker='.')
P2_G1_DF.plot(legend=False, ax=d2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.')
d1.grid(lw=0.2)
d2.grid(lw=0.2)


#GAME 3
fig, (e1,e2) = plt.subplots(2, 1)
fig.tight_layout(pad=1.0)
p6_g3_clicks = p6.loc[p6['game'] == 'game3'].plot(x= 'clicks', y='score', ax=e1, title='P6 Game 3  (Correct Scoring Structure Inferred)', legend=False, xlabel='', ylabel='Participant Score', marker='.')
P6_G3_DF.plot(legend=False, ax=e2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.')
e1.grid(lw=0.2)
e2.grid(lw=0.2)

fig, (f1,f2) = plt.subplots(2, 1)
fig.tight_layout(pad=1.0)
p5_g3_clicks = p5.loc[p5['game'] == 'game3'].plot(x= 'clicks', y='score', ax=f1, title='P5 Game 3  (Inorrect Scoring Structure Inferred)', legend=False, xlabel='', ylabel='Participant Score', marker='.')
P5_G3_DF.plot(legend=False, ax=f2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.')
f1.grid(lw=0.2)
f2.grid(lw=0.2)


#GAME 4
fig, (g1,g2) = plt.subplots(2, 1)
fig.tight_layout(pad=1.0)
p2_g4_clicks = p2.loc[p2['game'] == 'game4'].plot(x= 'clicks', y='score', ax=g1, title='P2 Game 4  (Correct Scoring Structure Inferred)', legend=False, xlabel='', ylabel='Participant Score', marker='.')
P2_G4_DF.plot(legend=False, ax=g2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.')
g1.grid(lw=0.2)
g2.grid(lw=0.2)

fig, (h1,h2) = plt.subplots(2, 1)
fig.tight_layout(pad=1.0)
p9_g4_clicks = p9.loc[p9['game'] == 'game4'].plot(x= 'clicks', y='score', ax=h1, title='P9 Game 4  (Incorrect Scoring Structure Inferred)', legend=False, xlabel='', ylabel='Participant Score', marker='.')
P9_G4_DF.plot(legend=False, ax=h2,xlabel="Number of Blocks Clicked", ylabel="Hypothesis Probability", marker='.')
h1.grid(lw=0.2)
h2.grid(lw=0.2)

plt.show()


                
                
                