import pygame
from classes.constants import *

class Wizard(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load('assets/gfx/wizard.png').convert_alpha()

        # Sprite dimensions (you can adjust the width and height based on your sprite size)
        self.sprite_width = 64  # Adjust based on your sprite size in the sheet
        self.sprite_height = 64

        # Extract animation frames (first four rows correspond to up, left, down, right)
        self.animations = {
            'up': self.get_frames(0),
            'left': self.get_frames(1),
            'down': self.get_frames(2),
            'right': self.get_frames(3),
            'attack-up': self.get_frames(47, attack=True),
            'attack-left': self.get_frames(50, attack=True),
            'attack-down': self.get_frames(53, attack=True),
            'attack-right': self.get_frames(56, attack=True),
        }
        
        self.current_direction = 'down'
        self.frame_index = 0
        self.image = self.animations[self.current_direction][self.frame_index]
        
        self.rect = self.image.get_rect()        
        self.rect.center = (width // 2, height // 2)
        self.rect.size = (50, 50)
        
        self.speed = 5
        self.max_health = 100
        self.health = self.max_health
        
        self.animation_speed = 0.25  # Adjust this for slower/faster animation
        self.frame_counter = 0
        
        self.is_attacking = False
        self.attack_speed = 0.25  # Attack animation speed
        self.attack_frame_index = 0

    def get_frames(self, row, attack=False):
        """Extracts frames from a specific row."""
        frames = []
        for i in (range(1, 23, 3) if attack else range(7)):  # Adjust 9 based on the number of frames per row
            frame = self.sprite_sheet.subsurface(
                pygame.Rect(
                    i * self.sprite_width,
                    row * self.sprite_height,
                    self.sprite_width + 10,
                    self.sprite_height + 10
                )
            )
            
            scaled_frame = pygame.transform.scale(frame, ((128, 128) if attack else (128, 128)))
            frames.append(scaled_frame)
        return frames

    def attack(self):
        """Initiate the attack animation."""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_frame_index = 0  # Start attack animation from the first frame

    def update(self, keys):
        is_moving = False  # Flag to track if the character is moving

        if self.is_attacking:
            # Handle attack animation
            self.frame_counter += self.attack_speed
            if self.frame_counter >= 1:
                self.frame_counter = 0
                self.attack_frame_index += 1

                # Get the appropriate attack animation for the direction
                attack_animation_key = f"attack-{self.current_direction}"
                if self.attack_frame_index >= len(self.animations[attack_animation_key]):
                    # End attack animation
                    self.is_attacking = False
                    self.attack_frame_index = 0
                else:
                    # Set the attack frame
                    self.image = self.animations[attack_animation_key][self.attack_frame_index]

            return  # Skip movement updates during attack

        # Movement controls
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.current_direction = 'left'
            is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.current_direction = 'right'
            is_moving = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.current_direction = 'up'
            is_moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            self.current_direction = 'down'
            is_moving = True

        # Handle animation only if moving
        if is_moving:
            self.frame_counter += self.animation_speed
            if self.frame_counter >= 1:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_direction])
                self.image = self.animations[self.current_direction][self.frame_index]
                # Update rect to match the new image size
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            # Reset to the first frame if not moving
            self.frame_index = 0
            self.image = self.animations[self.current_direction][self.frame_index]

        # Attack logic
        if keys[pygame.K_SPACE]:
            self.attack()
