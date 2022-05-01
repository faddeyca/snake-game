class Block:
    def __init__(self, x, y, blocks_amount):
        self.x = x
        self.y = y
        self.blocks_amount = blocks_amount

    def __eq__(self, other):
        return isinstance(other, Block) and self.x == other.x and self.y == other.y

    def put_in_boundary(self):
        self.x += self.blocks_amount
        self.x %= self.blocks_amount
        self.y += self.blocks_amount
        self.y %= self.blocks_amount