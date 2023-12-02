WHITE = 'white'
GREEN = 'green'
PURPLE = 'purple'
YELLOW = 'yellow'
RED = 'red'
BLUE = 'blue'
CYAN = 'cyan'
MAGENTA = (255, 0, 255)
ORANGE = 'orange'
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

COLORFUL_CLAS = [GREEN, PURPLE, YELLOW, RED]
RED_CLAS = [(32,0,0), (64,0,0), (128,0,0), (255,0,0)]
GREEN_CLAS = [(0,32,0), (0,64,0), (0,128,0), (0,255,0)]
BLUE_CLAS = [(0,0,32), (0,0,64), (0,0,128), (0,0,255)]

COLORFUL_NEUM = [GREEN, PURPLE, YELLOW, BLUE, CYAN, MAGENTA, ORANGE, RED]
RED_NEUM = [(16,0,0), (32,0,0), (48,0,0), (64,0,0), (96,0,0), (128,0,0), (192,0,0), (255,0,0)]
GREEN_NEUM = [(0,16,0), (0,32,0), (0,48,0), (0,64,0), (0,96,0), (0,128,0), (0,192,0), (0,255,0)]
BLUE_NEUM = [(0,0,16), (0,0,32), (0,0,48), (0,0,64), (0,0,96), (0,0,128), (0,0,192), (0,0,255)]

COLOR_TYPES = {1: {'colorful': COLORFUL_CLAS, 'red': RED_CLAS, 'green': GREEN_CLAS, 'blue': BLUE_CLAS},
               2: {'colorful': COLORFUL_NEUM, 'red': RED_NEUM, 'green': GREEN_NEUM, 'blue': BLUE_NEUM}}


WIDTH = 100
HEIGHT = 100
SANDPILES = 30000