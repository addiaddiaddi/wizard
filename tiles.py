import pygame
import random

from constants import *

class Tiles:
    def __init__(self, width, height):
        self.file = 'assets/gfx/cave.png'
        self.tile_width = 32
        self.tileset = pygame.image.load(self.file)
        self.tilemap = [[random.randint(0, 4) for _ in range(width // self.tile_width)] for _ in range(height // self.tile_width)]

    def get_tile(self, row, col):
        TILE_SIZE = self.tile_width
        tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile.blit(self.tileset, (0, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return tile

    def draw_tiles(self, screen, offset_x, offset_y):
        TILE_SIZE = self.tile_width
        for row_idx, row in enumerate(self.tilemap):
            for col_idx, tile_id in enumerate(row):
                tile_row = tile_id // (self.tileset.get_width() // TILE_SIZE)
                tile_col = tile_id % (self.tileset.get_width() // TILE_SIZE)
                tile = self.get_tile(tile_row, tile_col)
                screen.blit(tile, (col_idx * TILE_SIZE - offset_x, row_idx * TILE_SIZE - offset_y))