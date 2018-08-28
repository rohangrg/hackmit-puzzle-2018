'''

Constants and functions used in the puzzle generator.

'''

# Directory where generated puzzles are stored
DIR = 'graphs'

# File name for directed puzzles
FILE = 'graph'

# Width of generated graph
WIDTH = 150

# Height of generated graph
HEIGHT = 150

# File name generator
def filename(num):
    return FILE + '.' + f'{num:03}' + '.json'
