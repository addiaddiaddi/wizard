import pygame
import math

from classes.constants import *

class Wizard(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load('assets/gfx/wizard.png').convert_alpha()
        self.attack_sheet = pygame.image.load('assets/gfx/wizard_attack.png').convert_alpha()

        # Extract animation frames (first four rows correspond to up, left, down, right)
        self.animations = {
            'up': self.get_frames(0),
            'left': self.get_frames(1),
            'down': self.get_frames(2),
            'right': self.get_frames(3),
            'attack-up': self.get_attack_frames(0),
            'attack-left': self.get_attack_frames(1),
            'attack-down': self.get_attack_frames(2),
            'attack-right': self.get_attack_frames(3),
        }
        
        self.current_direction = 'down'
        self.frame_index = 0
        self.image = self.animations[self.current_direction][self.frame_index]
        
        self.rect = pygame.Rect(0, 0, 64, 64)        
        self.rect.center = (width // 2, height // 2)
        
        self.speed = 5
        self.max_health = 100
        self.health = self.max_health
        
        self.animation_speed = 0.25  # Adjust this for slower/faster animation
        self.frame_counter = 0
        
        self.is_attacking = False
        self.attack_speed = 0.25  # Attack animation speed
        self.attack_frame_index = 0

    def get_frames(self, row):
        """Extracts frames from a specific row."""
        frames = []
        for i in range(7):  # Adjust 9 based on the number of frames per row
            frame = self.sprite_sheet.subsurface(
                pygame.Rect(
                    i * 64,
                    row * 64,
                    64,
                    64
                )
            )
            
            scaled_frame = pygame.transform.scale(frame, (128, 128))
            frames.append(scaled_frame)
        return frames
    
    def get_attack_frames(self, row):
        frames = []
        for i in range(8):  # Adjust 9 based on the number of frames per row
            frame = self.attack_sheet.subsurface(
                pygame.Rect(
                    i * 192,
                    row * 192,
                    192,
                    192
                )
            )
            
            scaled_frame = pygame.transform.scale(frame, (128 * 3, 128 * 3))
            frames.append(scaled_frame)
        return frames
    
    def get_mouse_direction(self, mouse_pos):
        """Determine the direction to face based on the mouse position."""
        # Calculate the angle to the mouse position
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        angle = math.atan2(dy, dx)  # Get the angle to the mouse
        
        # Determine the closest direction based on the angle
        if -math.pi / 4 <= angle < math.pi / 4:
            return 'right'
        elif math.pi / 4 <= angle < 3 * math.pi / 4:
            return 'down'
        elif -3 * math.pi / 4 <= angle < -math.pi / 4:
            return 'up'
        else:
            return 'left'

    def attack(self, mouse_pos):
        """Initiate the attack animation and face the direction of the mouse."""
        if not self.is_attacking:
            # Update the direction based on the mouse position
            self.current_direction = self.get_mouse_direction(mouse_pos)
            self.is_attacking = True
            self.attack_frame_index = 0  # Start attack animation from the first frame

    def update(self, keys, mouse_pos):
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
                    
                    self.image = self.animations[self.current_direction][0]
                else:
                    # Set the attack frame
                    self.image = self.animations[attack_animation_key][self.attack_frame_index]


        # Movement controls
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.current_direction = 'left'
            is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.current_direction = 'right'
            is_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.current_direction = 'up'
            is_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            self.current_direction = 'down'
            is_moving = True

        # Handle animation only if moving
        if not self.is_attacking:
            if is_moving:
                self.frame_counter += self.animation_speed
                if self.frame_counter >= 1:
                    self.frame_counter = 0
                    self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_direction])
                    self.image = self.animations[self.current_direction][self.frame_index]
            else:
                self.frame_index = 0
                self.image = self.animations[self.current_direction][self.frame_index]

        # Attack logic
        if keys[pygame.K_SPACE]:
            self.attack(mouse_pos)
    
    def draw(self, screen, off_x, off_y):
        """Draw the sprite, centering attack animations properly."""
        if self.is_attacking:
            offset_x = (self.image.get_width() - self.rect.width) // 2 - 35
            offset_y = (self.image.get_height() - self.rect.height) // 2 - 35
            # Draw the image centered over the rect
            screen.blit(self.image, (self.rect.x - offset_x - off_x, self.rect.y - offset_y - off_y))
        else:
            # For normal movement, just draw it normally
            screen.blit(self.image, (self.rect.x - off_x, self.rect.y - off_y))
