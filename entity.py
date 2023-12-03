import arcade

from constants import *

def load_texture_pair(filename):
    """
    Carga un par de texturas, siendo la segunda una imagen espejo.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        # Mira a la derecha por defecto
        self.facing_direction = RIGHT_FACING

        # Secuencia de imagenes
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        
        main_path = f"sprites/{name_folder}/{name_file}"
        
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")
        self.idle_texture_pair = load_texture_pair(f'{main_path}_idle0.png')

        # Carga texturas para caminar
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Carga texturas para trepar
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Setea la imagen inicial
        self.texture = self.idle_texture_pair[0]

        # Hit box estará seteado basándose en la primer imagen usada. Si querés especificar
        # un hit box diferente, podés hacerlo con el código de abajo.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.set_hit_box(self.texture.hit_box_points)

class Enemy(Entity):
    def __init__(self, name_folder, name_file):

        # Setup clase padre
        super().__init__(name_folder, name_file)

        self.should_update_walk = 0
        self.health = 0
    
    def update_animation(self, delta_time: float = 1 / 60):

        # Mirar hacia la izquierda o hacia la derecha
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Animación inactivo
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Animación caminar
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1

class HorseEnemy(Enemy):
    def __init__(self):

        # Setup clase padre
        super().__init__("horse", "horse")

        self.health = 50

class TreeEnemy(Enemy):
    def __init__(self):

        # Setup clase padre
        super().__init__("tree", "tree")

        self.health = 100

