import pygame
import random
import subprocess
import sys

from classes.wizard import Wizard
from classes.mob import MobFactory
from classes.spell import SpellFactory
from classes.hotbar import Hotbar
from classes.tiles import Tiles
from classes.utilities import *
from classes.constants import *
from classes.inventory import Inventory
from classes.items import Shard
from classes.crafter import Crafter
from classes.planet import * 


def draw_stars(screen, num_stars=100):
    """Draw randomly placed stars for the background."""
    for _ in range(num_stars):
        star_color = (255, 255, 255)  # White stars
        star_pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        pygame.draw.circle(screen, star_color, star_pos, 2)  # Small star size

def home_screen():
    # Load title font, button font, and input font
    title_font = pygame.font.Font(None, 120)  # Sci-fi themed font or default pygame font
    button_font = pygame.font.Font(None, 50)
    input_font = pygame.font.Font(None, 40)  # Font for text input
    label_font = pygame.font.Font(None, 40)  # Font for the label

    # Create text surfaces
    # title_text = title_font.render("Wizard Game", True, (255, 255, 255))  # White text for space theme
    logo_image = pygame.image.load("assets/misc/logo.png").convert_alpha()
    start_original = pygame.image.load("assets/misc/start.png").convert_alpha()
    theme_original = pygame.image.load("assets/misc/theme.png").convert_alpha()
    
    start_width = start_original.get_width() // 3
    start_height = start_original.get_height() // 3
    theme_width = theme_original.get_width() // 3
    theme_height = theme_original.get_height() // 3
    
    start_image = pygame.transform.scale(start_original, (start_width, start_height))
    theme_image = pygame.transform.scale(theme_original, (theme_width, theme_height))
    
   
    # # Define button rectangles
    start_button = start_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    # exit_button = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    # # Text input box setup
    input_box_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 150, 300, 50)  # Input box rectangle
    input_text = ''  # Text the player types
    input_active = False  # Whether the input box is active (clicked)
    
    # Label for the text box
    label_text = label_font.render("Enter Biome Type:", True, (255, 255, 255))

    # Colors
    box_color_inactive = pygame.Color('lightskyblue3')
    box_color_active = pygame.Color('dodgerblue2')
    box_color = box_color_inactive

    # Load or generate a space background
    background_image = pygame.transform.scale(
        pygame.image.load("background.png").convert(), (1024, 1024)
    )  # Replace with your space image
    
    # Home screen loop
    biome_type = None  # Variable to store the biome type
    while True:
        # Draw the space background
        screen.blit(background_image, (0, 0))
        
        # Optionally, draw stars dynamically
        draw_stars(screen, num_stars=150)
        
        # Draw title and buttons
        # screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        
        screen.blit(logo_image, (WIDTH // 2 - logo_image.get_width() // 2, 100))
        screen.blit(start_image, start_button)
        # screen.blit(exit_text, exit_button)
        
        # Draw the label for the text box
        screen.blit(theme_image, (input_box_rect.x, input_box_rect.y - 40))
        
        # Draw the text input box
        pygame.draw.rect(screen, box_color, input_box_rect, 2)
        
        # Render the current input text
        input_surface = input_font.render(input_text, True, (255, 255, 255))
        screen.blit(input_surface, (input_box_rect.x + 10, input_box_rect.y + 10))
        
        pygame.display.flip()  # Update the display
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicks inside the input box, activate it
                if input_box_rect.collidepoint(event.pos):
                    input_active = not input_active
                else:
                    input_active = False
                # Change the color of the input box based on whether it's active
                box_color = box_color_active if input_active else box_color_inactive
                
                # Check for button clicks
                if start_button.collidepoint(event.pos):
                    biome_type = input_text  # Save the typed biome type
                    print(f"Starting game with biome type: {biome_type}")  # Print the biome type
                    return biome_type  # Return the biome type for use in the game

            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        biome_type = input_text  # Save the typed biome type when pressing Enter
                        print(f"Entered biome type: {biome_type}")
                        input_text = ''  # Clear the input after pressing enter (optional)
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]  # Remove the last character
                    else:
                        input_text += event.unicode  # Add the typed character to 

        

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 32*32, 32*32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wizard")

user_biome = home_screen()

lore = generate_lore(user_biome)
# Load the Star Wars font
font_path = "assets/misc/pixelfont.otf"  # Path to the Star Wars font file
font_size = 60  # Set the font size
font = pygame.font.Font(font_path, font_size)

score_font = pygame.font.Font(font_path, font_size)

def draw_star_wars_text(screen, text, font, color, speed=2):
    lines = text.split('\n')


    # Further split lines to limit each line to a certain number of characters without cutting words in half
    max_chars_per_line = 40  # Set the maximum number of characters per line
    split_lines = []
    for line in lines:
        while len(line) > max_chars_per_line:
            split_point = line.rfind(' ', 0, max_chars_per_line)
            if split_point == -1:
                split_point = max_chars_per_line
            split_lines.append(line[:split_point])
            line = line[split_point:].lstrip()
        split_lines.append(line)
    lines = split_lines


    max_width, max_height = screen.get_size()
    text_height = len(lines) * font.get_height()
    y = max_height
    while y + text_height > 0:
        screen.fill((0, 0, 0))  # Clear the screen with black

        padding = 20  # Define the padding value
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(max_width // 2, y + i * font.get_height()))
            text_rect.x += padding  # Add padding to the left side
            text_rect.width -= 2 * padding  # Adjust the width to account for padding on both sides
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        y -= speed
        pygame.time.wait(1)

# Define the Star Wars text
instructions = f"\n--------------\n Directive:\nYour mission is to explore the generated universe, kill many monsters, and discover spells. \nYou will spawn into the {user_biome} region of the galaxy where you will be greeted by {user_biome}-ish mobs. \nRegion-specific mobs will drop shards for that region, which can be crafted into unique spells at crafting planets."
lore += instructions
draw_star_wars_text(screen, lore, font, WHITE)
wizard = Wizard(WIDTH + 32 * 32, HEIGHT + 32 * 32)

crafter = Crafter()
crafter_group.add(crafter)

crafter.rect.x = wizard.rect.x
crafter.rect.y = wizard.rect.y
all_sprites.add(crafter)

inventory = Inventory()
wizard_group.add(wizard)

# Instantiate tiles
tiles = Tiles(3*WIDTH, 3*HEIGHT)

# Instantiate hotbar
hotbar = Hotbar()

spell_cooldown = 500  # Cooldown time in milliseconds (0.5 seconds)
last_spell_time = pygame.time.get_ticks()  # Initialize with the current time

# Game loop
running = True
inventory_showing = False

planet_manager = PlanetManager(wizard.rect.x, wizard.rect.y)

score = 0


while running:
    game_started = True
    
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
                current_time = pygame.time.get_ticks()  # Get the current time
                if current_time - last_spell_time >= spell_cooldown:
                    mouse_pos = pygame.mouse.get_pos()
                    selected_spell = hotbar.get_selected_spell()
                    SpellFactory.create_spell(selected_spell, wizard.rect.centerx, wizard.rect.centery, 
                        (mouse_pos[0] + offset_x, mouse_pos[1] + offset_y)
                    )
                    last_spell_time = current_time  # Update the last spell fire time
            
            if event.key == pygame.K_e:
                inventory_showing = not inventory_showing
            
            if event.key == pygame.K_c:
                if inventory_showing and active_crafter is not None:
                    crafter.craft(inventory, hotbar)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            inventory.handle_click(mouse_pos)
    
    crafting_collision = pygame.sprite.groupcollide(wizard_group, crafter_group, False, False)
    if crafting_collision != {}:
        active_crafter = crafting_collision[wizard][0]
    else:
        active_crafter = None

    # Update game objects
    keys = pygame.key.get_pressed()
    
    mouse_pos = pygame.mouse.get_pos()
    wizard.update(keys, mouse_pos)

    spells.update()
    mobs.update(wizard.rect.center)
    particles.update()

    # Check for collisions between spells and mobs
    hits = pygame.sprite.groupcollide(mobs, spells, False, False)
    for mob in hits:
        mob.health -= 10
        
        for hit_spell in hits[mob]:
            hit_spell.update(hit=True)
        
        if mob.health <= 0:
            if random.randint(0, 10) < 11:
                shard = Shard(mob.biome, mob.rect.centerx, mob.rect.centery)
            
                all_sprites.add(shard)
                dropped_shards.add(shard)
            
            score += 1
            mob.kill()

    # Check for collisions between the wizard and mobs  
    mob_hits = pygame.sprite.groupcollide(wizard_group, mobs, False, True)
    for mob in mob_hits.get(wizard, []):
        wizard.health -= mob.power

    if wizard.health <= 0:
        print("GAME OVER")
        running = False

    pickups = pygame.sprite.groupcollide(wizard_group, dropped_shards, False, False)
    for shard in pickups.get(wizard,[]):
        inventory.add_shard(shard)
        
    # planet_collisions = pygame.sprite.groupcollide(wizard_group, planet_group, False, False)
    
    for planet in planet_group:
        
        dist_x = planet.x - wizard.rect.centerx
        dist_y = planet.y - wizard.rect.centery
        distance = (dist_x**2 + dist_y**2) ** 0.5
        if distance < planet.radius *.8:
            angle = math.atan2(dist_y, dist_x)
            wizard.rect.x += math.cos(angle) * (distance - planet.radius*.8)
            wizard.rect.y += math.sin(angle) * (distance - planet.radius*.8)
    # Draw everything
    screen.fill(BLACK)
    tiles.draw_tiles(screen, offset_x, offset_y)
    planet_manager.draw_planets(wizard.rect.x, wizard.rect.y, screen, offset_x, offset_y)
    planet_manager.mob_gen(wizard.rect.x, wizard.rect.y)
    draw_sprites(all_sprites, screen, offset_x, offset_y)

    draw_healthbars(wizard, mobs, screen, offset_x, offset_y)
    
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    wizard.draw(screen, offset_x, offset_y)
    
    # Draw hotbar
    hotbar.draw(screen,)

    if inventory_showing:
        inventory.draw(screen)
        
        if active_crafter is not None:
            active_crafter.draw(screen, inventory)

    pygame.display.flip()

pygame.quit()

