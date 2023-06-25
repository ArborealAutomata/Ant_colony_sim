import pygame

#colours of sprites
FOOD = (0,255,0)
WALL =  (255,255,255)
NEST = (255,255,0)
#pheromone colours
ATTRACT = (0,0,255)
REPEL = (255,0,0)
# rect size per sprite
FOOD_SIZE = (6,6)
WALL_SIZE = (30,30)
NEST_SIZE = (20,20)
PHEROMONE_SIZE = (4,4)
# Rate of evaporation per cycle
EVAPORATE_RATE = 5
#pheromone lifespan / duration
HEALTH = 300

class enviro_element(pygame.sprite.Sprite):
    """
    Base class for all enviroment element sprites
    """
    def __init__(self):
        super().__init__()


    def set_position(self, x, y):
        self.rect.center = (x,y)

    def position(self):
        return self.rect.center
    

class Food(enviro_element):
    """
    """
    def __init__(self, location):
        super().__init__()
        self.image = pygame.Surface(FOOD_SIZE)
        self.image.fill(FOOD)
        self.rect = self.image.get_rect()
        self.rect.center = location
        

class Wall(enviro_element):
    """
    """
    def __init__(self, location):
        super().__init__()
        self.image = pygame.Surface(WALL_SIZE)
        self.image.fill(WALL)
        self.rect = self.image.get_rect()
        self.rect.center = location
        

class Nest(enviro_element):
    """
    """
    def __init__(self, location):
        super().__init__()
        self.image = pygame.Surface(NEST_SIZE)
        self.image.fill(NEST)
        self.rect = self.image.get_rect()
        self.rect.center = location


class Pheromone(enviro_element):
    """
    """
    def __init__(self, location):
        super().__init__()
        self.health = HEALTH

    def errode(self):
        self.health -= EVAPORATE_RATE
        if self.health <= 0:
            self.kill()


class FoodPheromone(Pheromone):
    """
    """
    def __init__(self, location):
        super().__init__()
        self.image = pygame.Surface(PHEROMONE_SIZE, pygame.SRCALPHA)
        self.radi = PHEROMONE_SIZE[1]/2
        pygame.draw.circle(self.image, ATTRACT, (self.radi, self.radi), self.radi)
        self.rect = self.surface.get_rect()
        self.rect.center = location
        self.health = HEALTH


class NoFoodPheromone(Pheromone):
    """
    """
    def __init__(self, location):
        super().__init__()
        self.sprite_surface = pygame.Surface(PHEROMONE_SIZE, pygame.SRCALPHA)
        self.radi = PHEROMONE_SIZE[1]/2
        pygame.draw.circle(self.image, REPEL, (self.radi, self.radi), self.radi)
        self.rect = self.surface.get_rect()
        self.rect.center = location
        self.health = HEALTH