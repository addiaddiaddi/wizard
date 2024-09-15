import pygame
from classes.constants import *

class Crafter(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()

        self.CRAFTING_WIDTH, self.CRAFTING_HEIGHT = 12*32, 8*32
        self.crafting_surface = pygame.Surface((self.CRAFTING_WIDTH, self.CRAFTING_HEIGHT))
        self.crafting_surface.fill(WHITE)
        self.crafting_surface.set_alpha(110)  # Set transparency level (0-255)
        
        self.crafting_rect = pygame.Rect(0, 0, self.CRAFTING_WIDTH, self.CRAFTING_HEIGHT)

        self.crafting_rect.x = (WIDTH - self.crafting_rect.width) // 2
        self.crafting_rect.y = (HEIGHT - self.crafting_rect.height) // 3
        self.crafting_surface.fill(WHITE)
        self.crafting_surface.set_alpha(110)  # Set transparency level (0-255)
        
        self.crafting_started = False
        
        self.image = pygame.Surface((512, 512))
        self.file = 'assets/misc/crafter.png'
        self.tile_width = 512
        self.tileset = pygame.image.load(self.file)
        self.image.blit(self.tileset, (0, 0), (0,0, 512, 512))
        self.image = pygame.transform.scale(self.image, (256, 256))
        self.rect = self.image.get_rect()
        
        self.slot_size = (100, 100)  # Width and height of each slot
        
    def draw(self, surface, inventory):
        surface.blit(self.crafting_surface, (self.crafting_rect.x, self.crafting_rect.y))
        
        slot_x = self.crafting_rect.x + (self.CRAFTING_WIDTH - self.slot_size[0]) // 2
        slot_y = self.crafting_rect.y + (self.CRAFTING_HEIGHT - self.slot_size[1]) // 2  
        pygame.draw.rect(surface, BLACK, (slot_x, slot_y, self.slot_size[0], self.slot_size[1]), 4, 8)
                
        self.crafting_button_rect = pygame.Rect(self.crafting_rect.x, self.crafting_rect.y + self.CRAFTING_HEIGHT + 10, self.CRAFTING_WIDTH, 50)
        pygame.draw.rect(surface, (177,52,235), self.crafting_button_rect, border_radius=8) 
       
        font = pygame.font.Font("assets/misc/pixelfont.otf", 28)
        text = font.render('Press C to Craft', True, WHITE)
        text_rect = text.get_rect(center=self.crafting_button_rect.center)
        surface.blit(text, text_rect)
        
        if inventory.selected_item is not None:
            item_image = pygame.transform.scale(
                pygame.image.load(f'assets/shards/shard_{inventory.selected_item}.png').convert_alpha(), 
                self.slot_size
            )
            surface.blit(item_image, (slot_x, slot_y))
            
    def craft(self, inventory, hotbar):
        if inventory.selected_item is None:
            return 
        
        biome = inventory.selected_item
        level = inventory.counts[biome]
        
        print(biome, level)
        
        hotbar.add_spell(biome, level)
        inventory.remove_shard(biome)
            

    