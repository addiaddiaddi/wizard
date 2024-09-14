import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wizard vs Mobs")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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
        self.health = 100

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Spell class
class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_pos):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        # Calculate direction vector towards mouse position
        dx, dy = mouse_pos[0] - x, mouse_pos[1] - y
        distance = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
        self.velocity_x = self.speed * dx / distance
        self.velocity_y = self.speed * dy / distance

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        # Remove the spell if it goes off screen
        if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y > HEIGHT or self.rect.y < 0:
            self.kill()

# Mob class
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH + 20, WIDTH + 100)
        self.rect.y = random.randint(0, HEIGHT)
        self.speed = random.randint(2, 6)
        self.power = 20

    def update(self, destination):
        
        # Calculate direction vector towards the player
        player_x, player_y = destination
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        distance = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
        
        self.rect.x += self.speed * dx / distance
        self.rect.y += self.speed * dy / distance
        
    
        # if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y > HEIGHT or self.rect.y < 0:
        #     self.kill()


# Create sprite groups
all_sprites = pygame.sprite.Group()
spells = pygame.sprite.Group()
mobs = pygame.sprite.Group()
wizard_group = pygame.sprite.Group()

# Instantiate wizard
wizard = Wizard()
wizard_group.add(wizard)
all_sprites.add(wizard)

# Game loop
# Game loop
running = True
while running:
    clock.tick(60)
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Fire spell
                mouse_pos = pygame.mouse.get_pos()
                spell = Spell(wizard.rect.centerx, wizard.rect.centery, mouse_pos)
                all_sprites.add(spell)
                spells.add(spell)

    # Spawn mobs randomly
    if random.randint(1, 100) < 3:
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)

    # Update the wizard separately
    keys = pygame.key.get_pressed()
    wizard.update(keys)

    # Update all other sprites
    spells.update()
    mobs.update(wizard.rect.center)

    # Check for collisions between spells and mobs
    hits = pygame.sprite.groupcollide(mobs, spells, True, True)

    hits = pygame.sprite.groupcollide(wizard_group, mobs, False, True)
    
    for hit_mob in hits.get(wizard, []):
        wizard.health -= hit_mob.power
        
    if wizard.health <= 0:
        print("GAME OVER")
        running = False

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
