# Constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constantes usadas para escalar los sprites del tamaño original
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING / 2
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Constantes de disparo
SPRITE_SCALING_LASER = 0.3
SHOOT_SPEED = 15
BULLET_SPEED = 12
BULLET_DAMAGE = 25

# Velocidad del movimiento del jugador, en pixel por frame
PLAYER_MOVEMENT_SPEED = 7

GRAVITY = 1.5
PLAYER_JUMP_SPEED = 30

# Cuantos pixels para mantener el margen entre el jugador 
# y el borde de la pantalla al mínimo.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

PLAYER_START_X = 2
PLAYER_START_Y = 1

# Se invierten valores ya que los Sprites miraban hacia la izquierda por defecto"
RIGHT_FACING = 1
LEFT_FACING = 0

# Nombres de las capas de nuestro TileMap
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_BULLETS = "Bullets"
