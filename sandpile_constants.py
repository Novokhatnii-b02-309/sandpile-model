WHITE = 'white'
GREEN = 'green'
PURPLE = 'purple'
YELLOW = 'yellow'
RED = 'red'
BLUE = 'blue'
CYAN = 'cyan'
MAGENTA = (255, 0, 255)
ORANGE = 'orange'
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

COLORFUL_CLAS = [GREEN, PURPLE, YELLOW, RED]
RED_CLAS = ['#FF9999', '#FF3333', '#CC0000', '#660000']
GREEN_CLAS = ['#99FF99', '#33FF33', '#00CC00', '#006600']
BLUE_CLAS = ['#9999FF', '#3333FF', '#0000CC', '#000066']

COLORFUL_NEUM = [GREEN, PURPLE, YELLOW, BLUE, CYAN, MAGENTA, ORANGE, RED]
RED_NEUM = ['#FF9999', '#FF6666', '#FF3333', '#FF0000', '#CC0000', '#990000', '#660000', '#330000']
GREEN_NEUM = ['#99FF99', '#66FF66', '#33FF33', '#00FF00', '#00CC00', '#009900', '#006600', '#003300']
BLUE_NEUM = ['#9999FF', '#6666FF', '#3333FF', '#0000FF', '#0000CC', '#000099', '#000066', '#000033']


# Словарь по ключам в виде типа рассыпания (1-classical, 2-neumann), и цвета выдаёт список цветов
COLOR_TYPES = {1: {'colorful': COLORFUL_CLAS, 'red': RED_CLAS, 'green': GREEN_CLAS, 'blue': BLUE_CLAS},
               2: {'colorful': COLORFUL_NEUM, 'red': RED_NEUM, 'green': GREEN_NEUM, 'blue': BLUE_NEUM}}


WIDTH = 100
HEIGHT = 100
SANDPILES = 30000
