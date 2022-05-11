from Classes.Food import FoodType


class Info:
    score = 0
    lives = 3
    blocks_amount = None
    current_level = None
    snake_blocks = []
    walls = []
    lvl_req = None
    d_x = 0
    d_y = 0
    speed = 1
    iteration = 0
    fixed_iteration = 0
    deathless_iteration = 0
    cheatsB = 0
    cheatsK = 0
    bonus_flag = 0
    apple = None
    bonus_food = None

    started_from_save = False
    pause = 1