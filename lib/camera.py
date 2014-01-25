from pysometric import settings

class Camera(object):
    """Stores information about the camera, its offsets
    and maximum constraints."""
    
    def __init__(self):
        self.offset = [0, 0]
        self.map_width = settings.MAP_WIDTH
        self.map_height = settings.MAP_HEIGHT

        self.max_offsets = {'N': self.calc_north_offset_max(),
                            'E': self.calc_east_offset_max(),
                            'S': self.calc_south_offset_max(),
                            'W': self.calc_west_offset_max()}

    def set_offset(self, inc_offset):
        """Constraints the camera via maximum offsets to stop
        the player leaving the map boundary."""
        self.offset[0] += inc_offset[0]
        self.offset[1] += inc_offset[1]

        # North offset max
        if self.offset[1] + inc_offset[1] >= self.max_offsets['N']:
            self.offset[1] = self.max_offsets['N']

        # East offset max
        if self.offset[0] + inc_offset[0] <= self.max_offsets['E']:
            self.offset[0] = self.max_offsets['E']

        # South offset max
        if self.offset[1] + inc_offset[1] <= self.max_offsets['S']:
            self.offset[1] = self.max_offsets['S']

        # West offset max
        if self.offset[0] + inc_offset[0] >= self.max_offsets['W']:
            self.offset[0] = self.max_offsets['W']

    def calc_north_offset_max(self):
        return settings.SCREEN_RESOLUTION[1]/2

    def calc_east_offset_max(self):
        return -1.0*self.map_width * (settings.TILEWIDTH) + settings.SCREEN_RESOLUTION[0]/2

    def calc_south_offset_max(self):
        return -1.0*self.map_height * (settings.TILEHEIGHT) + settings.SCREEN_RESOLUTION[1]/2

    def calc_west_offset_max(self):
        return settings.SCREEN_RESOLUTION[0]/2
    
        

    
