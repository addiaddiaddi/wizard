import pygame
import random
from classes.constants import *
class Shard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((random.randint(0,255),random.randint(0,255), random.randint(0,255)))
        self.type = 'forest'
        self.file = 'assets/gfx/wizard_full.png'
        self.tile_width = 32
        self.tileset = pygame.image.load(self.file)
        self.name = "Retard Shard"
        self.image.blit(self.tileset, (0, 0), (random.randint(0,15) * 32, 42 * 32, 32, 32))
        self.rect = self.image.get_rect()
        
        
    def draw(self, screen, coord_x, coord_y):
        screen.blit(self.image, (coord_x, coord_y))
        
        
        