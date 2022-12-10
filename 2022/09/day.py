# Day 9

MOVE = {"U": (1,0), "D": (-1,0), "R": (0,1), "L": (0,-1)}

class Knot:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def distance_from(self, knot):
        return max(abs(self.x - knot.x), abs(self.y - knot.y))

    def move(self, direction):
        self.y += MOVE[direction][0]
        self.x += MOVE[direction][1]

    def move_towards(self, knot):
        if self.distance_from(knot) > 1:
            if self.x == knot.x:
                self.move("U") if knot.y > self.y else self.move("D")
            elif self.y == knot.y:
                self.move("R") if knot.x > self.x else self.move("L")
            else:
                self.move("U") if knot.y > self.y else self.move("D")
                self.move("R") if knot.x > self.x else self.move("L")

def run_part_1(data):
    head = Knot(0, 0)
    tail = Knot(0, 0)
    locations = [(tail.y, tail.x)]
    for instruction in data:
        for i in range(instruction.spaces):
            head.move(instruction.direction)
            tail.move_towards(head)
            locations.append((tail.y, tail.x))
    return len(set(locations))

def run_part_2(data):
    knots = [Knot(0, 0) for _ in range(10)]
    locations = [(knots[-1].y, knots[-1].x)]
    for instruction in data:
        for i in range(instruction.spaces):
            knots[0].move(instruction.direction)
            for i, tail in enumerate(knots):
                if i == 0: continue
                tail.move_towards(knots[i-1])
            locations.append((knots[-1].y, knots[-1].x))
    return len(set(locations))


from dataclasses import dataclass

@dataclass
class Instruction:
    direction: str
    spaces: int    

def parse_input(data):
    return [Instruction(line.split(" ")[0], int(line.split(" ")[1])) for line in data]
