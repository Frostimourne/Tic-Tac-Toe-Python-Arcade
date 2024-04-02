"""
Tic Tac Toe
"""

import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Tic-Tac-Toe"

class TTTGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AMARANTH)

    def setup(self):

        pass

    def on_draw(self):
        self.clear()

    def on_mouse_press(self, x, y, button, key_modifiers):

        pass

    def on_mouse_release(self, x: float, y: float, button: int,
                     modifiers: int):
        """ Called when the user presses a mouse button. """
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        pass


def main():
    window = TTTGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()