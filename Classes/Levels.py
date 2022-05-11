from Classes.Game import *
from Classes.Block import *
from Classes.Level_Info import Info


class Level():
    """
    A class to represent a level

    ...

    Attributes
    ----------
    Same to Info
    

    Methods
    -------
    start():
        Sets level properties and init game
    clean():
        Drops old properties
    """
    def __init__(self, current_level, blocks_amount, snake_blocks, lvl_req, map):
        self.current_level = current_level
        self.blocks_amount = blocks_amount
        self.snake_blocks = snake_blocks
        self.lvl_req = lvl_req
        self.walls = []
        for i in range(len(map)):
            if map[i] == "1":
                self.walls.append(Block(i // self.blocks_amount, i % self.blocks_amount))
    

    def start(self):
        '''
        Sets level properties and init game
        '''
        if not Info.started_from_save:
            self.clean()
            Info.current_level = self.current_level
            Info.blocks_amount = self.blocks_amount
            Info.snake_blocks = self.snake_blocks.copy()
            Info.lvl_req = self.lvl_req
            Info.walls = self.walls
        game = Game()
        return game.start()

    def clean(self):
        '''
        Drops old properties
        '''
        Info.bonus_flag = 0
        Info.cheatsB = 0
        Info.cheatsK = 0
        Info.d_x = 0
        Info.d_y = 0
        Info.speed = 1
        Info.iteration = 0
        Info.bonus_food_iteration = 0
        Info.deathless_iteration = 0


def init_level_1():
    '''
    Starts the level with specific parameters.
    All further functions in this files do the same.
    '''
    current_level = 1
    blocks_amount = 10
    snake_blocks = [Block(5, 5), Block(5, 6)]
    lvl_req = 5
    map = "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"
    
    return Level(current_level, blocks_amount, snake_blocks, lvl_req, map)


def init_level_2():
    current_level = 2
    blocks_amount = 20
    snake_blocks = [Block(9, 9), Block(9, 10)]
    lvl_req = 10
    map = "00000000000000000000"\
          "00000000000000000000"\
          "00000000000000000000"\
          "00011110000001111000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00011111111111111000"\
          "00000000000000000000"\
          "00000000000000000000"

    return Level(current_level, blocks_amount, snake_blocks, lvl_req, map)


def init_level_3():
    current_level = 3
    blocks_amount = 20
    snake_blocks = [Block(8, 9), Block(8, 10)]
    lvl_req = 20
    map = "00000000000000000000"\
          "00000000000000000000"\
          "00000000000000000000"\
          "00011111110111111000"\
          "00010000010100001000"\
          "00010010010100001000"\
          "00010010010100001000"\
          "00010010010100001000"\
          "00010010000100001000"\
          "00010011111100001000"\
          "00010000000000001000"\
          "00011100000000001000"\
          "00010010000000001000"\
          "00010001000000001000"\
          "00010000100000001000"\
          "00010000000000001000"\
          "00010000000000001000"\
          "00011111111111111000"\
          "00000000000000000000"\
          "00000000000000000000"

    return Level(current_level, blocks_amount, snake_blocks, lvl_req, map)
