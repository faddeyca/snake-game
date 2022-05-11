from Classes.Level_Info import *


from Classes.Block import *


def test_init_block():
    x = 3
    y = 5
    block = Block(x, y)
    assert block.x == x and block.y == y

def test_eq_block():
    block1 = Block(0, 0)
    block2 = Block(0, 0)
    assert block1 == block2

def test_not_eq_block():
    block1 = Block(0, 0)
    block2 = Block(1, 1)
    assert block1 != block2

def test_put_in_boundary_block():
    Info.blocks_amount = 5
    block = Block(5, 5)
    block.put_in_boundary()
    assert block.x == 0 and block.y == 0


from Classes.Food import *


def test_init_food():
    type = FoodType.scoreUp
    pos = Block(1, 1)
    food = Food(pos, type)
    assert food.block == pos and food.type == type  

def test_eq_food():
    food1 = Food(Block(1, 5), FoodType.lengthUp)
    food2 = Food(Block(1, 5), FoodType.lengthUp)
    assert food1 == food2

def test_not_eq_food():
    food1 = Food(Block(1, 5), FoodType.lengthUp)
    food2 = Food(Block(5, 1), FoodType.lengthUp)
    assert food1 != food2

def test_enum_to_int_food():
    type = FoodType.scoreUp
    number = enum_to_int(type)
    assert number == 2   

def test_int_to_enum_food():
    number = 1
    type = int_to_enum(number)
    assert type == FoodType.speedUp


from Classes.Saver import *


def test_saver():
    current_level = 1
    score = 2
    lives = 3
    blocks_amount = 25
    lvl_req = 5
    d_x = 1
    d_y = -1
    speed = 6
    iteration = 7
    fixed_iteration = 8
    deathless_iteration = 9
    bonus_flag = 1
    cheatsB = 0
    cheatsK = 1
    apple = Food(Block(1, 5), FoodType.speedUp)
    bonus_food = Food(Block(2, 4), FoodType.scoreUp)
    snake_blocks = [Block(0, 1), Block(0, 2)]
    walls = [Block(4, 4)]

    Info.current_level = current_level
    Info.score = score
    Info.lives = lives
    Info.blocks_amount = blocks_amount
    Info.lvl_req = lvl_req
    Info.d_x = d_x
    Info.d_y = d_y
    Info.speed = speed
    Info.iteration = iteration
    Info.bonus_food_iteration = fixed_iteration
    Info.deathless_iteration = deathless_iteration
    Info.bonus_flag = bonus_flag
    Info.cheatsB = cheatsB
    Info.cheatsK = cheatsK
    Info.apple = apple
    Info.bonus_food = bonus_food
    Info.snake_blocks = snake_blocks
    Info.walls = walls

    save()

    load_save()

    assert Info.current_level == current_level
    assert Info.score == score
    assert Info.lives == lives
    assert Info.blocks_amount == blocks_amount
    assert Info.lvl_req == lvl_req
    assert Info.d_x == d_x
    assert Info.d_y == d_y
    assert Info.speed == speed
    assert Info.iteration == iteration
    assert Info.bonus_food_iteration == fixed_iteration
    assert Info.deathless_iteration == deathless_iteration
    assert Info.bonus_flag == bonus_flag
    assert Info.cheatsB == cheatsB
    assert Info.cheatsK == cheatsK
    assert Info.apple == apple
    assert Info.bonus_food == bonus_food
    assert Info.snake_blocks == snake_blocks
    assert Info.walls == walls


from Classes.Levels import *


def test_level_init():
    current_level = 1
    blocks_amount = 10
    snake_blocks = [Block(5, 5), Block(5, 6)]
    lvl_req = 5
    map = "1000000001"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "0000000000"\
          "1000000001"
    
    level = Level(current_level, blocks_amount, snake_blocks, lvl_req, map)

    assert level.current_level == current_level
    assert level.blocks_amount == blocks_amount
    assert level.snake_blocks == snake_blocks
    assert level.lvl_req == lvl_req

    check = True
    walls = [Block(0, 0), Block(0, 9), Block(9, 0), Block(9, 9)]

    for block in walls:
        if not block in level.walls:
            check = False

    for block in level.walls:
        if not block in walls:
            check = False

    assert check


from Classes.Game import *

def test_init_game():
    Info.blocks_amount = 10
    game = Game()
    assert game.size[0] == 310 and game.size[1] == 410

def test_move_up():
    Info.pause = 1
    game = Game()
    game.Move_up()
    assert Info.d_x == -1 and Info.d_y == 0

def test_move_down():
    Info.pause = 1
    game = Game()
    game.Move_down()
    assert Info.d_x == 1 and Info.d_y == 0

def test_move_right():
    Info.pause = 1
    game = Game()
    game.Move_right()
    assert Info.d_x == 0 and Info.d_y == 1

def test_move_left():
    Info.pause = 1
    game = Game()
    game.Move_left()
    assert Info.d_x == 0 and Info.d_y == -1

def test_start():
    Info.lvl_req = -1
    game = Game()
    res = game.start()
    assert res == 1

def test_execute_iteration_win():
    Info.lvl_req = -1
    game = Game()
    res = game.Execute_iteration()
    assert res == 1

def test_execute_iteration_defeat():
    Info.lives = 0
    game = Game()
    res = game.Execute_iteration()
    assert res == 0

def test_execute_iteration_defeat():
    Info.lives = 3
    Info.lvl_req = 10
    game = Game()
    res = game.Execute_iteration()
    assert res == -1

def test_get_damage():
    Info.iteration = 10
    Info.deathless_iteration = 0
    Info.lives = 1
    game = Game()
    game.get_damage()
    assert Info.lives == 0

def test_not_get_damage():
    Info.iteration = 3
    Info.deathless_iteration = 0
    Info.lives = 1
    game = Game()
    game.get_damage()
    assert Info.lives == 1

def test_eat_food_lengthUp():
    Info.score = 0
    Info.apple = Food(Block(0, 0), FoodType.lengthUp)
    game = Game()
    flag = game.eat_food()
    assert flag == 0
    assert Info.score == 1

def test_end_iteration_processing():
    Info.lvl_req = -1
    game = Game()
    res = game.end_iteration_processing()
    assert res == 1