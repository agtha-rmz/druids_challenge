# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING / 2
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Shooting Constants
SPRITE_SCALING_LASER = 0.3
SHOOT_SPEED = 15
BULLET_SPEED = 12
BULLET_DAMAGE = 25

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7

GRAVITY = 1.5
PLAYER_JUMP_SPEED = 30

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

PLAYER_START_X = 2
PLAYER_START_Y = 1

# Se invierten valores ya que los Sprites miraban hacia la izq por defecto"
RIGHT_FACING = 1
LEFT_FACING = 0

# Layer Names from our TileMap
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_BULLETS = "Bullets"
