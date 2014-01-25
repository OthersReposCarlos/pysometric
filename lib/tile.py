import pygame
from pygame.locals import *

from pysometric import settings
from pysometric.lib.perlin import PerlinNoiseFactory

class TileTable(object):
    def __init__(self):
        self.ocean_tile_file = settings.OCEAN_TILE_FILE
        self.grass_tile_file = settings.GRASS_TILE_FILE

        self.tiledict_coords = {}
        self.tiledict = {}

        self.tile_width = settings.TILEWIDTH
        self.tile_height = settings.TILEHEIGHT

        self.load_tile_tables()

    def load_tile_tables(self):
        # Load ocean set
        ocean_set_image = pygame.image.load(self.ocean_tile_file).convert_alpha()
        ocean_set_image_width, ocean_set_image_height = ocean_set_image.get_size()

        # Ocean coordinates
        for i, x in enumerate(['0000', 'OCEAN_NONE_1', 'OCEAN_NONE_2']):
            self.tiledict_coords[x] = (i, 0)
        
        # Load grass set
        grass_set_image = pygame.image.load(self.grass_tile_file).convert_alpha()
        grass_set_image_width, grass_set_image_height = grass_set_image.get_size()

        # Grass coordinates
        self.tiledict['1111'] = (grass_set_image.subsurface( (162, 7, 64, 32) ), (0, 0))
        self.tiledict['2222'] = (grass_set_image.subsurface( (162, 7, 64, 32) ), (0, -8))

        self.tiledict['2111'] = (grass_set_image.subsurface( (2, 55, 64, 39) ), (0, -8))
        self.tiledict['1211'] = (grass_set_image.subsurface( (482, 7, 64, 32) ), (0, 0))
        self.tiledict['1121'] = (grass_set_image.subsurface( (642, 55, 64, 15) ), (0, 8))
        self.tiledict['1112'] = (grass_set_image.subsurface( (242, 7, 64, 32) ), (0, 0))

        self.tiledict['2112'] = (grass_set_image.subsurface( (82, 55, 64, 39) ), (0, -8)) 
        self.tiledict['2211'] = (grass_set_image.subsurface( (322, 55, 64, 39) ), (0, -8))
        self.tiledict['1221'] = (grass_set_image.subsurface( (642, 7, 64, 32) ), (0, 0))
        self.tiledict['1122'] = (grass_set_image.subsurface( (402, 7, 64, 32) ), (0, 0))

        self.tiledict['2121'] = (grass_set_image.subsurface( (162, 55, 64, 32) ), (0, -8))
        self.tiledict['1212'] = (grass_set_image.subsurface( (562, 7, 64, 32) ), (0, 0))

        self.tiledict['1222'] = (grass_set_image.subsurface( (722, 7, 64, 32) ), (0, 0))
        self.tiledict['2122'] = (grass_set_image.subsurface( (242, 55, 64, 32) ), (0, -8))
        self.tiledict['2212'] = (grass_set_image.subsurface( (402, 55, 64, 39) ), (0, -8))
        self.tiledict['2221'] = (grass_set_image.subsurface( (482, 55, 64, 32) ), (0, -8))

        # Ocean coordinates
        for k,v in self.tiledict_coords.items():
            self.tiledict[k] = (ocean_set_image.subsurface( (self.tile_width * v[0], 
                                                            self.tile_height * v[1],
                                                            self.tile_width, 
                                                            self.tile_height) ), (0,0,0,0))


class TileBlock(object):
    """Holds altitude, geological and scenery information
    regarding an individual tile block."""

    def __init__(self, tile_type):
        """Initialise the altitudes for each of the tile corners."""
        self.tile_type=tile_type

class IsometricMap(object):
    """Stores the map coordinate, height and tile data
    for the entire isometric map."""

    def __init__(self, width, height):
        self.width=width
        self.height=height
        self.altitudes = self.create_altitude_map()
        self.tiles = self.create_tile_map()

    def create_altitude_map(self):
        """Creates the altitude data structure."""
        pnf = PerlinNoiseFactory(size=settings.PNF_MAP_SIZE, 
                                 tiledim=settings.PNF_TILEDIM, 
                                 repeats=settings.PNF_REPEATS)
        pnm = pnf._generate_map()

        altitudes = []
        for i in range(0, self.width + 1):
            tile_row = []
            for j in range(0, self.height + 1):
                tile_row.append(1)  
            altitudes.append(tile_row)

        for i in range(0, self.width):
            for j in range(0, self.height):
                try:
                    altitudes[i][j] = pnm.sample_map[i][j]
                except:
                    pass

        return altitudes

    def create_tile_map(self):
        """Creates the tile map data structure."""
        tiles = []
        for i in range(0, self.width):
            tile_row = []
            for j in range(0, self.height):
                tb = TileBlock('GRASS')
                tile_row.append(tb)
            tiles.append(tile_row)
        return tiles

    def obtain_tile_slope(self, x, y):
        """Obtains the correct tile slope key to use in
        the tile graphics image set."""
        alts = "%s%s%s%s" % (self.altitudes[x][y], self.altitudes[x][y+1],
                             self.altitudes[x+1][y+1], self.altitudes[x+1][y])
        return alts

    def generate_background(self, tiledict):
        """Generate the whole background image at once, so as not
        to continually call "blit" all the time!"""
        sw = self.width*settings.TILEWIDTH
        sh = self.height*settings.TILEHEIGHT
        image = pygame.Surface((sw+16, sh+16))
        for i in range(0, self.width):
            for j in range(0, self.height):
                td = tiledict['1111']
                image.blit(td[0], (-i*32 + j*32 + td[1][0] + sw/2, i*16 + j*16 + td[1][1]+8))               
                td = tiledict[self.obtain_tile_slope(i, j)]
                image.blit(td[0], (-i*32 + j*32 + td[1][0] + sw/2, i*16 + j*16 + td[1][1]+8))
        return image

    def draw_map(self, screen, tile_bg, camera_offset=[0,0]):
        """Draw the isometric map based on the tile blocks,
        with a camera offset."""
        sw = self.width*settings.TILEWIDTH
        sh = self.height*settings.TILEHEIGHT
        res = settings.SCREEN_RESOLUTION
        screen.fill([0,0,0])
        screen.blit(tile_bg, (camera_offset[0], camera_offset[1]))


