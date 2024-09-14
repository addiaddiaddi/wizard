import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 32*32, 32*32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wizard vs Mobs")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# Game clock
clock = pygame.time.Clock()

# Wizard class
class Wizard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.max_health = 100
        self.health = self.max_health

    def update(self, keys):
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

    def draw_health_bar(self, surface):
        health_bar_width = 50
        health_ratio = self.health / self.max_health
        health_bar_fill = health_bar_width * health_ratio
        pygame.draw.rect(surface, RED, (self.rect.x - offset_x, self.rect.y - 10 - offset_y, health_bar_width, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.x - offset_x, self.rect.y - 10 - offset_y, health_bar_fill, 5))

# Base Spell class
class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_pos, speed=10, direction_offset=0, is_explosive=False, explosion_type="cone", chain_explosion_types=None):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        dx, dy = mouse_pos[0] - x, mouse_pos[1] - y
        angle = math.atan2(dy, dx) + math.radians(direction_offset)
        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)

        # Explosion properties
        self.is_explosive = is_explosive
        self.distance_traveled = 0
        self.explosion_threshold = 300
        self.explosion_type = explosion_type
        self.chain_explosion_types = chain_explosion_types or []  # A list of explosion types to chain

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.distance_traveled += self.speed
        
        # Handle explosion logic
        if self.is_explosive and self.distance_traveled >= self.explosion_threshold:
            self.explode()

        if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y > HEIGHT or self.rect.y < 0:
            self.kill()

    def explode(self):
        """Explode the spell into a cone or circular pattern depending on the type, with random noise."""
        if self.explosion_type == "cone":
            for angle in [-30, 0, 30]:  # Cone explosion with random angle noise
                random_noise = random.uniform(-10, 10)  # Add random noise between -10 and 10 degrees
                new_spell = Spell(self.rect.centerx, self.rect.centery, 
                                  (self.rect.centerx + self.velocity_x, self.rect.centery + self.velocity_y), 
                                  direction_offset=angle + random_noise, is_explosive=True, 
                                  explosion_type=self.chain_explosion_types[0] if self.chain_explosion_types else None,
                                  chain_explosion_types=self.chain_explosion_types[1:] if self.chain_explosion_types else [])  # Pass down chain
                all_sprites.add(new_spell)
                spells.add(new_spell)
        elif self.explosion_type == "circular":
            for angle in range(0, 360, 30):  # Circular explosion with random noise
                random_noise = random.uniform(-15, 15)  # Add random noise between -15 and 15 degrees
                rad_angle = math.radians(angle + random_noise)
                new_velocity_x = self.speed * math.cos(rad_angle)
                new_velocity_y = self.speed * math.sin(rad_angle)
                new_spell = Spell(self.rect.centerx, self.rect.centery, 
                                  (self.rect.centerx + new_velocity_x, self.rect.centery + new_velocity_y), 
                                  direction_offset=0, is_explosive=True, 
                                  explosion_type=self.chain_explosion_types[0] if self.chain_explosion_types else None,
                                  chain_explosion_types=self.chain_explosion_types[1:] if self.chain_explosion_types else [])  # Pass down chain
                all_sprites.add(new_spell)
                spells.add(new_spell)
        self.kill()

# Spell Factory for creating different types of spells
class SpellFactory:
    @staticmethod
    def create_spell(spell_type, x, y, mouse_pos):
        if spell_type == "explosive":
            return Spell(x, y, mouse_pos, is_explosive=True, explosion_type="cone", chain_explosion_types=["circular", "cone", "circular"])
        elif spell_type == "circular":
            return Spell(x, y, mouse_pos, is_explosive=True, explosion_type="circular", chain_explosion_types=["cone", "circular"])
        elif spell_type == "fast":
            return Spell(x, y, mouse_pos, speed=20)
        elif spell_type == "slow":
            return Spell(x, y, mouse_pos, speed=5)
        else:
            return Spell(x, y, mouse_pos)

# Base Mob class
class Mob(pygame.sprite.Sprite):
    def __init__(self, health, speed, color):
        super().__init__()
        
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH + 20, WIDTH + 100)
        self.rect.y = random.randint(0, HEIGHT)
        self.speed = speed
        self.max_health = health
        self.health = self.max_health
        self.power = 20

    def update(self, destination):
        player_x, player_y = destination
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        distance = max(1, (dx**2 + dy**2)**0.5)
        self.rect.x += self.speed * dx / distance
        self.rect.y += self.speed * dy / distance
        
    def draw_health_bar(self, surface):
        health_bar_width = 40
        health_ratio = self.health / self.max_health
        health_bar_fill = health_bar_width * health_ratio
        pygame.draw.rect(surface, RED, (self.rect.x - offset_x, self.rect.y - 10 - offset_y, health_bar_width, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.x - offset_x, self.rect.y - 10 - offset_y, health_bar_fill, 5))

# Mob Factory for creating different types of mobs
class MobFactory:
    @staticmethod
    def create_mob(mob_type):
        if mob_type == "fast":
            return Mob(health=10, speed=5, color=RED)
        elif mob_type == "strong":
            return Mob(health=40, speed=2, color=BLUE)
        else:
            return Mob(health=20, speed=3, color=RED)

