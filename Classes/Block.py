from Classes.Propirties import Info


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        is_this_type = isinstance(other, Block)
        if is_this_type:
            return self.x == other.x and self.y == other.y
        return False

    def put_in_boundary(self):
        self.x += Info.blocks_amount
        self.x %= Info.blocks_amount
        self.y += Info.blocks_amount
        self.y %= Info.blocks_amount
