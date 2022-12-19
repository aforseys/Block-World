#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 17:08:18 2022

@author: aforsey
"""
import pygame
pygame.init()
from utils import *


def any(click, color):
    if click['color'] == color:
        return True
    return False


def background(click,color):
    if color == WHITE:
        if click['env_white_before']:
            return True
        return False
        
    elif color == BLACK:
        if not click['env_white_before']:
            return True
        return False
    
def check_history(prior_clicks,n, required_background=False):
    checked_clicks = prior_clicks[-n:]
    if required_background:
        if required_background == WHITE:
            if not all([c['env_white_before'] for c in checked_clicks]):
                return False
        elif required_background == BLACK:
          #  print(checked_clicks)
          #  print(all([not(c['env_white_before']) for c in checked_clicks]))
            if not all([not(c['env_white_before']) for c in checked_clicks]):
                return False
        
   # print(checked_clicks)
    return [c['color'] for c in checked_clicks]
    
    
def game1_score(click, prior_clicks):
    """"This game will be to click green boxes. Each click of a green box 
    adds points to a player's score. Each click of a red or blue box has 
    no effect on a player's score."""
    
    if any(click, GREEN):
        return 1

    return 0 
    
    
def game2_score(click, prior_clicks):
    """"The objective of the game is to click the blue square as many times 
    as possible while the black background is present and to also click on 
    the green square as many times as possible while the white background 
    is present. Each of these actions results in one point being awarded. 
    However, if the blue square is clicked while the white background or if 
    the green background is clicked while the black background is present, 
    three points are docked from the score. The red square is neutral and 
    serves no purpose other than changing the background color."""
    
    if background(click, WHITE):
        if any(click, GREEN):
            return 1
        if any(click, BLUE):
            return -3
        if any(click, RED):
            return 0 
        
    elif background(click, BLACK):
        if any(click, GREEN):
            return -3
        if any(click, BLUE):
            return 1
        if any(click,RED):
            return 0
 
def game3_score(click, prior_clicks):
    """"Get one point every time click any red, then any green, then any blue 
    during night. Have to click in that order. When background is white, no 
    points or penalties. Have to start from beginning of order whenever it 
    switches back to night.
    """
    
    if background(click,BLACK):
        if any(click,BLUE):
            if check_history(prior_clicks, 1, required_background=BLACK) == [GREEN]:
                return 1
    return 0 
        
 
def game4_score(click, prior_clicks):
    """Have to click on blue, blue, blue, green, red in repeating order. Points
    are given independent of the color of the background.
    """
    
    #NOTE CHANGED SO ONLY NEED HISTORY OF 3 
    
    if any(click, RED):
        if check_history(prior_clicks, 2) == [BLUE, GREEN]:
            return 1 
    
    return 0 
    
#def game5_score():
    
    
#def game6_score():
    