# constants.py
import pygame

# Screen dimensions
WIDTH, HEIGHT = 32*32, 32*32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Game clock
clock = pygame.time.Clock()

# Create sprite groups
all_sprites = pygame.sprite.Group()
spells = pygame.sprite.Group()
mobs = pygame.sprite.Group()
wizard_group = pygame.sprite.Group()
dropped_shards = pygame.sprite.Group()
crafter_group =pygame.sprite.Group()
particles = pygame.sprite.Group()
planet_group = pygame.sprite.Group()
