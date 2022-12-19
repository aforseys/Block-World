#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 17:51:45 2022

@author: aforsey
"""
import pygame
from pygame import mixer
import random
from datetime import datetime
import pickle
pygame.init()

from utils import *
from game_scoring_functions import *
mixer.init()
        
def run_episode(pygame, instructions, game_n=None, episode_n=None, next_episode_text=False, scoring_fcn=False, input_box=False):
    clock = pygame.time.Clock()
    blocks = generate_blocks(min_num, max_num, colors, hovered_colors, pressed_colors)
    all_blocks=pygame.sprite.Group(blocks)
    update_clock = False
    box_score_text = ''
    
    if next_episode_text:
        buttons = generate_buttons(next_episode_text, input_box)
        all_buttons = pygame.sprite.Group(buttons)
        
    if scoring_fcn:
        total_score = 0 
        counter = 30
        pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    episode_stats = {}
    start_time = pygame.time.get_ticks()
    episode_stats['start_time'] = pygame.time.get_ticks()
  
    env = pygame.Rect(525,25,block_area[0],block_area[1])
    
    env_white = random.random()>0.5
    
    episode_stats['env_start_white'] = env_white
    episode_stats['clicked_boxes'] = []
    episode_stats['num_red'] = sum(b.color == RED for b in all_blocks)
    episode_stats['num_blue'] = sum(b.color == BLUE for b in all_blocks)
    episode_stats['num_green'] = sum(b.color == GREEN for b in all_blocks)
    
    episode_running = True
   # active = False
   # spec = False 
    screen.fill(WHITE)
    if scoring_fcn:
        screen.blit(font.render('Time left in this episode: '+str(counter), True, (0, 0, 0)), (200, 125))
    
    while episode_running: 
        screen.fill(WHITE)
      #  print('ths is the time:', clock.get_rawtime())
        env_set = False 
        for event in pygame.event.get():
            
            if event.type == pygame.USEREVENT:
                counter -= 1
                if counter == 0:
                    return episode_stats
                clock_text = 'Time left in this episode: '+ str(counter).rjust(3) 
                update_clock = True
        
        
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                hovered_box = [s for s in all_blocks if s.rect.collidepoint(pos)]
                if next_episode_text:
                    hovered_button = [s for s in all_buttons if s.rect.collidepoint(pos)]
            
                if hovered_box: 
                    hovered_box = hovered_box[0]
                    hovered_box.hovered = True
                    
                elif next_episode_text:
                    if hovered_button: 
                        hovered_button = hovered_button[0]
                        hovered_button.hovered=True
                
                for b in all_blocks:
                    b.update_hover(pos)
                    
                if next_episode_text:
                    for b in all_buttons:
                        b.update(pos)

            elif event.type == pygame.MOUSEBUTTONDOWN: 
                pos = pygame.mouse.get_pos()
                        
                clicked_box = [s for s in all_blocks if s.rect.collidepoint(event.pos)]
                if clicked_box: 
                    clicked_box = clicked_box[0]
                    clicked_box.pressed = True
                    clicked_box_stats = {}
                    clicked_box_stats['ID'] = clicked_box.ID
                    clicked_box_stats['loc'] = (clicked_box.rect.x, clicked_box.rect.y)
                    clicked_box_stats['color'] = clicked_box.color
                    clicked_box_stats['env_white_before'] = env_white
                    clicked_box_stats['click_time'] = pygame.time.get_ticks()
                    
                    if random.random() < 0.2: #flip a coin w/ 0.2 probability of True 
                        #coin flip true, change color of env
                        if env_white: 
                            env_set = True
                            env_white = False
                            pygame.draw.rect(screen, BLACK, env)
                        else:
                            env_set = True 
                            env_white = True
                            pygame.draw.rect(screen, WHITE, env)
                            pygame.draw.rect(screen, BLACK, env, 1)
                            
                    clicked_box_stats['env_white_after'] = env_white
                    
                    if scoring_fcn:
                        box_score = scoring_fcn(clicked_box_stats, episode_stats['clicked_boxes'])
                        clicked_box_stats['click_score'] = box_score
                        total_score += box_score
                        clicked_box_stats['total_score'] = total_score
                        if box_score == 0:
                            box_score_text = ''
                        elif box_score >0:
                            box_score_text = '+'+str(box_score)
                            mixer.music.load("56895^DING.mp3")
                            mixer.music.play()
                        else: 
                            box_score_text = str(box_score)
                            mixer.music.load("error-126627.mp3")
                            mixer.music.play()
                        #print(box_score)
                  #  print([c['color'] for c in episode_stats['clicked_boxes'][-3:1]])
                    episode_stats['clicked_boxes'].append(clicked_box_stats)
                 #   print(episode_stats['clicked_boxes'])
                    
                else:
                    if scoring_fcn:
                        box_score_text = ''
                
                for b in all_blocks:
                    b.update_press_down(pos)
                            
                if next_episode_text:
                    clicked_button = [s for s in all_buttons if s.rect.collidepoint(event.pos)]
                    if clicked_button: 
                        clicked_button = clicked_button[0]
                        if clicked_button.button_type == 'next episode':
                            episode_running = False
                    # elif clicked_button.button_type == 'submit spec':
                    #     episode_running = False
                
           
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                unclicked_box = [s for s in all_blocks if s.rect.collidepoint(event.pos)]
                if unclicked_box:
                    unclicked_box = unclicked_box[0]
                    unclicked_box.pressed = False
                    unclicked_box.hovered = True
                    
                for b in all_blocks:
                    b.update_press_up(pos)
                            
            elif event.type == pygame.QUIT:
                continue #don't let user exit until it's done 
       
        if not env_set:
            if env_white: 
                pygame.draw.rect(screen, WHITE, env)
                pygame.draw.rect(screen, BLACK, env, 1)
            else: 
                pygame.draw.rect(screen, BLACK, env)
   
        all_blocks.draw(screen)
        if next_episode_text:
            all_buttons.draw(screen)
            
        if scoring_fcn:
            screen.blit(title_font.render('Game '+str(game_n),True, (0,0,0)), (200, 25))
            screen.blit(title_font.render('Episode '+str(episode_n),True, (0,0,0)), (200,75))
            screen.blit(font.render('Total episode score: '+ str(total_score), True, (0, 0, 0)), (200,160))
            #if clicked_box:
            
            screen.blit(reward_font.render(box_score_text, True, (0, 0, 0)), (250, 300))
            
        if update_clock:
            screen.blit(font.render(clock_text, True, (0, 0, 0)), (200, 125))
        
        blit_text(screen, instructions, (25,25), font)
        #Updates the screen 
        pygame.display.update()
        pygame.display.flip()
        
        #60 frames per second
        clock.tick(60)
        
    
    if scoring_fcn:
        episode_stats['total_score'] = total_score
    return episode_stats

def display_game_instructions(pygame, instructions):
    waiting = True
    first_game = button(color_inactive, color_active, 200, 100, (625,475), 'start playing games', 'next_game')
    button_group = pygame.sprite.Group([first_game])
    screen.fill(WHITE)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if first_game.rect.collidepoint(event.pos):
                    waiting=False
        
        button_group.draw(screen)
        blit_text(screen, instructions, (300, 50), font)
        #Updates the screen 
        pygame.display.update()
        pygame.display.flip()
        
        #60 frames per second
        clock.tick(60)

def game_transition(pygame):
    waiting = True
    next_game = button(color_inactive, color_active, 200, 100, (600,275), 'Play next game', 'next_game')
    button_group = pygame.sprite.Group([next_game])
    screen.fill(WHITE)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if next_game.rect.collidepoint(event.pos):
                    waiting=False
        
        button_group.draw(screen)
        #blit_text(screen, instructions, (525, 50), font)
        #Updates the screen 
        pygame.display.update()
        pygame.display.flip()
        
        #60 frames per second
        clock.tick(60)

pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Block Game')
clock = pygame.time.Clock()
practice_episodes = []
game_play = {}

def describe_game(pygame, instructions):
    waiting = True
    submit_game = button(color_inactive, color_active, 200, 100, (600,500), 'Submit', 'submit')
    button_group = pygame.sprite.Group([submit_game])
    screen.fill(WHITE)
    tb = pygame.Rect(350,150,700,300)
    active = False
    text = ''
    while waiting:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if submit_game.rect.collidepoint(event.pos):
                    waiting=False
                    
                elif tb.collidepoint(event.pos):
                    active = not active 
                else:
                    active = False 
                    
            elif event.type == pygame.KEYDOWN:
                if active:
                  #  print('active')
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                     #   print(text)
                    
        color_input_box = color_active if active else color_inactive
        pygame.draw.rect(screen, color_input_box, tb,1)
        #borrowed function for allowing input text to move to next line
        blit_text(screen, text, (350,150), font, edge=1050)
        
        button_group.draw(screen)
        blit_text(screen, instructions, (350, 50), font)
        #Updates the screen 
        pygame.display.update()
        pygame.display.flip()
        
        #60 frames per second
        clock.tick(60)
        
    return text

for i in range(num_practice_episodes):
     if i == num_practice_episodes-1:
         next_episode_text = "Next"
     else: 
         next_episode_text = "Next practice episode"
     instructions = """Welcome, and thank you for participating! Please read 
