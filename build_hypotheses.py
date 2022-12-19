#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:11:11 2022

@author: aforsey
"""
import itertools
import json 

def build_hypotheses():
                   
    #all permutations of blocks
    colors = ['red', 'green', 'blue']
    env = ['black', 'white', 'either']

    #get all permutations (with replacement) for 3 possible lengths
    ones = list(itertools.product(colors,repeat=1))
    twos = list(itertools.product(colors, repeat=2))
    threes = list(itertools.product(colors, repeat=3))
    
    ones = [list(l) for l in ones]
    twos = [list(l) for l in twos]
    threes = [list(l) for l in threes]
    
    h_black = []
    h_white = []
    h_either = []
    
   # for hypothesis_set in [h_black, h_white, h_either]:
    for group in [ones,twos,threes]:
        size = len(group[0])
        h_black.extend([{'type':size+1,'black':block_combo, 'white':False, 'either':False} for block_combo in group])
        h_white.extend([{'type':size+1,'black':False, 'white':block_combo, 'either':False} for block_combo in group])
        h_either.extend([{'type':size,'black':False, 'white':False, 'either':block_combo} for block_combo in group])
    
    
    #NOTE: ASSUMPTION THAT WOUDN'T HAVE SAME SPECIFICATION JUST 'BACKGROUND CAN'T CHANGE'
    #BECAUSE DON'T FIND PERMUTATIONS W/ REPLACEMENT 
  #  all_colors = ones+twos+threes
    combos = list(itertools.permutations(ones,2))
    combos = [list(combo) for combo in combos]

    h_combos = [{'type':3, 'black':c[0], 'white':c[1], 'either':False }  for c in combos]
    
 #   h_combos = [{'black': h[0], 'white':h[1], 'type':'double', 'prob':1} for h in h_combos]

    hypotheses =  h_black + h_white + h_either + h_combos
    
    
    
    for i,h in enumerate(hypotheses):
        h["ID"] = i
        
    return hypotheses
    
hypotheses = build_hypotheses()

print(len(hypotheses))

out_file = open("hypotheses_shortened.json", "w")
  
json.dump(hypotheses, out_file)
  
out_file.close()


