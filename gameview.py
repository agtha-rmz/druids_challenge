"""
Platformer Game

"""
import math 
import os
import arcade
from pc import PlayerCharacter
from entity import HorseEnemy, TreeEnemy
from constants import *

class GameView(arcade.View):
    """
    Clase aplicación principal
    """

    def __init__(self):
        """
        Inicializador del juego
        """

        # Llama clase padre y setea la ventana
        super().__init__()

        # Setea el path para arrancar el programa
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sigue el estado actual de la tecla presionada
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shoot_pressed = False
        self.jump_needs_reset = False

        # Nuestro objeto TileMap
        self.tile_map = None
        self.background_map = None

        # Nuestro objeto Scene
        self.scene = None

        # Variable separa que contiene al Sprite Jugador
        self.player_sprite = None

        # Nuestro motor de física
        self.physics_engine = None

        # Una cámara que puede ser usada para recorrer la pantalla
        self.camera = None

        # Una cámara que puede ser usada para dibujar elementos GUI
        self.gui_camera = None

        self.end_of_map = 0

        # Seguimiento del puntaje
        self.score = 0

        # Mecánicas de disparo
        self.can_shoot = False
        self.shoot_timer = 0

        # Cargar sonidos
        self.collect_coin_sound = arcade.load_sound("sonidos/Collect_Point.mp3")
        self.jump_sound = arcade.load_sound("sonidos/Jump.wav")
        self.game_over = arcade.load_sound("sonidos/Hero_Death_00.mp3")
        self.shoot_sound = arcade.load_sound("sonidos/Shoot.wav")
        self.hit_sound = arcade.load_sound("sonidos/hit.wav")

    def setup(self):
        """Acá se realiza el setup del juego. Se llama a esta función para reiniciarlo."""
        
        # Configuración de las cámaras
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Nombre del mapa
        map_name = ":resources:tiled_maps/map_with_ladders.json"
        self.background_map = arcade.load_texture('layers-mainmenu/forest_back_550_x_400.png')

        # Opciones específicas del TileMap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": False,
            },
            LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
        }

        # Cargar en el TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Inicializar la escene con nuestro TileMap, esto añadirá automáticamente todas las capas
        # de nuestro mapa y la lista de Sprites en la escena en el orden correcto.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Seguimiento del puntaje
        self.score = 0

        # Mecánicas de disparo
        self.can_shoot = True
        self.shoot_timer = 0
     
        # Configurar el jugador, ubicandolo en esas coordenadas específicamente.
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = (
            self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X
        )
        self.player_sprite.center_y = (
            self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y
        )
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Calcular el borde derecho del mapa en pixeles
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # Enemigos
        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]

        for my_object in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            enemy_type = my_object.properties["type"]
            if enemy_type == "robot":
                enemy = HorseEnemy()
            elif enemy_type == "zombie":
                enemy = TreeEnemy()
            enemy.center_x = math.floor(
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
            )
            if "boundary_left" in my_object.properties:
                enemy.boundary_left = my_object.properties["boundary_left"]
            if "boundary_right" in my_object.properties:
                enemy.boundary_right = my_object.properties["boundary_right"]
            if "change_x" in my_object.properties:
                enemy.change_x = my_object.properties["change_x"]
            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)
       
        # Agregar disparos a la escena
        self.scene.add_sprite_list(LAYER_NAME_BULLETS)
    

        # --- Otras cosas
       

        # Crear el 'motor físico'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
            gravity_constant=GRAVITY,
            ladders=self.scene[LAYER_NAME_LADDERS],
            walls=self.scene[LAYER_NAME_PLATFORMS]
        )
    def on_show_view(self):
        self.setup()

    def on_draw(self):
        """Renderizar la pantalla."""

        # Limpiar la pantalla al color de fondo.
        self.clear()

         # Establecer color de fondo
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background_map)

        # Activar nuestra cámara
        self.camera.use()

        # Dibujar la escena
        self.scene.draw()

        # Activar la cámara GUI camera antes de dibujar los elementos GUI
        self.gui_camera.use()

        # Dibujar el puntaje en la escena, desplazándolo con la ventana gráfica
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )
        
        # Dribujar hit boxes.
        # for wall in self.wall_list:
        #     wall.draw_hit_box(arcade.color.BLACK, 3)
        #
        # self.player_sprite.draw_hit_box(arcade.color.RED, 3)

    def process_keychange(self):
        """
        Called when we change a key up/down, or we move on/off a ladder.
        """
        # Proceso arriba/abajo
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Proceso arriba/abajo en una escalera
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Proceso izquierda/derecha
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Se llama siempre que se presione una tecla."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.Q:
            self.shoot_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Llamado cuando el usuario deja de presionar una tecla."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        if key == arcade.key.Q:
            self.shoot_pressed = False

        self.process_keychange()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.camera.zoom(-0.01 * scroll_y)

    def center_camera_to_player(self, speed=0.2):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, speed)

    def on_update(self, delta_time):
        """Movimiento y lógica del juego"""

        # Mover el jugador con el motor físico
        self.physics_engine.update()

        # Actualizar animaciones
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        if self.can_shoot:
            if self.shoot_pressed:
                arcade.play_sound(self.shoot_sound)
                bullet = arcade.Sprite(
                    "attack/35.png",
                    SPRITE_SCALING_LASER,
                )

                if self.player_sprite.facing_direction == RIGHT_FACING:
                    bullet.change_x = BULLET_SPEED
                else:
                    bullet.change_x = -BULLET_SPEED

                bullet.center_x = self.player_sprite.center_x
                bullet.center_y = self.player_sprite.center_y

                self.scene.add_sprite(LAYER_NAME_BULLETS, bullet)

                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == SHOOT_SPEED:
                self.can_shoot = True
                self.shoot_timer = 0

        # Actualizar animaciones
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_COINS,
                LAYER_NAME_BACKGROUND,
                LAYER_NAME_PLAYER,
                LAYER_NAME_ENEMIES,
            ],
        )

        # Actualizar plataformas móviles, enemigos y disparos
        self.scene.update(
            [LAYER_NAME_MOVING_PLATFORMS, LAYER_NAME_ENEMIES, LAYER_NAME_BULLETS]
        )

        # Si el enemigo choca contra un límite, necesita invertir su dirección.
        for enemy in self.scene[LAYER_NAME_ENEMIES]:
            if (
                enemy.boundary_right
                and enemy.right > enemy.boundary_right
                and enemy.change_x > 0
            ):
                enemy.change_x *= -1

            if (
                enemy.boundary_left
                and enemy.left < enemy.boundary_left
                and enemy.change_x < 0
            ):
                enemy.change_x *= -1

        for bullet in self.scene[LAYER_NAME_BULLETS]:
            hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene[LAYER_NAME_ENEMIES],
                    self.scene[LAYER_NAME_PLATFORMS],
                    self.scene[LAYER_NAME_MOVING_PLATFORMS],
                ],
            )

            if hit_list:
                bullet.remove_from_sprite_lists()

                for collision in hit_list:
                    if (
                        self.scene[LAYER_NAME_ENEMIES]
                        in collision.sprite_lists
                    ):
                        # Si el impacto fue contra un enemigo
                        collision.health -= BULLET_DAMAGE

                        if collision.health <= 0:
                            collision.remove_from_sprite_lists()
                            self.score += 100

                        # Sonido de impacto
                        arcade.play_sound(self.hit_sound)

                return

            if (bullet.right < 0) or (
                bullet.left
                > (self.tile_map.width * self.tile_map.tile_width) * TILE_SCALING
            ):
                bullet.remove_from_sprite_lists()

        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[LAYER_NAME_COINS],
                self.scene[LAYER_NAME_ENEMIES],
            ],
        )

        # Loop para remover monedas si fueron tocadas
        for collision in player_collision_list:

            if self.scene[LAYER_NAME_ENEMIES] in collision.sprite_lists:
                arcade.play_sound(self.game_over)
                game_over = GameOverView()
                self.window.show_view(game_over)
                return
            else:
                # Puntaje por cada moneda
                if "Points" not in collision.properties:
                    print("Warning, collected a coin without a Points property.")
                else:
                    points = int(collision.properties["Points"])
                    self.score += points

                # Remover la moneda
                collision.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)

        # Posición de la cámara
        self.center_camera_to_player()

class GameOverView(arcade.View):
    """Clase para la vista Game Over"""

    def on_show_view(self):
        """Se llama cuando se cambia a esta vista"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Dibujar la vista Game Over"""
        self.clear()
        arcade.draw_text(
            "Game Over - Click para reiniciar",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Usa el click del mouse para avanzar la vista del juego."""
        game_view = GameView()
        self.window.show_view(game_view)

