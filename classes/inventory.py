import pygame

from classes.constants import *
import random
from classes.items import Shard
class Inventory():
    
    def __init__(self):
        self.spells = pygame.sprite.Group()
        self.shards = pygame.sprite.Group()
        
        self.counts = {}
        for i in range(5):
            shard = Shard()
            self.shards.add(shard)
            self.counts[shard] = random.randint(0,25)
            
        self.slots = (10,3)  # Number of inventory slots
        self.slot_size = (50, 50)  # Width and height of each slot
        self.slot_margin = 10  # Margin between slots
        self.inventory_surface = pygame.Surface((self.slots[0] * (self.slot_size[0] + self.slot_margin) - self.slot_margin, 
                                                 self.slots[1] * (self.slot_size[1] + self.slot_margin) - self.slot_margin))
        self.inventory_surface.fill(GRAY)  # Background color of the inventory bar

    def draw(self, surface):
        # Draw the inventory surface
        inventory_x = (WIDTH - self.inventory_surface.get_width()) // 2
        inventory_y = HEIGHT - self.slot_size[1] - 300  # 20 pixels from the bottom of the screen
        surface.blit(self.inventory_surface, (inventory_x, inventory_y))

        # Draw slots and items
        for i in range(self.slots[0]):
            for j in range(self.slots[1]):
                
                slot_x = inventory_x + i * (self.slot_size[0] + self.slot_margin)
                slot_y = inventory_y + j * (self.slot_size[1] + self.slot_margin)
                pygame.draw.rect(surface, BLACK, (slot_x, slot_y, self.slot_size[0], self.slot_size[1]), 2)  # Draw slot border

                # Check if there is an item in the slot and draw it
                item_idx = j*self.slots[0] + i
                if item_idx < len(self.shards):  # Assuming shards are the items in the inventory
                    item = self.shards.sprites()[item_idx]
                    
                    item_image = pygame.transform.scale(item.image, self.slot_size )  # Scale item image to fit the slot
                    surface.blit(item_image, (slot_x, slot_y))
                    
                    font = pygame.font.Font(None, 24)  # Load a font object
                    count_text = font.render(str(self.counts[item]), True, WHITE)  # Render the count text
                    text_x = slot_x + self.slot_size[0] / 10  # Center text horizontally in the slot
                    text_y = slot_y + self.slot_size[1] - count_text.get_height()  # Position text at the bottom of the slot
                    surface.blit(count_text, (text_x, text_y))  # Draw the text on the surface

    def add_shard(self, shard):
        
        self.shards.add(shard)
        
        self.counts[shard] = self.counts.get(shard, 0) + 1