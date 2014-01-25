import pygame
import random
import sys

from pygame.locals import * 

from pysometric import settings
from pysometric.lib.tile import TileTable, TileBlock, IsometricMap
from pysometric.lib.camera import Camera

pygame.init() 
 
window = pygame.display.set_mode(settings.SCREEN_RESOLUTION, FULLSCREEN) 
pygame.display.set_caption('PySometric') 
screen = pygame.display.get_surface() 

def input(events): 
   for event in events: 
      if event.type == QUIT: 
         sys.exit(0) 
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
         sys.exit(0)
      elif event.type == MOUSEMOTION:# and event.button == RIGHT:
         if pygame.mouse.get_pressed() == (0,0,1):
            cam.set_offset(event.rel)
            tm.draw_map(screen, tile_bg, cam.offset)
      elif event.type == KEYDOWN and event.key == K_UP:
          cam.set_offset(0, 32)
          tm.draw_map(screen, tile_bg, cam.offset)
      elif event.type == KEYDOWN and event.key == K_DOWN:
          cam.set_offset(0,-32)
          tm.draw_map(screen, tile_bg, cam.offset)
      elif event.type == KEYDOWN and event.key == K_LEFT:
          cam.set_offset(64, 0)
          tm.draw_map(screen, tile_bg, cam.offset)
      elif event.type == KEYDOWN and event.key == K_RIGHT:
          cam.set_offset(-64, 0)
          tm.draw_map(screen, tile_bg, cam.offset)

cam = Camera()

tt = TileTable()
tm = IsometricMap(settings.MAP_WIDTH, settings.MAP_HEIGHT) 
tile_bg = tm.generate_background(tt.tiledict)

frame = 0
tm.draw_map(screen, tile_bg, cam.offset)
clock = pygame.time.Clock()

while True: 
    clock.tick(60)
    input(pygame.event.get())
    pygame.display.flip()

