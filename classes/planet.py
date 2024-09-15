import pygame
from classes.constants import *
import random
from classes.mob import *
import math

biome_names = [
    "apocalypse",
    "death",
    "desert",
    "fire",
    "ice",
    "magical",
    "techno-organic",
    "temporal-rift",
]

class PlanetManager:

    def __init__(self, player_x, player_y, crafter_x, crafter_y, initial_biome="cyberpunk"):
        self.biome_list = []

        # Generate clusters of planets
        num = 25
        width = 30000

        chunk_width = width // num


        print('starting world gen')
        for i in range(num):
            for j in range(num):

                if i == num // 2 and j == num // 2:
                    biome = initial_biome
                else:
                    biome = random.choice(biome_names)

                x = chunk_width * i - width // 2 + player_x
                y = chunk_width * j - width // 2 + player_y

                new_biome = Biome(biome)
                self.biome_list.append(new_biome)
                
                N = random.randint(2, 3)
                # N = 1
                
                planets = []
                attempts = 0
                max_attempts = 10
                
                while len(planets) < N and attempts < max_attempts:
                    radius = random.randint(150, 500)
                    new_x = random.randint(x, x + chunk_width - radius * 2)
                    new_y = random.randint(y, y + chunk_width - radius * 2)
                    collision = False
                    for planet in planets:
                        dist_x = planet.x - new_x
                        dist_y = planet.y - new_y
                        distance = (dist_x**2 + dist_y**2) ** 0.5
                        if distance < (planet.radius + radius):
                            collision = True
                            break

                        dist_x = planet.x - player_x
                        dist_y = planet.y - player_y
                        distance = (dist_x**2 + dist_y**2) ** 0.5
                        if distance < (planet.radius + radius + 25):
                            collision = True
                            break
                        
                        dist_x = planet.x - crafter_x
                        dist_y = planet.y - crafter_y
                        distance = (dist_x**2 + dist_y**2) ** 0.5
                        if distance < (planet.radius + 128):
                            collision = True
                            break

                    if not collision:
                        new_planet = new_biome.new_planet(new_x, new_y, radius)
                        planets.append(new_planet)
                        N -= 1

                        # print(x, y, radius)
                    attempts += 1

        print('stopping world gen')

    def draw_planets(self, player_x, player_y, screen, offset_x, offset_y):
        for planet in planet_group:
            dist_x = planet.x - player_x
            dist_y = planet.y - player_y
            distance = (dist_x**2 + dist_y**2) ** 0.5
            if distance < 1500:
                planet.draw(screen, offset_x, offset_y)

    def mob_gen(self, player_x, player_y):

        for planet in planet_group:
            dist_x = planet.x - player_x
            dist_y = planet.y - player_y
            distance = (dist_x**2 + dist_y**2) ** 0.5
            if distance < 100 or distance > 800:
                continue
            # Probability of mob spawning inversely proportional to the planet's radius
            spawn_probability = (
                planet.radius / 50000
            )  # Adjust the divisor to scale difficulty
            if random.random() < spawn_probability:
                # Assuming a function create_mob() exists that creates and returns a mob object

                angle = random.uniform(0, 2 * math.pi)
                spawn_x = int(planet.x + planet.radius * math.cos(angle))
                spawn_y = int(planet.y + planet.radius * math.sin(angle))
                mob = MobFactory.create_mob(
                    random.choice(["fast", "strong", "normal"]), 
                    planet.biome,
                    planet.id,
                    x=spawn_x, y=spawn_y
                )
                all_sprites.add(mob)
                mobs.add(mob)

                # print(
                #     f"Mob spawned at ({planet.x}, {planet.y}) on planet with radius {planet.radius}"
                # )


class Biome:

    def __init__(self, biome):
        self.biome = biome
        self.planets = []

    def new_planet(self, x, y, r):
        # planet = Planet(x, y, r, f"testing123", self.biome)
        planet = Planet(x, y, r, len(self.planets), self.biome)

        self.planets.append(planet)
        planet_group.add(planet)

        return planet


class Planet(pygame.sprite.Sprite):

    def __init__(self, x, y, radius, id, biome):
        super().__init__()

        self.x = x
        self.y = y
        self.radius = radius
        
        self.id = id
        self.biome = biome

        self.image = pygame.transform.scale(
            pygame.image.load(f"assets/planets/planet_{biome}_{id}.png").convert_alpha(),
            (radius*2, radius*2),
        )
        

    def draw(self, screen, offset_x, offset_y):
        screen.blit(
            self.image,
            (self.x - self.radius - offset_x, self.y - self.radius - offset_y),
        )
