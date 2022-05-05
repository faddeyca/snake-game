from Classes.Game import *
from Classes.Block import *
from Classes.Level_Info import Info


def start_level_1(started_from_save):
    '''
    Starts the level with specific parameters: Amount of blocks in row and columns, snake coords, walls coords, win level requirment.
    All further functions in this files do the same.
    '''
    if not started_from_save:
        Info.d_x = 0
        Info.d_y = 0
        Info.speed = 1
        Info.current_level = 1
        Info.blocks_amount = 10
        Info.snake_blocks = [Block(5, 5), Block(5, 6)]
        Info.walls = []
        Info.lvl_req = 15

    game = Game()

    res = game.start()
    return res


def start_level_2(started_from_save):
    if not started_from_save:
        Info.d_x = 0
        Info.d_y = 0
        Info.speed = 1
        Info.current_level = 2
        Info.blocks_amount = 20
        Info.snake_blocks = [Block(9, 9), Block(9, 10)]
        Info.walls = [Block(1, 1),
                Block(1, 2),
                Block(1, 3),
                Block(2, 1),
                Block(3, 1),
                Block(18, 1),
                Block(18, 2),
                Block(18, 3),
                Block(17, 1),
                Block(16, 1),
                Block(18, 18),
                Block(18, 17),
                Block(18, 16),
                Block(17, 18),
                Block(16, 18),
                Block(1, 18),
                Block(1, 17),
                Block(1, 16),
                Block(2, 18),
                Block(3, 18)]
        Info.lvl_req = 15

    game = Game()

    res = game.start()
    return res


def start_level_3(started_from_save):
    if not started_from_save:
        Info.d_x = 0
        Info.d_y = 0
        Info.speed = 1
        Info.current_level = 3
        Info.blocks_amount = 20
        Info.snake_blocks = [Block(9, 14), Block(9, 15)]
        Info.walls = [Block(1, 1),
                Block(1, 2),
                Block(2, 1),
                Block(18, 1),
                Block(18, 2),
                Block(17, 1),
                Block(18, 18),
                Block(18, 17),
                Block(17, 18),
                Block(1, 18),
                Block(1, 17),
                Block(2, 18),
                Block(2, 2),
                Block(3, 3),
                Block(4, 4),
                Block(5, 5),
                Block(6, 6),
                Block(7, 7),
                Block(8, 8),
                Block(11, 11),
                Block(12, 12),
                Block(13, 13),
                Block(14, 14),
                Block(15, 15),
                Block(16, 16),
                Block(17, 17),
                Block(2, 17),
                Block(3, 16),
                Block(4, 15),
                Block(5, 14),
                Block(6, 13),
                Block(7, 12),
                Block(8, 11),
                Block(11, 8),
                Block(12, 7),
                Block(13, 6),
                Block(14, 5),
                Block(15, 4),
                Block(16, 3),
                Block(17, 2)]
        Info.lvl_req = 15

    game = Game()

    res = game.start()
    return res
