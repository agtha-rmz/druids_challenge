import arcade
from constants import *
from gameview import GameView

class MainMenu(arcade.View):
    """Clase que maneja la vista 'Menú'."""

    def on_show_view(self):
        """Llamado al cambiar a esta vista."""
        self.background = arcade.load_texture('layers-mainmenu/JWDLx5AZBtI.jpg')

    def on_draw(self):
        """Dibuja el menu"""
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text(
            'El desafío del Druida',
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )
        start_x = 20
        start_y = 50
        
        arcade.draw_text(
            "Haz click con el mouse para iniciar", 
            start_x, start_y, arcade.color.BLACK, 12,
            anchor_x="left", anchor_y="top")
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Usa el click del mouse para avanzar a la vista del juego."""
        game_view = GameView()
        self.window.show_view(game_view)

def main():
    """Funcion principal"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()