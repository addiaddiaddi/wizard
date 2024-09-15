import pygame

from classes.constants import RED, GREEN, sprite_preloader, game_started

def load_sprite(url):    
    if sprite_preloader.get(url) is None:
        sprite_preloader[url] = pygame.image.load(url).convert_alpha()

    return sprite_preloader[url]

def get_camera_offset(screen, wizard):
    screen_center_x = screen.get_width() // 2
    screen_center_y = screen.get_height() // 2
    offset_x = wizard.rect.centerx - screen_center_x
    offset_y = wizard.rect.centery - screen_center_y
    return offset_x, offset_y

def draw_sprites(all_sprites, screen, offset_x, offset_y):
    for sprite in all_sprites:
        sprite.rect.x -= offset_x
        sprite.rect.y -= offset_y
        
    all_sprites.draw(screen)

    for sprite in all_sprites:
        sprite.rect.x += offset_x
        sprite.rect.y += offset_y

def draw_healthbars(wizard, mobs, screen, offset_x, offset_y):
    for mob in mobs:
        health_bar_width = mob.image.get_width()
        health_ratio = mob.health / mob.max_health
        health_bar_fill = health_bar_width * health_ratio
        pygame.draw.rect(screen, RED, (mob.rect.x - offset_x, mob.rect.y - 10 - offset_y, health_bar_width, 5))
        pygame.draw.rect(screen, GREEN, (mob.rect.x - offset_x, mob.rect.y - 10 - offset_y, health_bar_fill, 5))

    health_bar_width = 128
    health_ratio = wizard.health / wizard.max_health
    health_bar_fill = health_bar_width * health_ratio
    pygame.draw.rect(screen, RED, (wizard.rect.x - offset_x, wizard.rect.y - 10 - offset_y, health_bar_width, 5))
    pygame.draw.rect(screen, GREEN, (wizard.rect.x - offset_x, wizard.rect.y - 10 - offset_y, health_bar_fill, 5))

def generate_lore(biome):
    from openai import OpenAI
    import os
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # Set your OpenAI API key

    prompt = f"create a story about a wizard who is fighting monsters in space around the planet based on the {biome} biome. make it approximately 125 words and try to make it funny."

    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message.content


if __name__ == "main":

    print(generate_lore('industrious'))