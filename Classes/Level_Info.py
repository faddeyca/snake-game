class Info:
    """
    A class to represent the game information.

    ...

    Attributes
    ----------
    score : int
        Current score
    lives : int
        Lives left
    blocks_amount : int
        Amount of blocks in rows and columns in current map
    current_level: int
        Number of the last started level
    snake_blocks : Blocks array
        Snake's body and head array: (0) - tail, (-1) - head
    walls : Blocks array
        Walls positions
    lvl_req : int
        Required length of the snake to win this level
    d_x : int
        Snake's direction in row
    d_y : int
        Snake's direction in column
    speed : int
        Current snake's speed
    iteration : int
        Current iteration number - times "execute_iteration" called - number of current frame
    bonus_food_iteration : int
        Fixed number of iteration when bonus food was created
    deathless_iteration : int
        Fixed number of iteration when snake got damage
    cheatB : bool
        Is boundary cheat turned on
    cheatK : bool
        Is length and speed cheat turned on
    bonus_flag : bool
        Bonus food has been created
    apple : Food
        Main food
    bonus_food : Food
        Bonus food

    started_from_save : bool
        Is the game started from save
    pause : bool
        Is the game on pause
    """
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
    bonus_food_iteration = 0
    deathless_iteration = 0
    cheatsB = 0
    cheatsK = 0
    bonus_flag = 0
    apple = None
    bonus_food = None

    started_from_save = False
    pause = 1