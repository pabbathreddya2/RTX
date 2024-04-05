class Node:

    def __init__(self, id, weight=float('inf'), name="", degree=0):
        self.id = id
        self.weight = weight
        self.name = name
        self.degree = degree

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __str__(self):
        return self.id

    def __hash__(self):
        return hash(self.id)
