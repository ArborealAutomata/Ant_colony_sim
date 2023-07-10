#!/usr/bin/env python3
"""
The executable. Run this.
"""
__author__ = "James Davis"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import random
import pygame as pyg
import pygame_gui as pygui
import numpy
import Ant
import enviro
import interface

CURRENT_DIR = os.getcwd()
DATA_PATH = CURRENT_DIR +'/data'

def main():
    '''
    '''
    # Initialisation
    display = interface.Interface()
    display.setDisplay()
    clock = pyg.time.Clock()
    is_running = True
    brush = None
    draw = False

    while is_running:
        time_delta = clock.tick(60)/1000.0
        
        for event in pyg.event.get():
            ##### QUIT #####
            if event.type == pyg.QUIT:
                is_running = False
            #------------------------------------------------------- UI events
            ##### PAUSE #####
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.pause_button:
                    display.pause()
                    print('Hello World!')

            ##### RESET #####
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.reset_button:
                    draw = False
                    brush = None
                    display.reset()

            ##### DRAW FOOD #####
            # When clicked on the screen 
            # if there is no wall or food at that point (doesn't overlap an existing entity)
            # adds a new one when mouse1 is pressed
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.food_button:
                    display.food_clicked()
                    if brush == 'FOOD':
                        brush = None
                    else:
                        brush = 'FOOD'
                    print(brush)

            ##### DRAW WALL #####
            # When clicked on the screen 
            # if there is no wall or food at that point (doesn't overlap an existing entity)
            # adds a new one when mouse 1 is pressed
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.wall_button:
                    display.wall_clicked()
                    if brush == 'WALL':
                        brush = None
                    else:
                        brush = 'WALL'
                    print(brush)
                    #once clicked, changes to the button colour to indicate it is selected
                    #if the colour is already of the colour that indicates it is selected
                    #then sets to default
                    # sets the brush type to wall once selected so when the user clicks on the 
                    # it spawns wall entitys there.

            ##### SPAWN ANTS #####
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.spawn_button:
                    display.spawn_clicked()
                    if brush == 'NEST':
                        brush = None
                    else:
                        brush = 'NEST'
                    print(brush)

            # Reset and Load the 1st map  
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.map1_button:
                    display.map_1_clicked()

            # Reset and Load the 2rd map  
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.map2_button:
                    display.map_2_clicked()
                
            # Reset and Load the 3rd map    
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.map3_button:
                    display.map_3_clicked()
            #------------------------------------------------------- mouse events
            # Draws on the screen, the selected type (Food or Wall)
            if event.type == pyg.MOUSEBUTTONDOWN:
                target_position = pyg.mouse.get_pos()
                if display.screenrect.collidepoint(target_position):
                    if event.button == 1:
                        draw = True
                        if brush == 'NEST':
                            display.spawn_nest(target_position)
                        print(draw)
                        # per cycle test if the target position is
                        # over another object, it will not draw
                        # hoever if the space is empty draw, do until the mouse
                        # button is lifted.
                if event.button == 2:
                    brush = None
                    draw = False

            if event.type == pyg.MOUSEMOTION:
                if draw:
                    target_position = pyg.mouse.get_pos()
                    if brush == 'FOOD':
                        display.spawn_food(target_position)  
                    elif brush == 'WALL':
                        display.spawn_wall(target_position) 
                    else:
                        draw = False
                    
            # 
            if event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    draw = False
                    
                        
            display.manager.process_events(event)

        display.manager.update(time_delta)

        display.window_surface.blit(display.background, (0, 0))
        display.manager.draw_ui(display.window_surface)
        display.refresh()
    


if __name__ == "__main__":
    """  """
    main()