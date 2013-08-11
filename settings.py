import os

SCREEN_RESOLUTION = (1280,1024)

MAP_WIDTH=16
MAP_HEIGHT=16

TILEWIDTH=64
TILEHEIGHT=32
OCEAN_TILE_FILE=os.path.join(os.path.dirname(__file__), 'assets/ocean-tiles-64x32.png')
GRASS_TILE_FILE=os.path.join(os.path.dirname(__file__), 'assets/openttd-grass-tiles-64.png')

PNF_MAP_SIZE=16
PNF_TILEDIM=4
PNF_REPEATS=1
