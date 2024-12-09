# Day 9

EMPTY = "."

# Brute force. Not quick. Still works.
def run_part_1(data):
    defragged = defrag_blocks(data)
    return calculate_checksum(defragged)

def run_part_2(data):
    defragged = defrag_files(data)
    return calculate_checksum(defragged)

def defrag_blocks(fs):
    i = len(fs) - 1
    while EMPTY in fs:
        if fs[i] != EMPTY: fs[fs.index(EMPTY)] = fs[i]
        del(fs[i])
        i -= 1
    return fs

def defrag_files(fs):
    i = len(fs) - 1
    while i >= 0:
        if fs[i] == EMPTY:
            i -= 1
            continue
        first = fs.index(fs[i])
        size = i - first + 1
        space_for_file = find_empty_space(fs, size)
        if space_for_file > -1 and space_for_file < first:
            file_id = fs[i]
            for j in range(size):
                fs[space_for_file + j] = file_id
                fs[i-j] = EMPTY
        i -= size
    return fs

def calculate_checksum(fs):
    return sum([i * id for i, id in enumerate(fs) if id != EMPTY])

def find_empty_space(fs, size):
    for i in range(len(fs) - size + 1):
        if all(fs[i + j] == EMPTY for j in range(size)):
            return i
    return -1

def parse_input(data):
    filesystem = []
    for i, n in enumerate(list(map(int, list(data[0])))):
        if i%2 == 0: # file block
            filesystem.extend([i//2]*n)
        else:
            filesystem.extend(["."]*n)
    return filesystem
