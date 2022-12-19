#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 16:44:03 2022

@author: aforsey
"""

import pygame
import random 
import pickle
from datetime import datetime

pygame.init()

from utils import *
        
def run_episode(pygame, instructions, next_episode_text, input_box=False, text = '', add_spec = False):
    blocks = generate_blocks(min_num, max_num, colors, hovered_colors, pressed_colors)
    buttons = generate_buttons(next_episode_text, input_box)
    
    all_blocks=pygame.sprite.Group(blocks)
    all_buttons = pygame.sprite.Group(buttons)
    
    episode_stats = {}
  
    env = pygame.Rect(525,25,block_area[0],block_area[1])
  
    if input_box:
        tb = pygame.Rect(1050,25,350,500) #add input textbox
    
    env_white = random.random()>0.5
    
    episode_stats['env_start_white'] = env_white
    episode_stats['clicked_boxes'] = []
    episode_stats['num_red'] = sum(b.color == RED for b in all_blocks)
    episode_stats['num_blue'] = sum(b.color == BLUE for b in all_blocks)
    episode_stats['num_green'] = sum(b.color == GREEN for b in all_blocks)
    
    episode_running = True
    active = False
    spec = False 
    screen.fill(WHITE)
    
    while episode_running: 
        screen.fill(WHITE)
        env_set = False 
        for event in pygame.event.get():
        
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                hovered_box = [s for s in all_blocks if s.rect.collidepoint(pos)]
                hovered_button = [s for s in all_buttons if s.rect.collidepoint(pos)]
            
                if hovered_box: 
                    hovered_box = hovered_box[0]
                    hovered_box.hovered = True
                    
                elif hovered_button: 
                    hovered_button = hovered_button[0]
                    hovered_button.hovered=True
                
                for b in all_blocks:
                    b.update_hover(pos)
                    
                for b in all_buttons:
                    b.update(pos)

            elif event.type == pygame.MOUSEBUTTONDOWN: 
                pos = pygame.mouse.get_pos()

                if input_box: 
                    if tb.collidepoint(pos):
                        active = not active
                    else: 
                        active = False 
                        
                clicked_box = [s for s in all_blocks if s.rect.collidepoint(event.pos)]
                if clicked_box: 
                    clicked_box = clicked_box[0]
                    clicked_box.pressed = True
                
                    clicked_box_stats = {}
                    clicked_box_stats['ID'] = clicked_box.ID
                    clicked_box_stats['loc'] = (clicked_box.rect.x, clicked_box.rect.y)
                    clicked_box_stats['color'] = clicked_box.color
                    clicked_box_stats['env_white_before'] = env_white
                    
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
                    episode_stats['clicked_boxes'].append(clicked_box_stats)
                            
                for b in all_blocks:
                    b.update_press_down(pos)
                            
                clicked_button = [s for s in all_buttons if s.rect.collidepoint(event.pos)]
                if clicked_button: 
                    clicked_button = clicked_button[0]
                    if clicked_button.button_type == 'next episode':
                        episode_running = False
                    elif clicked_button.button_type == 'submit spec':
                        episode_running = False
                        spec = text
                        print(spec)
           
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                unclicked_box = [s for s in all_blocks if s.rect.collidepoint(event.pos)]
                if unclicked_box:
                    unclicked_box = unclicked_box[0]
                    unclicked_box.pressed = False
                    unclicked_box.hovered = True
                    
                for b in all_blocks:
                    b.update_press_up(pos)
                
                
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode                
                            
            elif event.type == pygame.QUIT:
                continue #don't let user exit until it's done 
       
        if not env_set:
            if env_white: 
                pygame.draw.rect(screen, WHITE, env)
                pygame.draw.rect(screen, BLACK, env, 1)
            else: 
                pygame.draw.rect(screen, BLACK, env)
   
        all_blocks.draw(screen)
        all_buttons.draw(screen)
        blit_text(screen, instructions, (25,25), font)
        
        if add_spec:
            blit_text(screen, add_spec, (1050,25), font)
        
        if input_box: 
            color_input_box = color_active if active else color_inactive
            pygame.draw.rect(screen, color_input_box, tb,1)
            #borrowed function for allowing input text to move to next line
            blit_text(screen, text, (1050,25), font)
            
        #Updates the screen 
        pygame.display.update()
        pygame.display.flip()
        
        #60 frames per second
        clock.tick(60)
    
    return episode_stats, text, spec


pygame.init()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Block Game')
clock = pygame.time.Clock()
        
game_spec = False 
text = ''

practice_episodes = []
defining_episodes = []
example_episodes = []
        
for i in range(num_practice_episodes):
     if i == num_practice_episodes-1:
         next_episode_text = "Next"
     else: 
         next_episode_text = "Next practice episode"
     instructions = """Welcome, and thank you for participating! Please read 
