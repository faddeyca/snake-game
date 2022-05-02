from Classes.Game import *
from Classes.Block import *


def start_level_1(screen, size):
    snake_blocks = [Block(5, 5), Block(5, 6)]
    walls = []
    lvl_req = 4
    d_x = 0
    d_y = 1

    game = Game(screen, size, snake_blocks, walls, lvl_req, d_x, d_y)

    res = game.start()
    return res


def start_level_2(screen, size):
    snake_blocks = [Block(5, 5), Block(5, 6)]
    walls = [Block(1, 1),
             Block(1, 8),
             Block(8, 1),
             Block(8, 8)]
    lvl_req = 5
    d_x = 0
    d_y = 1
    game = Game(screen, size, snake_blocks, walls, lvl_req, d_x, d_y)
    
    res = game.start()
    return res


def start_level_3(screen, size):
    snake_blocks = [Block(5, 5), Block(5, 6)]
    walls = []
    lvl_req = 5
    d_x = 0
    d_y = 1
    game = Game(screen, size, snake_blocks, walls, lvl_req, d_x, d_y)
    
    res = game.start()
    return res
