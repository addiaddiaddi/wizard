import pygame
import random
import math

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Initial size of the particle
        self.initial_size = 10
        self.current_size = self.initial_size

        # Create the particle image with the initial size
        self.image = pygame.Surface((self.initial_size, self.initial_size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (120,6,6), (self.initial_size // 2, self.initial_size // 2), self.initial_size // 2)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Random angle and speed for the particle
        random_angle = random.uniform(0, 2 * math.pi)  # Random angle in radians (0 to 360 degrees)
        speed = random.uniform(6, 8)  # Random speed for the particle

        # Calculate velocity components based on the angle and speed
        self.velocity_x = speed * math.cos(random_angle)
        self.velocity_y = speed * math.sin(random_angle)

        self.lifetime = 1000  # Lifetime in milliseconds
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        # Move the particle
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Calculate the percentage of lifetime passed
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.spawn_time
        lifetime_percentage = elapsed_time / self.lifetime

        # Shrink the particle based on its lifetime
        if lifetime_percentage < 1:
            self.current_size = max(self.initial_size * (1 - lifetime_percentage), 0)  # Shrink size
            self.image = pygame.Surface((self.current_size, self.current_size), pygame.SRCALPHA)  # Update the surface size
            pygame.draw.circle(self.image, (120,6,6), (self.current_size // 2, self.current_size // 2), self.current_size // 2)
            self.rect = self.image.get_rect(center=self.rect.center)  # Update the rect to match the new size