the below instructions:

In this experiment you will be asked to come up with
a game that can be played in the block world 
environment. You will begin the experiment by 
familiarizing yourself with the block world 
environment. To the right is an example of one 
instance of the block world environment, which
will be referred to as an episode. Each 
episode will have a random number of red, blue,
and green blocks. There will always be at least
one block of each color in each epsiode. The 
only action a player can take in the environment
is to click on any of the blocks. The background
of each episode is initialized randomly as 
either white or black. The background color 
changes between white and black with a small chance
any time any block is clicked. 

Play in the environment by clicking on blocks. 
Generate a new episode of the environment by
selecting 'Next practice episode'. You will be given 
the chance to play in three environment episodes 
before you will be asked to generate a game. 
     """
     episode_stats, _, _ = run_episode(pygame, instructions, next_episode_text)
     practice_episodes.append(episode_stats)
    
while not game_spec:
    next_episode_text = "Generate new episode"
    instructions = """Instructions: 
        
You will now specify a simple game that can be 
played in any randomly initialized instance of 
the block world environment. The game will be 
played in a timed session. The game specified 
should:
    1. Be for a single player 
    2. Require no additions to the environment 
    3. Include a scoring system 

Click and type in the blue text box on the far 
right to describe your game. You may continue 
to play in the environment while you specify 
a game. If you would like to generate a new 
epsiode to play in, select 'Generate new 
episode'. 

NOTE: Please do not use enter key when writing 
in the text box (no new paragraphs).

When you are finished specifying your game, 
select 'Submit Game'. You will NOT be able to 
change your game specification after you submit 
your game. After you submit your game, you will 
be asked to provide three examples of game play 
in three different environment episodes."""
    episode_stats, text, game_spec = run_episode(pygame, instructions, next_episode_text, input_box=True, text=text)
    defining_episodes.append(episode_stats)

for i in range(num_example_episodes):
    if i == num_example_episodes-1:
        next_episode_text = "Finish"
    else: 
        next_episode_text = "Next example episode"
    instructions = """Instructions:
        
You will now provide examples of optimal 
game play for the game you just specified 
in three different environment episodes. 

Please demonstrate optimal game play in 
the provided episode until the game is 
finished or until you think you have clearly 
demonstrated optimal game play for that 
episode. Then select 'Next example episode' 
to move on to the next epsiode example. You 
will be asked to provide three total 
examples.""" #add on this display a box displaying the game specification 
    episode_stats,_,_ = run_episode(pygame, instructions, next_episode_text, add_spec = "Specified Game:\n"+game_spec)
    
   # print(episode_stats)
    example_episodes.append(episode_stats)

pygame.quit()

filename = 'game_spec' + datetime.now().strftime("%Y%m%d_%H%M%S")

with open(filename, 'wb') as handle:
    pickle.dump([practice_episodes, defining_episodes, example_episodes, game_spec], handle, protocol=pickle.HIGHEST_PROTOCOL)
