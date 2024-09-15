import pygame
import random

from classes.wizard import Wizard
from classes.mob import MobFactory
from classes.spell import SpellFactory
from classes.hotbar import Hotbar
from classes.tiles import Tiles
from classes.utilities import get_camera_offset, draw_sprites, draw_healthbars
from classes.constants import *
from classes.inventory import Inventory
from classes.items import Shard
from classes.crafter import Crafter

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 32*32, 32*32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wizard")

wizard = Wizard(WIDTH, HEIGHT)

crafter = Crafter()
crafter_group.add(crafter)

crafter.rect.x = wizard.rect.x
crafter.rect.y = wizard.rect.y
all_sprites.add(crafter)

inventory = Inventory()
wizard_group.add(wizard)
all_sprites.add(wizard)

# Instantiate tiles
tiles = Tiles(WIDTH, HEIGHT)

# Instantiate hotbar
hotbar = Hotbar()

# Game loop
running = True
inventory_showing = False


while running:
    clock.tick(60)
    offset_x, offset_y = get_camera_offset(screen, wizard)
        
    keydown = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keydown = True
            # Check number keys (1-9) for hotbar selection
            if pygame.K_1 <= event.key <= pygame.K_9:
                hotbar.select_slot(event.key - pygame.K_1)

            # Fire a spell on spacebar press
            if event.key == pygame.K_SPACE:
                mouse_pos = pygame.mouse.get_pos()
                selected_spell = hotbar.get_selected_spell()
                SpellFactory.create_spell(selected_spell, wizard.rect.centerx, wizard.rect.centery, mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            crafter.select(inventory)
    
    crafting_collission = pygame.sprite.groupcollide(wizard_group, crafter_group, False, False)
    
    if crafting_collission != {}:
        active_crafter = crafting_collission[wizard][0]
        inventory_showing = True
    elif pygame.key.get_pressed()[pygame.K_e] and keydown:
        inventory_showing = not inventory_showing
    elif crafting_collission == {}:
        if active_crafter is not None:
            active_crafter = None
            inventory_showing = False

    # Spawn mobs randomly
    if random.randint(1, 100) < 3:
        mob = MobFactory.create_mob(random.choice(["fast", "strong", "normal"]))
        all_sprites.add(mob)
        mobs.add(mob)

    # Update game objects
    keys = pygame.key.get_pressed()
    wizard.update(keys)

    spells.update()
    mobs.update(wizard.rect.center)

    # Check for collisions between spells and mobs
    hits = pygame.sprite.groupcollide(mobs, spells, False, True)
    for mob in hits:
        mob.health -= 10
        if mob.health <= 0:
            
            shard = Shard()
            shard.rect = mob.rect
            
            all_sprites.add(shard)
            dropped_shards.add(shard)
            mob.kill()

    # Check for collisions between the wizard and mobs  
    mob_hits = pygame.sprite.groupcollide(wizard_group, mobs, False, True)
    for mob in mob_hits.get(wizard, []):
        wizard.health -= mob.power

    if wizard.health <= 0:
        print("GAME OVER")
        running = False


    pickups = pygame.sprite.groupcollide(wizard_group, dropped_shards, False, True)

    for shard in pickups.get(wizard,[]):
        inventory.add_shard(shard)
        
        
        
    # Draw everything
    screen.fill(BLACK)
    tiles.draw_tiles(screen, offset_x, offset_y)
    draw_sprites(all_sprites, screen, offset_x, offset_y)
    draw_healthbars(wizard, mobs, screen, offset_x, offset_y)

    # Draw hotbar
    hotbar.draw(screen)

    if inventory_showing:
        inventory.draw(screen)
        
    if active_crafter is not None:
        active_crafter.draw(screen, inventory)

    pygame.display.flip()

pygame.quit()
