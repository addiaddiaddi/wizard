import pygame

from classes.constants import *
from classes.utilities import load_sprite

class Hotbar:
    def __init__(self):
        self.selected_slot = 0
        self.spell_types = [("electricity", 1)]
    
    def add_spell(self, biome, level):
        self.spell_types.append((biome, level))

    def select_slot(self, slot):
        if 0 <= slot < len(self.spell_types):
            self.selected_slot = slot

    def get_selected_spell(self):
        return self.spell_types[self.selected_slot]

    def draw(self, surface):
        for i, spell_data in enumerate(self.spell_types):
            color = GREEN if i == self.selected_slot else GRAY
            pygame.draw.rect(surface, color, (50 + i * 60, surface.get_height() - 300, 50, 50), 2, 8)
            surface.blit(pygame.transform.scale(
                load_sprite(f'assets/shards/shard_{spell_data[0]}.png'), (50, 50)
            ), (50 + i * 60, surface.get_height() - 300))