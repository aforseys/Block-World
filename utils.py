#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 17:11:42 2022

@author: aforsey
"""
import random
import pygame 

WIDTH = 50
HEIGHT = 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
colors = [RED, GREEN, BLUE]
screen_size = (1400,675)
block_area = (500,500)
min_num = 1
max_num = 4
hovered_green = (0, 175, 0)
hovered_blue = (0,0, 175)
hovered_red = (175,0,0)
pressed_green = (0, 100, 0)
pressed_blue = (0,0, 100)
pressed_red = (100,0,0)
hovered_colors = [hovered_red, hovered_green, hovered_blue]
pressed_colors = [pressed_red, pressed_green, pressed_blue]
num_practice_episodes = 3
num_example_episodes = 3
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
font = pygame.font.SysFont("Segoe UI", 20)
reward_font = pygame.font.SysFont("Segoe UI", 30, GREEN)
error_font = pygame.font.SysFont("Segoe UI", 30, RED)
title_font = pygame.font.SysFont("Segoe UI", 24, BLACK)
subtitle_font = pygame.font.SysFont("Segoe UI", 24, BLACK)
episodes_per_game = 3
  

class block(pygame.sprite.Sprite):
    
    def __init__(self, color, hovered_color, pressed_color, width, height, ID):
        super().__init__()
        self.width = width
        self.height = height
        self.ID = ID
        self.color = color
        
        self.image_normal = pygame.Surface([width, height])
        self.image_normal.fill(WHITE)
        self.image_normal.set_colorkey(WHITE)
        self.image_normal.fill(color)
        self.image = self.image_normal
        self.rect = self.image.get_rect()
         
        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill(WHITE)
        self.image_hovered.set_colorkey(WHITE)
        self.image_hovered.fill(hovered_color)
        
        self.image_pressed = pygame.Surface((width, height))
        self.image_pressed.fill(WHITE)
        self.image_pressed.set_colorkey(WHITE)
        self.image_pressed.fill(pressed_color)
        
        self.hovered = False 
        self.pressed = False
        
    def __getstate__(self):
        
        attributes = self.__dict__.copy()
        del attributes['_Sprite__g']
        del attributes['image_normal']
        del attributes['image_hovered']
        del attributes['image_pressed']
        del attributes['hovered']
        del attributes['pressed']
        del attributes['image']
        del attributes['rect']
        x,y = self.rect.x, self.rect.y
        attributes['pos'] = (x,y)
        
        print(attributes)
        
        return attributes

    def update_hover(self, pos):
        """ Change color if mouse is over the button."""

        if self.rect.collidepoint(pos):
            self.image = self.image_hovered
        else:
            self.image = self.image_normal
            
    def update_press_down(self, pos):
        """ Change color if mouse is over the button."""
        if self.rect.collidepoint(pos):
            self.image = self.image_pressed
            
    def update_press_up(self,pos):
        """ Change color if mouse is over the button."""
        if self.rect.collidepoint(pos):
            self.image = self.image_hovered
            
class button(pygame.sprite.Sprite):
    
    def __init__(self, color, hovered_color, width, height, position, button_text, button_type):
        super().__init__()
        self.width = width
        self.height = height
        self.button_type = button_type
        
        self.image_normal = pygame.Surface([width, height])
        self.image_normal.fill(WHITE)
        self.image_normal.set_colorkey(WHITE)
        self.image_normal.fill(color)
        
        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill(WHITE)
        self.image_hovered.set_colorkey(WHITE)
        self.image_hovered.fill(hovered_color)
        
        font = pygame.font.SysFont('Segoe UI', 20)
        text_image = font.render(button_text, True, BLACK)
        rect = self.image_normal.get_rect()
        text_rect = text_image.get_rect(center=rect.center)

        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)
        
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.hovered = False 
        
    def update(self, pos):
        
        if self.rect.collidepoint(pos):
            self.image = self.image_hovered
        else:
            self.image=self.image_normal
            
        
       
def generate_blocks(min_num, max_num, colors, hovered_colors, pressed_colors, block_size=(50,50)):
    """
    Generates a random number of blocks within provided max and min 
    for each color type passed in. 
    """
    blocks = []
    ID = 0 
    
    for i in range(len(colors)):
        color = colors[i]
        n = random.randint(min_num, max_num)
        for l in range(n):
            new_block = block(color, hovered_colors[i],pressed_colors[i],block_size[0], block_size[1], ID)
            block_loc = generate_block_pos(new_block, blocks) #generate new block location 
            new_block.rect.x = block_loc[0]
            new_block.rect.y = block_loc[1]
            blocks.append(new_block)
            ID +=1

    return blocks

def generate_block_pos(new_block, blocks, block_size=(50,50)):
    
    """
    Generates n blocks equal size that all fit in the provided
    screen size and do not overlap. 
    """
    not_selected = True 
    
    while not_selected:
    
        #randomly select x,y starting points inside the screen size 
        #until one doesn't collide with other blocks 
        x = random.randint(525, block_area[0]+525-block_size[0])
        y = random.randint(25, block_area[1]+25-block_size[1])
        
        test_rect = pygame.Rect((x,y), block_size)
        
        if any([b for b in blocks if pygame.Rect.colliderect(test_rect, b.rect)]):
            continue
        else:
            return (x,y)
    
def generate_buttons(next_episode_text, input_box):
    buttons = []
    next_button = button(color_inactive, color_active, 250, 50, (625, 540), next_episode_text, 'next episode')
    buttons.append(next_button)
    if input_box:
        input_button = button(color_inactive, color_active, 250, 50, (1095, 540), 'Submit Game', 'submit spec')
        buttons.append(input_button)
    return buttons
    
def blit_text(surface, text, pos, font, color=pygame.Color('black'), edge = False):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.    
    max_width, max_height = surface.get_size()
    if edge:
        max_width = edge
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

     
