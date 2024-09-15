import pygame
import random

from classes.constants import *

class Shard(pygame.sprite.Sprite):
    def __init__(self, biome, x, y):
        super().__init__()
        
        self.biome = biome
        self.image = pygame.transform.scale(pygame.image.load(f'assets/shards/shard_{self.biome}.png').convert_alpha(), (80, 80))
        
        self.rect = self.image.get_rect(center=(x, y))
        
        
    def draw(self, screen, coord_x, coord_y):
        screen.blit(self.image, (coord_x, coord_y))
        
        
        