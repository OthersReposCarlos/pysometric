import os
import pygame
import random
import sys

from pygame.locals import * 
 
pygame.init() 
 
window = pygame.display.set_mode((800, 600)) 
pygame.display.set_caption('Isometric Game Engine') 
screen = pygame.display.get_surface() 
tileset_file_name = os.path.join('/vol/isometric/production/releases/current/assets/images', 'iso-64x64-outside.png')


class MapCell(object):
    def __init__(self, tile_id):
        self.tile_id = tile_id

class MapRow(object):
    def __init__(self):
        self.row = []

class TileMap(object):
    def __init__(self, width, height, tilefile):
        self.width = width
        self.height = height
        self.tilefile = tilefile
        self.cols = []

        self.tile_width = 64
        self.tile_height = 64

        self.tile_table = self._loadTileTable()
        self._createMap()

        print self.tile_table

    def _loadTileTable(self):
        image = pygame.image.load(self.tilefile).convert_alpha()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_y in range(0, 1):
            line = []
            tile_table.append(line)
            for tile_x in range(0, 4):
                rect = (self.tile_width * tile_x, self.tile_height * tile_y, 
                        self.tile_width, self.tile_height)
                line.append(image.subsurface(rect))
        return tile_table

    def _createMap(self):
        for j in xrange(0, self.height):
            m = MapRow()
            for i in xrange(0, self.width):
                mc = MapCell(random.choice([0,1,2,3]))
                m.row.append(mc)
            self.cols.append(m)

    def drawMap(self, camera_offset):
        for j in xrange(0, self.height):
            for i in xrange(0, self.width):
                screen.blit(self.tile_table[0][ self.cols[j].row[i].tile_id ], (i*64 + (j%2 * 32) + camera_offset[0], j*16 + camera_offset[1]))

    def printMap(self):
        for j in xrange(0, self.height):
            sys.stdout.write("[ ")
            for i in xrange(0, self.width):
                sys.stdout.write("%s " % self.cols[j].row[i].tile_id)
            print "]"
        print "\n"
            
 
def input(events): 
   for event in events: 
      if event.type == QUIT: 
         sys.exit(0) 
      elif event.type == KEYDOWN and event.key == K_UP:
          camera_offset[1] += 32
          tm.drawMap(camera_offset)
      elif event.type == KEYDOWN and event.key == K_DOWN:
          camera_offset[1] -= 32
          tm.drawMap(camera_offset)
      elif event.type == KEYDOWN and event.key == K_LEFT:
          camera_offset[0] += 64
          tm.drawMap(camera_offset)
      elif event.type == KEYDOWN and event.key == K_RIGHT:
          camera_offset[0] -= 64
          tm.drawMap(camera_offset)
      else: 
         print event 

camera_offset = [-128, -128]
tm = TileMap(30, 60, tileset_file_name) 
tm.drawMap(camera_offset)
clock = pygame.time.Clock()

while True: 
    clock.tick(60)
    input(pygame.event.get())
    pygame.display.flip()
