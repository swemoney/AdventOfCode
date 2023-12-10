# Day 10

P_VERT = "|"
P_HORZ = "-"
P_NE   = "L"
P_NW   = "J"
P_SW   = "7"
P_SE   = "F"
GROUND = "."
START  = "S"

N = (-1, 0)
E =  (0, 1)
S = (1, 0)
W =  (0, -1)

VALID_PIPES = {
    P_VERT: {N: [START, P_VERT, P_SW, P_SE], S: [START, P_VERT, P_NW, P_NE]},
    P_HORZ: {E: [START, P_HORZ, P_NW, P_SW], W: [START, P_HORZ, P_SE, P_NE]},
    P_NE:   {N: [START, P_VERT, P_SW, P_SE], E: [START, P_HORZ, P_NW, P_SW]},
    P_NW:   {N: [START, P_VERT, P_SW, P_SE], W: [START, P_HORZ, P_NE, P_SE]},
    P_SW:   {S: [START, P_VERT, P_NE, P_NW], W: [START, P_HORZ, P_NE, P_SE]},
    P_SE:   {E: [START, P_HORZ, P_NW, P_SW], S: [START, P_VERT, P_NE, P_NW]},
    START:  {N: [P_VERT, P_SW, P_SE], E: [P_HORZ, P_NW, P_SW], S: [P_VERT, P_NE, P_NW], W: [P_HORZ, P_NE, P_SE]},
    GROUND: {}
}

START_PIPES = {
    (N,S): P_VERT, (S,N): P_VERT,
    (E,W): P_HORZ, (W,E): P_HORZ,
    (N,E): P_NE, (E,N): P_NE,
    (N,W): P_NW, (W,N): P_NW,
    (S,W): P_SW, (W,S): P_SW,
    (S,E): P_SE, (E,S): P_SE}

class PipeMaze:
    maze: [str]

    def __init__(self, maze: [[str]]):
        self.maze = maze
        self.find_start()
        self.traverse_pipe()

    def traverse_pipe(self):
        prev_positions = [self.start, self.start]
        curr_positions = self.find_connecting_neighbors(self.start)
        self.add_to_pipe(curr_positions)
        steps = 1
        while True:
            for i, coord in enumerate(curr_positions):
                neighbors = self.find_connecting_neighbors(coord)
                neighbors.remove(prev_positions[i])
                self.add_to_pipe(neighbors)
                prev_positions[i] = curr_positions[i]
                curr_positions[i] = neighbors[0]
            steps += 1
            if curr_positions[0] == curr_positions[1]:
                break
        self.furthest_pipe_segment = steps

    def add_to_pipe(self, coords):
        for coord in coords:
            self.pipe[coord] = self.pipe_at(coord)

    def pos_out_of_bounds(self, pos):
        return pos[0] < 0 or pos[1] < 0 or pos[0] >= len(self.maze) or pos[1] >= len(self.maze[0])
    
    def pipe_at(self, coords: (int,int)):
        return self.maze[coords[0]][coords[1]]

    def find_start(self):
        for y, row in enumerate(self.maze):
            if START in row:
                x = row.index(START)
                self.start = (y, x)
                self.pipe = {self.start: START}
                break

    def find_connecting_neighbors(self, pos):
        connecting = []
        current_pipe = self.pipe_at(pos)
        for y, x in VALID_PIPES[current_pipe].keys():
            next_coords = (pos[0]+y, pos[1]+x)
            if self.pos_out_of_bounds(next_coords):
                continue
            next_pipe = self.pipe_at(next_coords)
            if next_pipe in VALID_PIPES[current_pipe][(y, x)]:
                connecting.append(next_coords)
        return connecting
    
    def replace_start(self):
        neighbors = self.find_connecting_neighbors(self.start)
        directions = (
            (neighbors[0][0] - self.start[0], neighbors[0][1] - self.start[1]),
            (neighbors[1][0] - self.start[0], neighbors[1][1] - self.start[1]))
        self.maze[self.start[0]][self.start[1]] = START_PIPES[directions]
    
    def fill_non_loop(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if not (y, x) in self.pipe:
                    self.maze[y][x] = GROUND

    def flood_fill(self):
        self.insides = 0
        for y, row in enumerate(self.maze):
            inside = False
            for x, col in enumerate(row):
                if col == P_VERT or col == P_NW or col == P_NE:
                    inside = not inside
                elif col == GROUND and inside:
                    self.maze[y][x] = "I"
                    self.insides += 1
        return self.insides


def run_part_1(data):
    maze = PipeMaze(data)
    return maze.furthest_pipe_segment

def run_part_2(data):
    maze = PipeMaze(data)
    maze.replace_start()
    maze.fill_non_loop()
    return maze.flood_fill()

def parse_input(data):
    return [list(line) for line in data]
