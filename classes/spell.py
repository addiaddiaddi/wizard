import pygame
import math
import random

from classes.constants import *
from .particle import Particle

class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_pos, biome="electricity", power_level=1, speed=10, direction_offset=0, chain_explosion_types=None):
        super().__init__()
        
        # Load spell images (assuming they are named sprite_1.png, sprite_2.png, sprite_3.png)
        self.sprites = [
            pygame.transform.scale(pygame.image.load(f'assets/spells/spell_{0}_{biome}.png').convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load(f'assets/spells/spell_{1}_{biome}.png').convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load(f'assets/spells/spell_{2}_{biome}.png').convert_alpha(), (100, 100)),
        ]
        
        self.explosion_sprite = pygame.transform.scale(
            pygame.image.load(f'assets/spells/spell_explosion_{biome}.png'
        ).convert_alpha(), (120, 120))
        
        self.explosion_sprite = pygame.transform.rotate(
            self.explosion_sprite, random.randint(30, 300)
        )
        
        # Set the initial image and rect
        self.current_sprite_index = 0
        self.image = self.sprites[self.current_sprite_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.rect.size = (40, 40)
        
        self.animation_speed = 12  # Controls how fast the animation cycles through frames
        self.animation_counter = 0  # Keeps track of frames to control the animation speed
        
        # Spell movement
        self.speed = speed
        dx, dy = mouse_pos[0] - x , mouse_pos[1] - y 
        angle = math.atan2(dy, dx) + math.radians(direction_offset)
        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)

        # Spell properties
        self.distance_traveled = 0
        self.explosion_threshold = 200
        self.chain_explosion_types = chain_explosion_types or []
        
        self.explosion_time = 110  # Duration for the explosion (in milliseconds)
        self.exploding = False  # Whether the spell is in the explosion state
        self.explosion_start_time = None  # The time when the explosion started

    def update(self, hit=False):
        if self.exploding:
            # Check if the explosion time has passed
            current_time = pygame.time.get_ticks()
            if current_time - self.explosion_start_time >= self.explosion_time:
                self.kill()  # Remove the spell after the explosion sprite has been shown for 1 second
            return  # Skip the normal update when exploding
        
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.distance_traveled += self.speed

        # Check for chain explosion
        if len(self.chain_explosion_types) > 0 and (self.distance_traveled >= self.explosion_threshold or hit):
            SpellFactory.create_spell(
                self.chain_explosion_types,
                self.rect.centerx, self.rect.centery,
                (self.rect.centerx + self.velocity_x, self.rect.centery + self.velocity_y)
            )
            
            self.explode()
            return
        
        if hit:
            self.explode()
            return

        # Kill the spell after it travels a certain distance
        if self.distance_traveled >= 5000:
            self.kill()
            return

        # Animate the spell
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite_index]  # Update to the next sprite image
    
    def explode(self):
        """Trigger the explosion by switching to the explosion sprite and starting the timer."""
        self.rect.x += self.velocity_x * 10
        self.rect.y += self.velocity_y * 10
        
        self.exploding = True
        self.image = self.explosion_sprite  # Set the explosion sprite as the current image
        self.explosion_start_time = pygame.time.get_ticks()  # Record the start time of the explosion
        
        for _ in range(8):  # Adjust the number of particles as desired
            particle = Particle(self.rect.centerx, self.rect.centery)
            particles.add(particle)
            all_sprites.add(particle)

        self.rect.size = (0, 0)  # Make the hitbox size 0, so it won't collide with enemies


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
            for angle in range(0, 360, 60):
                random_noise = random.uniform(-15, 15)
                spell = Spell(
                    x, y, mouse_pos,
                    speed=10,
                    direction_offset=angle + random_noise,
                    chain_explosion_types=spell_chain[1:]
                )
                
                all_sprites.add(spell)
                spells.add(spell)