import pygame
from classes.constants import *

class Crafter(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()

        self.CRAFTING_WIDTH, self.CRAFTING_HEIGHT = 5*32, 5*32
        self.crafting_surface = pygame.Surface((self.CRAFTING_WIDTH, self.CRAFTING_HEIGHT))
        self.crafting_surface.fill(GRAY)
        
        self.crafting_rect = pygame.Rect(0, 0, self.CRAFTING_WIDTH, self.CRAFTING_HEIGHT)
        
        self.crafting_rect.x = (WIDTH - self.crafting_rect.width) // 2
        self.crafting_rect.y = (HEIGHT - self.crafting_rect.height) // 3
        self.crafting_surface.fill(GRAY)
        
        self.crafting_started = False
        
        self.image = pygame.Surface((32, 32))
        self.file = 'assets/gfx/wizard_full.png'
        self.tile_width = 32
        self.tileset = pygame.image.load(self.file)
        self.image.blit(self.tileset, (0, 0), (58 * 32, 0 * 32, 32, 32))
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.rect = self.image.get_rect()
        
        self.slot_size = (50, 50)  # Width and height of each slot
        
    def draw(self, surface, inventory):
        surface.blit(self.crafting_surface, (self.crafting_rect.x, self.crafting_rect.y))
        
        slot_x = self.crafting_rect.x + (self.CRAFTING_WIDTH - self.slot_size[0]) // 2
        slot_y = self.crafting_rect.y + (self.CRAFTING_HEIGHT - self.slot_size[1]) // 2  
        pygame.draw.rect(surface, BLACK, (slot_x, slot_y, self.slot_size[0], self.slot_size[1]), 2)
                
        self.crafting_button_rect = pygame.Rect(self.crafting_rect.x, self.crafting_rect.y + self.CRAFTING_HEIGHT + 10, self.CRAFTING_WIDTH, 50)
        pygame.draw.rect(surface, BLUE, self.crafting_button_rect) 
       
        font = pygame.font.Font(None, 28)
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
        biome = inventory.selected_item
        level = inventory.counts[biome]
        
        print(biome, level)
        
        hotbar.add_spell(biome, level)
        inventory.remove_shard(biome)
            

    