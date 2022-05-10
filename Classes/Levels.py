from Classes.Game import *
from Classes.Block import *
from Classes.Level_Info import Info


def start_level_1():
    '''
    Starts the level with specific parameters: Amount of blocks in row and columns, snake coords, walls coords, win level requirment.
    All further functions in this files do the same.
    '''
    if not Info.started_from_save:
        to_zero()
        Info.current_level = 1
        Info.blocks_amount = 10
        Info.snake_blocks = [Block(5, 5), Block(5, 6)]
        Info.walls = []
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
        for i in range(len(map)):
            if map[i] == "1":
                Info.walls.append(Block(i // Info.blocks_amount, i % Info.blocks_amount))
        Info.lvl_req = 5

    game = Game()

    res = game.start()
    return res


def start_level_2():
    if not Info.started_from_save:
        to_zero()
        Info.current_level = 2
        Info.blocks_amount = 20
        Info.snake_blocks = [Block(9, 9), Block(9, 10)]
        Info.walls = []
        map = "10000000000000000000"\
              "01000000000000000000"\
              "00100000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00010000000000000000"\
              "00000000000000000000"\
              "00000000000000000000"
        for i in range(len(map)):
            if map[i] == "1":
                Info.walls.append(Block(i // Info.blocks_amount, i % Info.blocks_amount))

        Info.lvl_req = 15

    game = Game()

    res = game.start()
    return res


def start_level_3():
    if not Info.started_from_save:
        to_zero()
        Info.current_level = 3
        Info.blocks_amount = 20
        Info.snake_blocks = [Block(9, 14), Block(9, 15)]
        Info.walls = []
        map = "00000000000000000000"\
              "00000000000000000000"\
              "00111110000001111100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00100000000000000100"\
              "00111111111111111100"\
              "00000000000000000000"\
              "00000000000000000000"
        for i in range(len(map)):
            if map[i] == "1":
                Info.walls.append(Block(i // Info.blocks_amount, i % Info.blocks_amount))
        Info.lvl_req = 15

    game = Game()

    res = game.start()
    return res


def to_zero():
    Info.bonus_flag = 0
    Info.cheatsB = 0
    Info.cheatsK = 0
    Info.d_x = 0
    Info.d_y = 0
    Info.speed = 1
    Info.iteration = 0
    Info.fixed_iteration = 0
    Info.deathless_iteration = 0
