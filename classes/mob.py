import pygame
import random

from classes.constants import *

class Mob(pygame.sprite.Sprite):
    def __init__(self, health, speed, color, width, height):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(width + 20, width + 100)
        self.rect.y = random.randint(0, height)
        self.speed = speed
        self.max_health = health
        self.health = self.max_health
        self.power = 20

    def update(self, destination):
        player_x, player_y = destination
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        distance = max(1, (dx**2 + dy**2)**0.5)
        self.rect.x += self.speed * dx / distance
        self.rect.y += self.speed * dy / distance


class MobFactory:
    @staticmethod
    def create_mob(mob_type):
        if mob_type == "fast":
            return Mob(health=10, speed=5, color=RED, width=20, height=10)
        elif mob_type == "strong":
            return Mob(health=40, speed=2, color=RED, width=20, height=10)
        else:
            return Mob(health=20, speed=3, color=RED, width=20, height=10)