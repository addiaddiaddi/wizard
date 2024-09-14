import pygame

from classes.constants import *

from classes.items import Shard
class Inventory():
    
    def __init__(self):
        self.spells = pygame.sprite.Group()
        self.shards = pygame.sprite.Group()
        
        
        for i in range(5):
            self.shards.add(Shard())
        self.slots = 10  # Number of inventory slots
        self.slot_size = (50, 50)  # Width and height of each slot
        self.slot_margin = 10  # Margin between slots
        self.inventory_surface = pygame.Surface((self.slots * (self.slot_size[0] + self.slot_margin) - self.slot_margin, self.slot_size[1]))
        self.inventory_surface.fill(GRAY)  # Background color of the inventory bar

    def draw(self, surface):
        # Draw the inventory surface
        inventory_x = (WIDTH - self.inventory_surface.get_width()) // 2
        inventory_y = HEIGHT - self.slot_size[1] - 20  # 20 pixels from the bottom of the screen
        surface.blit(self.inventory_surface, (inventory_x, inventory_y))

        # Draw slots and items
        for i in range(self.slots):
            slot_x = inventory_x + i * (self.slot_size[0] + self.slot_margin)
            slot_y = inventory_y
            pygame.draw.rect(surface, BLACK, (slot_x, slot_y, self.slot_size[0], self.slot_size[1]), 2)  # Draw slot border

            # Check if there is an item in the slot and draw it
            if i < len(self.shards):  # Assuming shards are the items in the inventory
                item = self.shards.sprites()[i]
                item_image = pygame.transform.scale(item.image, self.slot_size)  # Scale item image to fit the slot
                surface.blit(item_image, (slot_x, slot_y))