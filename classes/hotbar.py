import pygame

from classes.constants import *

class Hotbar:
    def __init__(self):
        self.selected_slot = 0
        self.spell_types = ["normal", "explosive", "fast", "slow", "circular"]

    def select_slot(self, slot):
        if 0 <= slot < len(self.spell_types):
            self.selected_slot = slot

    def get_selected_spell(self):
        return self.spell_types[self.selected_slot]

    def draw(self, surface):
        for i, spell_type in enumerate(self.spell_types):
            color = YELLOW if i == self.selected_slot else GRAY
            pygame.draw.rect(surface, color, (50 + i * 60, surface.get_height() - 60, 50, 50))
            font = pygame.font.Font(None, 36)
            text = font.render(f"{i+1}", True, WHITE)
            surface.blit(text, (65 + i * 60, surface.get_height() - 55))