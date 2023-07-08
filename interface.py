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
        # tool_tip_text=

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




def main():
    '''
    '''
    # Initialisation
    display = Interface()
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
    '''
    '''
    main()