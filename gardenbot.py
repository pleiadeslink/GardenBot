import pygame, sys, os, random, pathlib
from pygame.locals import *
from mastodon import Mastodon

# Mastodon token and domain
mastodon = Mastodon(
    access_token = 'asdf',
    api_base_url = 'https://botsin.space/'
)

# Set a dummy display to run headless mode
os.environ["SDL_VIDEODRIVER"] = "dummy" 

# Init pygame and set final image resolution
pygame.init()
screen = pygame.display.set_mode((1064, 600), DOUBLEBUF)
pygame.display.init()

# Set sprite dimensions
tileWidth = 128
tileHeight = 128
 
# Init a 8x8 map
gardenMap = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

# Load images and save them in a list
background = pygame.image.load('tx_bg.png')
graphics = [
pygame.image.load('tx_grass.png').convert_alpha(),
pygame.image.load('tx_tree.png').convert_alpha(),
pygame.image.load('tx_rock.png').convert_alpha(),
pygame.image.load('tx_flowersp.png').convert_alpha(),
pygame.image.load('tx_flowersy.png').convert_alpha(),
pygame.image.load('tx_flowersb.png').convert_alpha(),
pygame.image.load('tx_fountain.png').convert_alpha(),
pygame.image.load('tx_column.png').convert_alpha(),
pygame.image.load('tx_cow.png').convert_alpha(),
pygame.image.load('tx_crack.png').convert_alpha()
]

# Print background
screen.blit(background, (0,0))

# Iterate each map tile
for row_nb, row in enumerate(gardenMap):
    for col_nb, tile in enumerate(row):
        
        # Select a random sprite using weight values
        tileImage = random.choices(graphics, weights=(18, 12, 5, 10, 10, 10, 1, 3, 3, 0.5), k=1)
        
        # Maths for isometric positioning
        # Thanks to https://python-forum.io/Thread-PyGame-Simple-code-for-isometric-2D-games
        cart_x = row_nb * (tileWidth / 2)
        cart_y = col_nb * (tileHeight / 2) 
        iso_x = cart_x - cart_y
        iso_y = (cart_x + cart_y) / 2
        centered_x = screen.get_rect().centerx + iso_x
        centered_y = screen.get_rect().centery / 2 + iso_y
        
        # Print the tile sprite at its position
        screen.blit(tileImage[0], (centered_x - (tileWidth / 2), centered_y - (tileHeight + 8)))

# Save the image into a PNG file
pygame.image.save(screen,"garden.png")

# Upload PNG file to Mastodon
media = mastodon.media_post("garden.png")
mastodon.status_post("", media_ids=media)

# Delete the image, since it is no longer needed
os.remove("garden.png")