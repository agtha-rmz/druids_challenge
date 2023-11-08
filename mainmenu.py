import arcade
from constants import *
from gameview import GameView

class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""

    def on_show_view(self):
        """Called when switching to this view."""
        self.background = arcade.load_texture('layers-mainmenu/JWDLx5AZBtI.jpg')

    def on_draw(self):
        """Draw the menu"""
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
        """Use a mouse press to advance to the 'game' view."""
        game_view = GameView()
        self.window.show_view(game_view)

def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()