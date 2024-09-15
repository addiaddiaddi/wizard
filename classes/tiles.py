import pygame
import environment.get_environments 
class Tiles:
    def __init__(self, width, height):
        print(width, height)
        # Load 9 images (1024x1024 each) from file paths
        # image_paths = [environment.get_environments.get_background(i) for i in range(9)]
        # image_paths = [f"background_{i}.png" for i in range(9)]
        
        # Convert image paths to pygame surfaces
        # images = [pygame.image.load(image_path) for image_path in image_paths]
        
        # Check the sizes of the images to ensure they are 1024x1024
        # for i, img in enumerate(images):
        #     if img.get_size() != (1024, 1024):
        #         raise ValueError(f"Image {image_paths[i]} is not 1024x1024! Got {img.get_size()} instead.")
        
        # Create a surface to combine the 9 images into a 3x3 grid (3072x3072 total)
        self.combined_image = pygame.Surface((1024 * 3, 1024 * 3))

        
        # Blit the 9 images into the combined image at their correct positions
        for i in range(9):
            # img = environment.get_environments.get_background(i)
            img = pygame.image.load(f"background_{i+1}.png")
            # img = pygame.image.load(img) 

            row = i // 3  # Determine the row in the 3x3 grid
            col = i % 3   # Determine the column in the 3x3 grid
            print(f"Blitting image {i} at position {(col * 1024, row * 1024)}")  # Debug print for blit positions
            self.combined_image.blit(img, (col * 1024, row * 1024))  # Blit image to its place in the 3x3 grid

        self.tile_width = 32
        self.tiles_per_image_row = (1024 * 3) // self.tile_width  # Number of tiles per row in the 3072x3072 image

        # Generate a tilemap with sequential tile IDs (non-random)
        self.tilemap = []
        for row in range(height // self.tile_width):
            self.tilemap.append([])
            for col in range(width // self.tile_width):
                # Assign tile IDs in a sequential order
                tile_id = (row * (width // self.tile_width) + col) % (self.tiles_per_image_row ** 2)
                self.tilemap[row].append(tile_id)
        pygame.image.save(self.combined_image, "combined_image_debug.png")

    def get_tile(self, row, col):
        TILE_SIZE = self.tile_width
        tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile.blit(self.combined_image, (0, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return tile

    def draw_tiles(self, screen, offset_x, offset_y):
        TILE_SIZE = self.tile_width
        for row_idx, row in enumerate(self.tilemap):
            for col_idx, tile_id in enumerate(row):
                # Determine the tile position within the combined image
                tile_row = tile_id // self.tiles_per_image_row
                tile_col = tile_id % self.tiles_per_image_row
                
                # Get the appropriate tile from the combined image
                tile = self.get_tile(tile_row, tile_col)
                screen.blit(tile, (col_idx * TILE_SIZE - offset_x, row_idx * TILE_SIZE - offset_y))

# import pygame
# import environment.get_environments 
# import pygame
# import environment.get_environments
# import random  # Import random module to shuffle tiles

# class Tiles:
#     def __init__(self, width, height):
#         print(width, height)
#         # Load 9 images (1024x1024 each) from file paths
#         # image_paths = [environment.get_environments.get_background(i) for i in range(9)]
#         image_paths = [f"background_{i}.png" for i in range(9)]
#         # Convert image paths to pygame surfaces
#         images = [pygame.image.load(image_path) for image_path in image_paths]
        
#         # Check the sizes of the images to ensure they are 1024x1024
#         for i, img in enumerate(images):
#             if img.get_size() != (1024, 1024):
#                 raise ValueError(f"Image {image_paths[i]} is not 1024x1024! Got {img.get_size()} instead.")
        
#         # Create a surface to combine the 9 images into a 3x3 grid (3072x3072 total)
#         self.combined_image = pygame.Surface((1024 * 3, 1024 * 3))

#         # Blit the 9 images into the combined image at their correct positions
#         for i, img in enumerate(images):
#             row = i // 3  # Determine the row in the 3x3 grid
#             col = i % 3   # Determine the column in the 3x3 grid
#             print(f"Blitting image {i} at position {(col * 1024, row * 1024)}")  # Debug print for blit positions
#             self.combined_image.blit(img, (col * 1024, row * 1024))  # Blit image to its place in the 3x3 grid

#         self.tile_width = 32
#         self.tiles_per_image_row = (1024 * 3) // self.tile_width  # Number of tiles per row in the 3072x3072 image

#         # Generate a list of tile IDs and shuffle them to randomize the order
#         tile_ids = list(range(self.tiles_per_image_row * (height // self.tile_width)))
#         random.shuffle(tile_ids)  # Shuffle tile IDs to randomize the order

#         # Create the tilemap by filling it with randomized tile IDs
#         self.tilemap = []
#         tile_id_index = 0
#         for row in range(height // self.tile_width):
#             self.tilemap.append([])
#             for col in range(width // self.tile_width):
#                 self.tilemap[row].append(tile_ids[tile_id_index])
#                 tile_id_index += 1

#         pygame.image.save(self.combined_image, "combined_image_debug.png")

#     def get_tile(self, row, col):
#         TILE_SIZE = self.tile_width
#         tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
#         tile.blit(self.combined_image, (0, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
#         return tile

#     def draw_tiles(self, screen, offset_x, offset_y):
#         TILE_SIZE = self.tile_width
#         for row_idx, row in enumerate(self.tilemap):
#             for col_idx, tile_id in enumerate(row):
#                 # Determine the tile position within the combined image
#                 tile_row = tile_id // self.tiles_per_image_row
#                 tile_col = tile_id % self.tiles_per_image_row
                
#                 # Get the appropriate tile from the combined image
#                 tile = self.get_tile(tile_row, tile_col)
#                 screen.blit(tile, (col_idx * TILE_SIZE - offset_x, row_idx * TILE_SIZE - offset_y))

