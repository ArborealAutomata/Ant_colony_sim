#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "James Davis"
__version__ = "0.1.2"
__license__ = "MIT"

import os
import pygame as pyg
import pygame_gui as pygui
import enviro


"""
DISPLAYSIZE: this is the whole program box on the screen
SCREENSIZE: this is just the area of the box that is used to display
"""
DISPLAYSIZE1 = (800, 600)
SCREENSIZE1 = (700, 600)
DISPLAYSIZE2 = (640, 480)
SCREENSIZE2 = (540, 480)
DISPLAYSIZE3 = (1080, 750)
SCREENSIZE3 = (980, 750)
BUTTONSIZE = (100, 50)

CURRENT_DIR = os.getcwd()
DATA_PATH = CURRENT_DIR +'/data'
THEME_PATH = os.path.join(DATA_PATH, 'theme.json')

class Interface:
    """
    Generates the interface.
    sets a default for
    """
    def __init__(self):
        pyg.init()
        pyg.display.set_caption('Quick Start')
        self.display_type = DISPLAYSIZE1
        self.screen_type = SCREENSIZE1
        self.window_surface = pyg.display.set_mode(self.display_type)
        self.background = pyg.Surface(self.screen_type)
        self.background.fill(pyg.Color('black'))
        self.manager = pygui.UIManager(self.display_type, THEME_PATH)
        self.screenrect = self.window_surface.get_rect() 
        self.paused = True
        self.mode = ''

        self.food_group = pyg.sprite.Group()
        self.wall_group = pyg.sprite.Group()
        self.nest_group = pyg.sprite.GroupSingle()
        self.ants = pyg.sprite.Group()
        self.pos_pheromone = pyg.sprite.Group()
        self.neg_pheromone =  pyg.sprite.Group()


    def setDisplay(self, displaytype = DISPLAYSIZE1):
        """
        When a button is clicked to change the display type, the old screen 
        is closed and a new one has to be created, this change in screen 
        size means the layout has to be rearranged.
        """
        # Catch errors
        try:
            self.display_type = displaytype
            if self.display_type == DISPLAYSIZE1:
                self.screen_type = SCREENSIZE1
            if self.display_type == DISPLAYSIZE2:
                self.screen_type = SCREENSIZE2
            if self.display_type == DISPLAYSIZE3:
                self.screen_type = SCREENSIZE3
        except:
            self.display_type = DISPLAYSIZE1
            self.screen_type = SCREENSIZE1

        self.window_surface = pyg.display.set_mode(self.display_type)
        self.background = pyg.Surface(self.screen_type)
        self.background.fill(pyg.Color('black'))
        self.manager = pygui.UIManager(self.display_type)
        self.screenrect = self.window_surface.get_rect() 
        # set up the positions of each of the buttons along the left 100 pixels of the screen.        
        self.food_button = pygui.elements.UIButton(relative_rect =pyg.Rect((self.screen_type[0], 0),BUTTONSIZE),
                                                    text = 'Food',
                                                    manager=self.manager,
                                                    tool_tip_text='Click to begin or stop drawing food on the map'
                                                    )
        self.wall_button = pygui.elements.UIButton(relative_rect =pyg.Rect((self.screen_type[0], 50),BUTTONSIZE),
                                                    text = 'Wall',
                                                    manager=self.manager,
                                                    tool_tip_text='Click to begin or stop drawing walls on the map'
                                                    )
        self.spawn_button = pygui.elements.UIButton(relative_rect =pyg.Rect((self.screen_type[0], 100),BUTTONSIZE),
                                                    text = 'Spawn Ant',
                                                    manager=self.manager,
                                                    tool_tip_text='Click to select a spawn point for the colony'
                                                    )
        self.map1_button = pygui.elements.UIButton(relative_rect=pyg.Rect((self.screen_type[0], 150), BUTTONSIZE),
                                                    text='Load Map1',
                                                    manager=self.manager,
                                                    tool_tip_text= f'Changes the map size to: {SCREENSIZE1}, this will reset the program'
                                                    )
        self.map2_button = pygui.elements.UIButton(relative_rect=pyg.Rect((self.screen_type[0], 200), BUTTONSIZE),
                                                    text='Load Map2',
                                                    manager=self.manager,
                                                    tool_tip_text=f'Changes the map size to: {SCREENSIZE2}, this will reset the program'
                                                    )
        self.map3_button = pygui.elements.UIButton(relative_rect=pyg.Rect((self.screen_type[0], 250), BUTTONSIZE),
                                                    text='Load Map3',
                                                    manager=self.manager,
                                                    tool_tip_text=f'Changes the map size to: {SCREENSIZE3}, this will reset the program'
                                                    )
        self.reset_button = pygui.elements.UIButton(relative_rect =pyg.Rect((self.screen_type[0], 300),BUTTONSIZE),
                                                    text = 'Reset',
                                                    manager=self.manager,
                                                    tool_tip_text='Resets the map to initial starting conditions'
                                                    )
        self.pause_button = pygui.elements.UIButton(relative_rect=pyg.Rect((self.screen_type[0], 350), BUTTONSIZE),
                                                    text='PAUSE', 
                                                    manager=self.manager,
                                                    tool_tip_text='Press to pause / start / resume the program'
                                                    )

        self.map1_button.is_selected = True
        self.pause()
        self.refresh()

    def food_clicked(self):
        self.mode = 'FOOD'
        self.env_object_deactivate()
        self.food_button.is_selected = True

    def wall_clicked(self):
        self.mode = 'WALL'
        self.env_object_deactivate()
        self.wall_button.is_selected = True

    def spawn_clicked(self):
        self.mode = 'SPAWN'
        self.env_object_deactivate()
        self.spawn_button.is_selected = True

    def map_1_clicked(self):
        self.setDisplay(DISPLAYSIZE1)
        self.map_change_deactivate()
        self.map1_button.disable()
        self.reset()

    def map_2_clicked(self):
        self.setDisplay(DISPLAYSIZE2)
        self.map_change_deactivate()
        self.map2_button.disable()
        self.reset()

    def map_3_clicked(self):
        self.setDisplay(DISPLAYSIZE3)
        self.map_change_deactivate()
        self.map3_button.disable()
        self.reset()

    def env_object_deactivate(self):
        self.food_button.is_selected = False
        self.wall_button.is_selected = False
        self.spawn_button.is_selected = False

    def map_change_deactivate(self):
        self.map1_button.enable()
        self.map2_button.enable()
        self.map3_button.enable()

    def reset(self):
        '''
        clears the current session, resets back to the initial conditions of the current screen.
        '''
        self.food_group.empty()
        self.wall_group.empty()
        self.nest_group.empty()
        self.ants.empty()
        self.pos_pheromone.empty()
        self.neg_pheromone.empty()
        self.refresh()

    def pause(self):
        '''
        Freezes the screen as it is.
        '''
        if self.paused is True:
            self.pause_button.set_text('PLAY')
            self.pause_button.is_selected = True
            self.paused = False

        elif self.paused is False:
            self.pause_button.set_text('PAUSE')
            self.pause_button.is_selected = False
            self.paused = True


    def refresh(self):
        '''
        update the display
        '''
        self.background.fill(pyg.Color('black'))
        self.food_group.update()
        self.food_group.draw(self.background)
        self.wall_group.update()
        self.wall_group.draw(self.background)
        self.nest_group.update()
        self.nest_group.draw(self.background)
        pyg.display.update()

    def test_collision(self, item):
        food_test = pyg.sprite.spritecollideany(item, self.food_group) 
        wall_test = pyg.sprite.spritecollideany(item, self.wall_group)
        nest_test = pyg.sprite.spritecollideany(item, self.nest_group) 
        if not food_test and not wall_test and not nest_test:
            return True
        else:
            return False

    def spawn_food(self, location):
        food = enviro.Food(location)
        if self.test_collision(food) is True:
            self.food_group.add(food)
        
    def spawn_wall(self, location):
        wall = enviro.Wall(location)
        if self.test_collision(wall) is True:
            self.wall_group.add(wall)

    def spawn_nest(self, location):
        nest = enviro.Nest(location)
        if self.test_collision(nest) is True:
            self.nest_group.add(nest)
