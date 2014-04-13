import pygame
import random

from pygame.locals import *
from pysometric import settings


class MenuItem(object):
    """A sub menu button."""
    
    def __init__(self, item_name):
        self.item_name = item_name
        self.clicked = False


class Menu(object):
    """Handles the top-level menu."""

    def __init__(self, screen_width, screen_height, menu_items):
        self.menu_bg_image = self._load_menu_image_file()
        self.menu_graphics_image = self._load_menu_graphics_file()

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.menu_types = self._set_menu_types()
        self.menu_item_width = 23
        self.menu_item_height = 23
        self.menu_items = menu_items

        self.width = self._calculate_menu_width()
        self.height = self.menu_item_height
        self.position = self._calculate_position()
        
    
    def _set_menu_types(self):
        """Sets the menu types dictionary for the menu."""
        return {"Railway Construction": self.menu_graphics_image.subsurface( (0, 0, 20, 20) ),
                "Landscaping": self.menu_graphics_image.subsurface( (20, 0, 20, 20) )}

    def _calculate_menu_width(self):
        """Calculates the menu width using the tile width."""
        return len(self.menu_items)*self.menu_item_width

    def _calculate_position(self):
        """Returns the position of the menu as a tuple
        based on initial screen dimensions."""
        return (self.screen_width / 2.0 - self.width, 0.0)

    def _load_menu_image_file(self):
        """Loads the menu image background file."""
        image = pygame.image.load(settings.MENU_BG_FILE).convert_alpha()
        menu_image = {False: image.subsurface( (0, 0, 23, 23) ),
                      True: image.subsurface( (23, 0, 23, 23) )}
        return menu_image

    def _load_menu_graphics_file(self):
        """Loads the menu graphics files."""
        return pygame.image.load(settings.MENU_GRAPHICS_FILE).convert_alpha()

    def _generate_menu(self):
        """Draws the menu to the menu image surface."""
        menu_image = pygame.Surface((self.width, self.height))

        # Blit the background and then icons
        for i, mi in enumerate(self.menu_items):
            menu_image.blit(self.menu_bg_image[mi.clicked], (i*self.menu_item_width, 0))
            menu_image.blit(self.menu_types[mi.item_name], (i*self.menu_item_width+1+1*mi.clicked, 1+1*mi.clicked))
        return menu_image

    def draw_menu(self, screen):
        """Blits the menu image surface to the screen."""
        menu_image = self._generate_menu()
        screen.blit(menu_image, self.position)


def create_main_menu():
    """Creates the main header menu."""
    menu_items = [MenuItem("Railway Construction"), 
                  MenuItem("Landscaping")]

    res = settings.SCREEN_RESOLUTION
    menu = Menu(res[0], res[1], menu_items)
    return menu