the below instructions:

In this experiment you will be asked to play a 
series of games in the block world environment. 
You will begin the experiment by familiarizing 
yourself with the block world environment. To the
right is an example of one instance of the block
world environment, which will be referred to as 
an episode. Each episode will have a random 
number red, blue, and green blocks. There will 
always be at least one block of each color in each
episode. The only action you can take as a player 
in the environment is to click on any of the 
blocks. The background of each episode is 
initialized randomly as either white or black. The
background color changes between white and black 
with a small chance any time any block is clicked.

Play in the environment by clicking on blocks. 
Generate a new episode of the environment by
selecting 'Next practice episode'. You will be given 
the chance to play in three environment episodes 
before you will be asked to play a game. 
     """
     episode_stats = run_episode(pygame, instructions, next_episode_text=next_episode_text)
     practice_episodes.append(episode_stats)

game_instructions = """
You will now play a series of games in the block world environment. In each game the only action
you are allowed to play is to click any block. Each game has a scoring system. 

The one catch is that you do not know the scoring system of each game beforehand. Therefore,
you will have to uncover the scoring system while you play in the environment. While you 
are playing each game, you will be shown a point value and hear a noise if you 
receive or lose points after an action. 

You will play a series of four games. Your goal is to maximize your points acrued for each game. 
You will have 90 seconds to play each game. The episode in which you are playing a game will 
change every 30 seconds, therefore, you will play in three different episodes for each game. 
A count down timer will be shown next to the environment to display the total time you have left
in an episode. Additionally, a running total of your points for an episode will be shown to the 
left of the episode. Again, your goal is to maximize the points you acrue for each game.
"""

describe_instructions = """
Please do your best to describe what you think the scoring function was for that game. 

NOTE: Please do not use enter key when writing in text box (no new paragraphs).
"""

#display_game_instructions(pygame, game_instructions)
display_game_instructions(pygame, game_instructions)

games = [game1_score, game2_score, game3_score, game4_score]
random.shuffle(games)
game_play['order'] = [str(g) for g in games]
#print(games)

for i, game in enumerate(games):
    if i!=0:
        game_transition(pygame)
    game_play[str(game)] = {}
    game_play[str(game)]['episodes'] = []
    for j in range(episodes_per_game):
        episode_stats = run_episode(pygame, '', game_n=i+1, episode_n=j+1, scoring_fcn=game)
        game_play[str(game)]['episodes'].append(episode_stats)
    inferred_rules = describe_game(pygame, describe_instructions)
    game_play[str(game)]['inferred_spec'] = inferred_rules
pygame.quit()    

filename = 'game_play' + datetime.now().strftime("%Y%m%d_%H%M%S")

with open(filename, 'wb') as handle:
    pickle.dump([practice_episodes, game_play], handle, protocol=pickle.HIGHEST_PROTOCOL)

