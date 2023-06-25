#! python3

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



class Interface:
    """
    Generates the interface.
    sets a default for
    """
    def __init__(self):
        pyg.init()
        pyg.display.set_caption('Quick Start')
        self.displaytype = DISPLAYSIZE1
        self.screentype = SCREENSIZE1
        self.window_surface = pyg.display.set_mode(self.displaytype)
        self.background = pyg.Surface(self.screentype)
        self.background.fill(pyg.Color('black'))
        self.manager = pygui.UIManager(self.displaytype)
        self.screenrect = self.window_surface.get_rect() 

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
            self.displaytype = displaytype
            if self.displaytype == DISPLAYSIZE1:
                self.screentype = SCREENSIZE1
            if self.displaytype == DISPLAYSIZE2:
                self.screentype = SCREENSIZE2
            if self.displaytype == DISPLAYSIZE3:
                self.screentype = SCREENSIZE3
        except:
            self.displaytype = DISPLAYSIZE1
            self.screentype = SCREENSIZE1

        self.window_surface = pyg.display.set_mode(self.displaytype)
        self.background = pyg.Surface(self.screentype)
        self.background.fill(pyg.Color('black'))
        self.manager = pygui.UIManager(self.displaytype)
        self.screenrect = self.window_surface.get_rect() 
        # set up the positions of each of the buttons along the left 100 pixels of the screen.        
        self.food_button = pygui.elements.UIButton(relative_rect =pyg.Rect((self.screentype[0], 0),BUTTONSIZE),
                                                    text = 'Food',
                                                    manager=self.manager)
        self.wall_button = pygui.elements.UIButton(relative_rect =pyg.Rect((self.screentype[0], 50),BUTTONSIZE),
                                                    text = 'Wall',
                                                    manager=self.manager)
        self.spawn_button = pygui.elements.UIButton(relative_rect =pyg.Rect((self.screentype[0], 100),BUTTONSIZE),
                                                    text = 'Spawn Ant',
                                                    manager=self.manager)
        self.map1_button = pygui.elements.UIButton(relative_rect=pyg.Rect((self.screentype[0], 150), BUTTONSIZE),
                                                    text='Load Map1',
                                                    manager=self.manager)
        self.map2_button = pygui.elements.UIButton(relative_rect=pyg.Rect((self.screentype[0], 200), BUTTONSIZE),
                                                    text='Load Map2',
                                                    manager=self.manager)
        self.map3_button = pygui.elements.UIButton(relative_rect=pyg.Rect((self.screentype[0], 250), BUTTONSIZE),
                                                    text='Load Map3',
                                                    manager=self.manager)
        self.reset_button = pygui.elements.UIButton(relative_rect =pyg.Rect((self.screentype[0], 300),BUTTONSIZE),
                                                    text = 'Reset',
                                                    manager=self.manager)
        self.pause_button = pygui.elements.UIButton(relative_rect=pyg.Rect((self.screentype[0], 350), BUTTONSIZE),
                                                    text='PAUSE', 
                                                    manager=self.manager)
        # tool_tip_text=
        self.refresh()


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
        pass

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


    def button_change(self, button_type):
        #if self.button_type == default:
        pass

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
                    #display.food_button.element_ids  ###
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
                    if brush == 'NEST':
                        brush = None
                    else:
                        brush = 'NEST'
                    print(brush)

            # Reset and Load the 1st map  
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.map1_button:
                    display.setDisplay(DISPLAYSIZE1)

            # Reset and Load the 2rd map  
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.map2_button:
                    display.setDisplay(DISPLAYSIZE2)
                
            # Reset and Load the 3rd map    
            if event.type == pygui.UI_BUTTON_PRESSED:
                if event.ui_element == display.map3_button:
                    display.setDisplay(DISPLAYSIZE3)
            #------------------------------------------------------- mouse events
            # Draws on the screen, the selected type (Food or Wall)
            if event.type == pyg.MOUSEBUTTONDOWN:
                target_position = pyg.mouse.get_pos()
                if display.screenrect.collidepoint(target_position):
                    if event.button == 1:
                        draw = True
                        if brush == 'NEST':
                            display.spawn_nest (target_position)
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
    main()