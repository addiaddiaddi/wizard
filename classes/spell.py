import pygame
import math
import random

from classes.constants import *

WHITE = (255, 255, 255)

class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_pos, speed=10, direction_offset=0, is_explosive=False, explosion_type="cone", chain_explosion_types=None):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        dx, dy = mouse_pos[0] - x, mouse_pos[1] - y
        angle = math.atan2(dy, dx) + math.radians(direction_offset)
        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)

        # Explosion properties
        self.is_explosive = is_explosive
        self.distance_traveled = 0
        self.explosion_threshold = 300
        self.explosion_type = explosion_type
        self.chain_explosion_types = chain_explosion_types or []

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.distance_traveled += self.speed

        if self.is_explosive and self.distance_traveled >= self.explosion_threshold:
            self.explode()

        if self.rect.x > 1024 or self.rect.x < 0 or self.rect.y > 1024 or self.rect.y < 0:
            self.kill()

    def explode(self):
        if self.explosion_type == "cone":
            for angle in [-30, 0, 30]:
                random_noise = random.uniform(-10, 10)
                new_spell = Spell(self.rect.centerx, self.rect.centery, (self.rect.centerx + self.velocity_x, self.rect.centery + self.velocity_y),
                                  direction_offset=angle + random_noise, is_explosive=True,
                                  explosion_type=self.chain_explosion_types[0] if self.chain_explosion_types else None,
                                  chain_explosion_types=self.chain_explosion_types[1:] if self.chain_explosion_types else [])
                all_sprites.add(new_spell)
                spells.add(new_spell)
        elif self.explosion_type == "circular":
            for angle in range(0, 360, 30):
                random_noise = random.uniform(-15, 15)
                rad_angle = math.radians(angle + random_noise)
                new_velocity_x = self.speed * math.cos(rad_angle)
                new_velocity_y = self.speed * math.sin(rad_angle)
                new_spell = Spell(self.rect.centerx, self.rect.centery, (self.rect.centerx + new_velocity_x, self.rect.centery + new_velocity_y),
                                  direction_offset=0, is_explosive=True,
                                  explosion_type=self.chain_explosion_types[0] if self.chain_explosion_types else None,
                                  chain_explosion_types=self.chain_explosion_types[1:] if self.chain_explosion_types else [])
                all_sprites.add(new_spell)
                spells.add(new_spell)
        self.kill()


class SpellFactory:
    @staticmethod
    def create_spell(spell_type, x, y, mouse_pos):
        if spell_type == "explosive":
            return Spell(x, y, mouse_pos, is_explosive=True, explosion_type="cone", chain_explosion_types=["circular", "cone", "circular"])
        elif spell_type == "circular":
            return Spell(x, y, mouse_pos, is_explosive=True, explosion_type="circular", chain_explosion_types=["cone", "circular"])
        elif spell_type == "fast":
            return Spell(x, y, mouse_pos, speed=20)
        elif spell_type == "slow":
            return Spell(x, y, mouse_pos, speed=5)
        else:
            return Spell(x, y, mouse_pos)