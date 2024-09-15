import pygame

from classes.constants import *

class Inventory():
    
    def __init__(self):
        self.spells = pygame.sprite.Group()
        self.shards = pygame.sprite.Group()
        
        self.counts = {}
            
        self.slots = (10,3)  # Number of inventory slots
        self.slot_size = (50, 50)  # Width and height of each slot
        self.slot_margin = 10  # Margin between slots
        self.inventory_surface = pygame.Surface((self.slots[0] * (self.slot_size[0] + self.slot_margin) - self.slot_margin, 
                                                 self.slots[1] * (self.slot_size[1] + self.slot_margin) - self.slot_margin))
        self.inventory_surface.fill(GRAY)  # Background color of the inventory bar
        self.selected_item = None  # Track the selected item
        
        self.inventory_array = []

    def handle_click(self, pos):
        inventory_x = (WIDTH - self.inventory_surface.get_width()) // 2
        inventory_y = HEIGHT - self.slot_size[1] - 300
        self.selected_item = None
        
        for i in range(self.slots[0]):
            for j in range(self.slots[1]):
                slot_x = inventory_x + i * (self.slot_size[0] + self.slot_margin)
                slot_y = inventory_y + j * (self.slot_size[1] + self.slot_margin)
                slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size[0], self.slot_size[1])
                
                if slot_rect.collidepoint(pos):
                    item_idx = j * self.slots[0] + i
                    if item_idx < len(self.inventory_array):
                        self.selected_item = self.inventory_array[item_idx]
                        return

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
                if item_idx >= len(self.inventory_array):
                    continue
                
                item_biome = self.inventory_array[item_idx]
                item_image = pygame.transform.scale(
                    pygame.image.load(f'assets/shards/shard_{item_biome}.png').convert_alpha(), 
                    self.slot_size
                )  # Scale item image to fit the slot
                
                surface.blit(item_image, (slot_x, slot_y))
                
                font = pygame.font.Font(None, 24)  # Load a font object
                count_text = font.render(str(self.counts[item_biome]), True, WHITE)  # Render the count text
                text_x = slot_x + self.slot_size[0] / 10  # Center text horizontally in the slot
                text_y = slot_y + self.slot_size[1] - count_text.get_height()  # Position text at the bottom of the slot
                surface.blit(count_text, (text_x, text_y))  # Draw the text on the surface
                
                if item_biome == self.selected_item:
                    pygame.draw.rect(surface, RED, (slot_x, slot_y, self.slot_size[0], self.slot_size[1]), 4)
    
    def add_shard(self, shard):
        if len(self.inventory_array) >= 30:
            return
        
        if shard.biome not in self.inventory_array:
            self.inventory_array.append(shard.biome)
        
        if self.counts.get(shard.biome) is None:
            self.counts[shard.biome] = 1
        else:
            self.counts[shard.biome] += 1
        
        shard.kill()
        
    def remove_shard(self, biome):
        self.inventory_array.pop(
            self.inventory_array.index(biome)
        )
        
        del self.counts[biome]