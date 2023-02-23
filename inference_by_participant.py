#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:39:21 2023

@author: aforsey
"""
import os
import pandas as pd
import pickle

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

def perform_inference(file, participant_data):
    #priors = [0.5,0.5,0.5,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333,0.3333333333333333]
    #normalized_priors = [float(i)/sum(priors) for i in priors]
    
    #model_data={}
    
    os.system(f"mkdir /Users/aforsey/Desktop/Block\ World\ Final\ Project/DATA/inference_json_files/{file}")
              
    
    for game_num in range(1,5): #for each of the four games 
        game_name="game"+str(game_num)
        output_folder = f"/Users/aforsey/Desktop/Block\ World\ Final\ Project/DATA/inference_json_files/{file}/{game_name}/"
        
        os.system(f"mkdir {output_folder}")
        
        upper_bound = participant_data[game_name]['clicks'].iloc[-1] #gets number of total clicks from participant data
        
        #mkdir 
        #set output location (folder)
    
        for i in range(5,upper_bound+1,5):
            os.system(f"webppl wppl_model.wppl --require webppl-json -- --participant {file} --game {game_name} --bound {i} --output {output_folder}") #runs inference with each section of data, saves to json file 

if __name__ == "__main__":
    # options = "p:"
    # long_options= ["Participant="]
    # args = sys.argv[1:]
    # try: 
    #     arguments,vals = getopt.getopt(args, options, long_options)
    # except getopt.error as err:
    #     print(str(err))
        
   # ID = vals[0] #check this
    for ID in range(1,11):
        participant_data, file = process_participant_scores(ID)
    #print(participant_data["game1"]['clicks'].iloc[-1])
    #print(participant_data)
        model_data = perform_inference(file, participant_data) #need participant data as input to get number of clicks
    # plot_participant(participant_data, model_data)


        #print(model_output)
            #game_DF.loc[i] = model_output
            
        #model_data[game_name] = game_DF
    
#    return model_data

# if __name__ == "__main__":
#     perform_inference()
    
#     options = "p:"
#     long_options= ["Participant="]
#     args = sys.argv[1:]
#     try: 
#         arguments,vals = getopt.getopt(args, options, long_options)
#     except getopt.error as err:
#         print(str(err))
        
#     ID = vals[0] #check this
#     model_data = perform_inference(ID)
   # save_data(model_data)
 