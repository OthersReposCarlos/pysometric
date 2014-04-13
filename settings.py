import os

SCREEN_RESOLUTION = (1920,1200)

MAP_WIDTH=64
MAP_HEIGHT=MAP_WIDTH

TILEWIDTH=64
TILEHEIGHT=32
OCEAN_TILE_FILE=os.path.join(os.path.dirname(__file__), 'assets/ocean-tiles-64x32.png')
GRASS_TILE_FILE=os.path.join(os.path.dirname(__file__), 'assets/openttd-grass-tiles-64.png')

PNF_MAP_SIZE=MAP_WIDTH
PNF_TILEDIM=4
PNF_REPEATS=1

MENU_BG_FILE=os.path.join(os.path.dirname(__file__), 'assets/images/menu.png')
MENU_GRAPHICS_FILE=os.path.join(os.path.dirname(__file__), 'assets/images/menu_graphics.png')
