import pygame
from classes.constants import *
import random

class PlanetManager:
    
    def __init__(self, player_x, player_y, initial_biome='forest'):
        
        biome_names = ['lava', 'ice', 'desert', 'fairy', 'mountain', 'mushroom', 'gemstones', 'river', 'flowerland']
        
        biome_list = []


        # Generate clusters of planets
        num = 2
        num_clusters = num**2
        width = 3000
        
        chunk_width = width // num
        
        for i in range(num):
            for j in range(num):
                
                if i == num // 2 and j == num // 2:
                    name = initial_biome
                name = random.choice(biome_names)
                
                x = chunk_width * i - width // 2 + player_x
                y = chunk_width * j - width // 2 + player_y
                
                new_biome = Biome(name)
                
                N = random.randint(2,4)
                planets = []
                attempts = 0
                max_attempts = 100
                while len(planets) < N and attempts < max_attempts:
                    radius = random.randint(150, 500)
                    new_x = random.randint(x, x + chunk_width - radius * 2)
                    new_y = random.randint(y, y + chunk_width - radius * 2)
                    collision = False
                    for planet in planets:
                        dist_x = planet.x - new_x
                        dist_y = planet.y - new_y
                        distance = (dist_x**2 + dist_y**2)**0.5
                        if distance < (planet.radius + radius):
                            collision = True
                            break
                    if not collision:
                        new_planet = new_biome.new_planet(new_x, new_y, radius)
                        planets.append(new_planet)
                        N -= 1
                        
                        print(x,y, radius)
                    attempts += 1
                biome_list.append((name, planets))
                
    def draw_planets(self, player_x, player_y, screen,  offset_x, offset_y):
        
        for planet in planet_group:
            dist_x = planet.x - player_x
            dist_y = planet.y - player_y
            distance = (dist_x**2 + dist_y**2)**0.5
            if distance < 2000:
                planet.draw(screen, offset_x, offset_y)

class Biome:
    
    def __init__(self, name):
        self.name = name
        self.planets = []
        
        self.color = random.choice([
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 255, 255) # White
        ])
    
    def new_planet(self,x ,y, r):
          
        print(x,y,r)
        planet = Planet(x, y, r, len(self.planets), self.color)
        
        self.planets.append(planet)
        
        planet_group.add(planet)
        
        return planet

class Planet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, radius, id, color):
        super().__init__()
        
        self.x = x 
        self.y = y
        self.radius = radius
        self.id = id
        self.color = color
        
        self.image = pygame.Surface((radius * 2, radius * 2))
        
    def draw(self,screen, offset_x, offset_y):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        screen.blit(self.image, (self.x - self.radius - offset_x, self.y - self.radius - offset_y))
        
