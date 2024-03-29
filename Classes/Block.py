from Classes.Level_Info import Info


class Block:
    """
    A class to represent a block

    ...

    Attributes
    ----------
    x : int
        position in row
    y : int
        position in column
    """
    def __init__(self, x, y):
        '''
        Initializes block
        '''
        self.x = x
        self.y = y

    def __eq__(self, other):
        '''
        Compares blocks
        '''
        is_this_type = isinstance(other, Block)
        if is_this_type:
            return self.x == other.x and self.y == other.y
        return False

    def put_in_boundary(self):
        '''
        Puts the block in field's boundary
        '''
        self.x += Info.blocks_amount
        self.x %= Info.blocks_amount
        self.y += Info.blocks_amount
        self.y %= Info.blocks_amount
