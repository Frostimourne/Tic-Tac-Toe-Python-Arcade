# Tic Tac Toe
import arcade
import os

import arcade.csscolor
import arcade.gui


# Current Directory
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Screen Dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Tic-Tac-Toe"

# Sizing Constant
GLOBAL_SCALE = 1

# X and O size?
TILE_WIDTH = 200 * GLOBAL_SCALE
TILE_HEIGHT = 200 * GLOBAL_SCALE


# Board Size
BOARD_MARGIN = 1.10
BOARD_WIDTH = 700 * GLOBAL_SCALE
BOARD_HEIGHT = 700 * GLOBAL_SCALE

# Board starting location
BOARD_X = SCREEN_WIDTH/2
BOARD_Y = SCREEN_HEIGHT/2

#Tile starting locations
X_START_X = TILE_WIDTH/2 * GLOBAL_SCALE * BOARD_MARGIN
X_START_Y = SCREEN_HEIGHT/2

O_START_X = SCREEN_WIDTH - (TILE_WIDTH/2 * GLOBAL_SCALE * BOARD_MARGIN)
O_START_Y = SCREEN_HEIGHT/2

# Tile Constants
TILE_VALUES = ["X","O"]

# Valid Placement Spacing
PLACEMENT_SPACING = TILE_HEIGHT + 50

# Button Style
DEFAULT_STYLE = {
    "font_name": ("calibri", "arial"),
    "font_size": 15,
    "font_color": arcade.color.WHITE,
    "border_width": 2,
    "border_color": None,
    "bg_color": (21, 19, 21),

    # used if button is pressed
    "bg_color_pressed": arcade.color.WHITE,
    "border_color_pressed": arcade.color.WHITE,  # also used when hovered
    "font_color_pressed": arcade.color.BLACK,
}

class Tile(arcade.Sprite):
    # Tile Sprite
    def __init__(self, value, scale=1):
        #Tile constructor

        self.value = value
        self.image_file_name = f"{CURRENT_DIRECTORY}/images/{self.value}.png"
        super().__init__(self.image_file_name, scale, hit_box_algorithm=None) 

class Board(arcade.Sprite):
    #Board Sprite
    def __init__(self, scale=1):
        self.image_file_name = f"{CURRENT_DIRECTORY}/images/Board.png"
        super().__init__(self.image_file_name, scale, hit_box_algorithm=None)


class TTTGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)

        self.tile_list = None
        self.background_sprites = None

        self.x_turn = True
        self.tile_positions = None
        self.placed_tiles = 0
        self.game_over = False
        self.game_over_message = None
        self.flip_player = True

        arcade.set_background_color(arcade.color.WHITE)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        reset_button = arcade.gui.UIFlatButton(x= 1050, y= 50, text="RESTART", width=200, height=100)
        reset_button.on_click = self.reset
        self.manager.add(reset_button)

        # Held Tile
        self.held_tile = None

        # List of Valid Places
        self.tile_placement_list = None


    def setup(self):

        self.x_turn = True
        self.placed_tiles = 0
        self.game_over = False
        self.game_over_message = "DRAW"
        self.flip_player = True

        self.tile_positions = []
        for i in range(0,9):
            self.tile_positions.append(None)

        self.tile_list = arcade.SpriteList()
        self.background_sprites = arcade.SpriteList()

        board = Board()
        board.position = BOARD_X, BOARD_Y
        self.background_sprites.append(board)

        # Create Valid Placement Locations
        self.tile_placement_list = arcade.SpriteList()

        for i in range(-1,2):
            for j in range(-1,2):
                place = arcade.SpriteSolidColor(5,5,arcade.csscolor.WHITE_SMOKE)
                place.position = BOARD_X + i * PLACEMENT_SPACING, BOARD_Y + j * PLACEMENT_SPACING
                self.tile_placement_list.append(place)


        for tile_count in range(6):
            for tile_value in TILE_VALUES:
                tile = Tile(tile_value)

                if(tile_value == "X"):
                    tile.position = X_START_X, X_START_Y
                else:
                    tile.position = O_START_X, O_START_Y

                self.tile_list.append(tile)
            
        pass

    def reset(self, event):
        self.setup()

    def on_draw(self):
        self.clear()
        self.background_sprites.draw()
        self.tile_placement_list.draw()
        self.tile_list.draw()

        player_turn = "O"
        if(self.x_turn):
            player_turn = "X"
        arcade.draw_text(f"{player_turn}\'s turn!",
                         30, SCREEN_HEIGHT - 50,
                         arcade.color.BLACK,
                         30, font_name="Kenney Blocks")
        if self.game_over:
            arcade.draw_text(f"{self.game_over_message}",
                         SCREEN_WIDTH - 250, SCREEN_HEIGHT - 50,
                         arcade.color.BLACK,
                         40, font_name="Kenney Blocks")
            self.manager.draw()

            
        
    def check_game_end(self):

        current_player_tile = 'O'
        if self.x_turn:
            current_player_tile = 'X'

        if self.placed_tiles > 8:
            self.game_over = True

        if (self.tile_positions[0] == self.tile_positions[1] == self.tile_positions[2] == current_player_tile
            or self.tile_positions[3] == self.tile_positions[4] == self.tile_positions[5] == current_player_tile
            or self.tile_positions[6] == self.tile_positions[7] == self.tile_positions[8] == current_player_tile
            or self.tile_positions[0] == self.tile_positions[3] == self.tile_positions[6] == current_player_tile
            or self.tile_positions[1] == self.tile_positions[4] == self.tile_positions[7] == current_player_tile
            or self.tile_positions[2] == self.tile_positions[5] == self.tile_positions[8] == current_player_tile
            or self.tile_positions[0] == self.tile_positions[4] == self.tile_positions[8] == current_player_tile
            or self.tile_positions[2] == self.tile_positions[4] == self.tile_positions[6] == current_player_tile):
            self.game_over = True
            self.game_over_message = f"{current_player_tile} WINS"


        if not self.game_over and self.flip_player == True:
            self.x_turn = not self.x_turn
        self.flip_player = True
        

    def on_mouse_press(self, x, y, button, key_modifiers):
        # Get list of tiles we've clicked on
        tiles = arcade.get_sprites_at_point((x, y), self.tile_list)

        # Have we clicked on a tile?
        if len(tiles) > 0 and not self.game_over:

            # Might be a stack of cards, get the top one
            primary_tile = tiles[0]

            # Is Tile already in a place
            if len(arcade.check_for_collision_with_list(primary_tile, self.tile_placement_list)) != 0:
                return

            if (self.x_turn and primary_tile.value == "X") or ( not self.x_turn and primary_tile.value == "O"):
                # If turn matches tile, grab the tile we are clicking on
                self.held_tile = primary_tile
                # Put on top in drawing order
                self.pull_to_top(self.held_tile)

        pass

    def on_mouse_release(self, x: float, y: float, button: int,
                     modifiers: int):
        """ Called when the user presses a mouse button. """

        if self.held_tile == None:
            return

        place, distance = arcade.get_closest_sprite(self.held_tile, self.tile_placement_list)
        reset_position = True

        if arcade.check_for_collision(self.held_tile, place):
            if len(arcade.check_for_collision_with_list(place, self.tile_list)) < 2:
                self.held_tile.position = place.center_x, place.center_y
                self.tile_positions[self.tile_placement_list.index(place)] = self.held_tile.value
                reset_position = False
                self.placed_tiles += 1


        if reset_position:
            self.flip_player = False
            if self.held_tile.value == "X":
                self.held_tile.position = X_START_X, X_START_Y
            else:
                self.held_tile.position = O_START_X, O_START_Y
        
        self.held_tile = None
        self.check_game_end()

        

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        if(self.held_tile != None):
            self.held_tile.center_x += dx
            self.held_tile.center_y += dy

        pass

    def pull_to_top(self, card: arcade.Sprite):
        # Pull tile to top of rendering order (last to render, looks on-top)
        # Remove, and append to the end
        self.tile_list.remove(card)
        self.tile_list.append(card)


def main():
    window = TTTGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()