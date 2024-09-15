import pygame
import math
import random

from classes.constants import *

class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_pos, speed=10, direction_offset=0, chain_explosion_types=None):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(random.choice([WHITE, RED, BLUE, GREEN, YELLOW, GRAY]))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        dx, dy = mouse_pos[0] - x , mouse_pos[1] - y 
        angle = math.atan2(dy, dx) + math.radians(direction_offset)
        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)

        # spell properties
        self.distance_traveled = 0
        self.explosion_threshold = 200
        self.chain_explosion_types = chain_explosion_types or []

    def update(self, hit=False):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.distance_traveled += self.speed

        if len(self.chain_explosion_types) > 0 and (self.distance_traveled >= self.explosion_threshold or hit):
            SpellFactory.create_spell(
                self.chain_explosion_types,
                self.rect.centerx, self.rect.centery,
                (self.rect.centerx + self.velocity_x, self.rect.centery + self.velocity_y)
            )
            
            self.kill()

        if self.distance_traveled >= 5000:
            self.kill()


class SpellFactory:
    @staticmethod
    def create_spell(spell_chain, x, y, mouse_pos):
        if spell_chain[0] == "normal":
            spell = Spell(x, y, mouse_pos, chain_explosion_types=spell_chain[1:])
            all_sprites.add(spell)
            spells.add(spell)
        
        elif spell_chain[0] == "cone":
            for angle in [-30, 0, 30]:
                random_noise = random.uniform(-10, 10)
                spell = Spell(
                    x, y, mouse_pos,
                    speed=10,
                    direction_offset=angle + random_noise,
                    chain_explosion_types=spell_chain[1:]
                )
                
                all_sprites.add(spell)
                spells.add(spell)
                
        elif spell_chain[0] == "circular":
            for angle in range(0, 360, 30):
                random_noise = random.uniform(-15, 15)
                spell = Spell(
                    x, y, mouse_pos,
                    speed=10,
                    direction_offset=angle + random_noise,
                    chain_explosion_types=spell_chain[1:]
                )
                
                all_sprites.add(spell)
                spells.add(spell)
                