# Hotbar class
class Hotbar:
    def __init__(self):
        self.selected_slot = 0  # Default selected spell (slot 1)
        self.spell_types = ["normal", "explosive", "fast", "slow", "circular"]  # Added "circular" spell type

    def select_slot(self, slot):
        if 0 <= slot < len(self.spell_types):
            self.selected_slot = slot

    def get_selected_spell(self):
        return self.spell_types[self.selected_slot]

    def draw(self, surface):
        # Draw a simple hotbar at the bottom of the screen
        for i, spell_type in enumerate(self.spell_types):
            color = YELLOW if i == self.selected_slot else GRAY
            pygame.draw.rect(surface, color, (50 + i * 60, HEIGHT - 60, 50, 50))
            font = pygame.font.Font(None, 36)
            text = font.render(f"{i+1}", True, WHITE)
            surface.blit(text, (65 + i * 60, HEIGHT - 55))

class Tiles:
    def __init__(self):
        self.file = 'assets/gfx/cave.png'
        self.tile_width = 32
        self.tileset = pygame.image.load(self.file)
        import random
        self.tilemap = [[random.randint(0,4) for _ in range(WIDTH // self.tile_width)] for _ in range(HEIGHT // self.tile_width)]
        
    def get_tile(self, row, col):
        TILE_SIZE = self.tile_width
        tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        
        tile.blit(self.tileset, (0, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
        return tile
    
    
    def draw_tiles(self, offset_x, offset_y):
        TILE_SIZE = self.tile_width
        
        for row_idx, row in enumerate(self.tilemap):
            for col_idx, tile_id in enumerate(row):
                # Calculate the row and column of the tile in the tileset
                tile_row = tile_id // (self.tileset.get_width() // TILE_SIZE)
                tile_col = tile_id % (self.tileset.get_width() // TILE_SIZE)
                
                # Get the tile image
                tile = self.get_tile(tile_row, tile_col)
                
                # Draw the tile on the screen
                screen.blit(tile, (col_idx * TILE_SIZE - offset_x, row_idx * TILE_SIZE - offset_y))
    
    
def get_camera_offset(wizard):
    screen_center_x = screen.get_width() // 2
    screen_center_y = screen.get_height() // 2
    offset_x = wizard.rect.centerx - screen_center_x
    offset_y = wizard.rect.centery - screen_center_y
    
    
    return offset_x, offset_y

def draw_sprites():
      # this is pretty janky. might need to adjust later
    for sprite in all_sprites:
        sprite.rect.x -= offset_x
        sprite.rect.y -= offset_y
        
    all_sprites.draw(screen)
    
    for sprite in all_sprites:
        sprite.rect.x += offset_x
        sprite.rect.y += offset_y
# Create sprite groups
all_sprites = pygame.sprite.Group()
spells = pygame.sprite.Group()
mobs = pygame.sprite.Group()
wizard_group = pygame.sprite.Group()
tiles = Tiles()
# Instantiate wizard
wizard = Wizard()
wizard_group.add(wizard)
all_sprites.add(wizard)

# Instantiate hotbar
hotbar = Hotbar()

# Game loop
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check number keys (1-9) for hotbar selection
            if pygame.K_1 <= event.key <= pygame.K_9:
                hotbar.select_slot(event.key - pygame.K_1)

            # Fire a spell on spacebar press
            if event.key == pygame.K_SPACE:
                mouse_pos = pygame.mouse.get_pos()
                selected_spell = hotbar.get_selected_spell()
                spell = SpellFactory.create_spell(selected_spell, wizard.rect.centerx, wizard.rect.centery, mouse_pos)
                all_sprites.add(spell)
                spells.add(spell)

    offset_x, offset_y = get_camera_offset(wizard)
    
    # Spawn mobs randomly
    if random.randint(1, 100) < 3:
        mob = MobFactory.create_mob(random.choice(["fast", "strong", "normal"]))
        all_sprites.add(mob)
        mobs.add(mob)

    keys = pygame.key.get_pressed()
    wizard.update(keys)

    spells.update()
    mobs.update(wizard.rect.center)

    # Check for collisions between spells and mobs
    hits = pygame.sprite.groupcollide(mobs, spells, False, True)
    for mob in hits:
        mob.health -= 10
        if mob.health <= 0:
            mob.kill()

    # Check for collisions between the wizard and mobs
    mob_hits = pygame.sprite.groupcollide(wizard_group, mobs, False, True)
    for mob in mob_hits.get(wizard, []):
        wizard.health -= mob.power

    hits = pygame.sprite.groupcollide(wizard_group, mobs, False, True)
    
    for hit_mob in hits.get(wizard, []):
        wizard.health -= hit_mob.power
    
    if wizard.health <= 0:  
        print("GAME OVER")
        running = False

    # Draw everything
    screen.fill(BLACK)
    
    tiles.draw_tiles(offset_x, offset_y)
    
    
    draw_sprites()
  
    # Draw health bars
    wizard.draw_health_bar(screen)
    for mob in mobs:
        mob.draw_health_bar(screen)

    # Draw hotbar
    hotbar.draw(screen)

    pygame.display.flip()

pygame.quit()
