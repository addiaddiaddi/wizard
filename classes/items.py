import pygame
import random
from classes.constants import *
class Shard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((random.randint(0,255),random.randint(0,255), random.randint(0,255)))
        self.type = 'forest'
        
        self.file = 'assets/gfx/wizard_full.png'
        self.tile_width = 32
        self.tileset = pygame.image.load(self.file)
        
        
        