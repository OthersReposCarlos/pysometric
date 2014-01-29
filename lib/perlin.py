import random


class PerlinNoiseMap(object):
    """Stores the Perlin Noise map from which to sample."""
    
    def __init__(self, size, tiledim, tilew, tileh):
        print "PNM: size, tiledim, tilew, tileh: %s, %s, %s, %s" % (size, tiledim, tilew, tileh)
        self.p = []
        self.map = []
        self.sample_map = []
        self.tilekey_map = []
        
        self.size = size
        self.tiledim = tiledim
        self.tilew = tilew
        self.tileh = tileh

        self._prepare_p()
        self._randomise_p()
        self._prepare_map()

    def _prepare_p(self):
        for x in xrange(2*self.tiledim):
            self.p.append(0)

    def _randomise_p(self):
        permutation = []
        for value in xrange(self.tiledim):
            permutation.append(value)
        random.shuffle(permutation)

        for i in xrange(self.tiledim):
            self.p[i] = permutation[i]
            self.p[self.tiledim+i] = self.p[i]

    def _prepare_map(self):
        for x in xrange(self.size):
            y_map = []
            for y in xrange(self.size):
                y_map.append(0.0)
            self.map.append(y_map)
            
    def create_sample_map(self):
        sample_x = int(self.size/self.tilew)
        sample_y = int(self.size/self.tileh)

        for x in xrange(self.tilew):
            y_map = []
            for y in xrange(self.tileh):
                sample = self.map[x*sample_x][y*sample_y]                

                if sample < 0.4:
                    y_map.append(1)
                elif sample >= 0.4 and sample < 0.45:
                    y_map.append(1)
                elif sample >= 0.45 and sample < 0.5:
                    y_map.append(1)
                elif sample >= 0.5 and sample < 0.55:
                    y_map.append(2)
                elif sample >= 0.55 and sample < 0.6:
                    y_map.append(2)
                else:
                    y_map.append(2)
            self.sample_map.append(y_map)

    def _determine_tile_type(self, x, y, tile_dir):
        if x == 0 or y == 0 or x == len(self.sample_map)-1 or y == len(self.sample_map[x])-1:
            return 0
        else:
            if tile_dir == 'NW': return self.sample_map[x-1+y%2][y-1]
            if tile_dir == 'NE': return self.sample_map[x+y%2][y-1]
            if tile_dir == 'SE': return self.sample_map[x+y%2][y+1]
            if tile_dir == 'SW': return self.sample_map[x-1+y%2][y+1]

    def create_tilekey_map(self):
        for x in xrange(self.tilew):
            y_map = []
            for y in xrange(self.tileh):
                tile_key = ''
                if self.sample_map[x][y] == 0:
                    tile_key += 'OCEAN_'
                    
                    tile_NW = self._determine_tile_type(x, y, 'NW')
                    tile_NE = self._determine_tile_type(x, y, 'NE')
                    tile_SE = self._determine_tile_type(x, y, 'SE')
                    tile_SW = self._determine_tile_type(x, y, 'SW')
                    tile_list = [tile_NW, tile_NE, tile_SE, tile_SW]

                    tile_code = ''
                    for i, t in enumerate(tile_list):
                        if t > 0:
                            tile_code += '%s' % str(i+1)
                    if tile_code == '':
                        tile_key += 'NONE_1'
                    else:
                        tile_key += 'BANK_%s' % tile_code
                else:
                    tile_key = 'GRASS_NONE_1'

                y_map.append(tile_key)
            self.tilekey_map.append(y_map)

    
class PerlinNoiseFactory(object):
    """Creates a PerlinNoiseMap object."""

    def __init__(self, size, tiledim, repeats):
        print "PNF: size, tiledim, repeats: %s, %s, %s" % (size, tiledim, repeats)

        self.size = size
        self.tiledim = tiledim   #In nodes
        self.repeats = repeats    #number of repetitions on screen

        self.tilesize = float(self.size)/self.repeats
        self.tilesize /= self.tiledim

    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, t, a, b):
        return a + t * (b - a)
    
    def _grad(self, hash, x, y, z):
        """Convert LO 4 bits of hash code into 12 gradient directions."""
        h = hash & 15

        if h < 8:
            u = x
        else:
            u = y

        if h < 4:
            v = y
        else:
            if h == 12 or h == 14:
                v = x
            else:
                v = z

        if h&1 == 0:
            first = u
        else:
            first = -u

        if h&2 == 0:
            second = v
        else:
            second = -v

        return first + second

    def _noise(self, x, y, z, p):
        # Find unit cube that contains point.
        X = int(x)&(self.tiledim-1)
        Y = int(y)&(self.tiledim-1)
        Z = int(z)&(self.tiledim-1)
        
        # Find relative x,y,z of point in cube.
        x -= int(x)
        y -= int(y)
        z -= int(z)

        # Compute fade curves for each of x,y,z.
        u = self._fade(x)
        v = self._fade(y)
        w = self._fade(z)

        # Hash coordinates of the 8 cube corners.
        A = p[X  ]+Y; AA = p[A]+Z; AB = p[A+1]+Z
        B = p[X+1]+Y; BA = p[B]+Z; BB = p[B+1]+Z
    
        # And add blended results from 8 corners of cube
        return self._lerp(w,
                          self._lerp(v,
                                     self._lerp(u,self._grad(p[AA  ],x  ,y  ,z  ),
                                                self._grad(p[BA  ],x-1,y  ,z  )),
                                     self._lerp(u,self._grad(p[AB  ],x  ,y-1,z  ),
                                                self._grad(p[BB  ],x-1,y-1,z  ))),
                          self._lerp(v,
                                     self._lerp(u,self._grad(p[AA+1],x  ,y  ,z-1),
                                                self._grad(p[BA+1],x-1,y  ,z-1)),
                                     self._lerp(u,self._grad(p[AB+1],x  ,y-1,z-1),
                                                self._grad(p[BB+1],x-1,y-1,z-1))))    

    def _generate_map(self):
        pnm = PerlinNoiseMap(self.size, self.tiledim, self.size, self.size)

        octaves = 8
        persistence = 0.8
        
        amplitude = 1.0
        maxamplitude = 1.0
        for octave in xrange(octaves):
            amplitude *= persistence
            maxamplitude += amplitude
            
        for x in xrange(self.size):
            for y in xrange(self.size):
                sc = float(self.size)/self.tilesize
                frequency = 1.0
                amplitude = 1.0
                color = 0.0
                for octave in xrange(octaves):
                    sc *= frequency
                    grey = self._noise(sc*float(x)/self.size,
                                       sc*float(y)/self.size,
                                       0.0,
                                       pnm.p)
                    grey = (grey+1.0)/2.0
                    grey *= amplitude
                    color += grey
                    frequency *= 2.0
                    amplitude *= persistence
                color /= maxamplitude
                pnm.map[x][y] = color
        
        pnm.create_sample_map()
        pnm.create_tilekey_map()

        return pnm
