# Day 7

from functools import reduce

TARGET_SIZE = 100000
TOTAL_SIZE = 70000000
NEEDED_FOR_UPDATE = 30000000

def run_part_1(data):
    path_sizes = get_size_of_all_directories(data)
    return sum(size for size in path_sizes if size < TARGET_SIZE)

def run_part_2(data):
    path_sizes = get_size_of_all_directories(data)
    currently_free = TOTAL_SIZE - path_sizes[-1] # Last item should be root
    space_required = NEEDED_FOR_UPDATE - currently_free
    return min(size for size in path_sizes if size > space_required)

def get_size_of_all_directories(data):
    path_sizes = []
    size_of_items_at_path(data, "/", path_sizes)
    return path_sizes

def size_of_items_at_path(data, path, path_sizes = None):
    if type(data) == int: return data
    size = 0
    for item in data:
        size += size_of_items_at_path(data[item], item, path_sizes)
    if path_sizes != None:
        path_sizes.append(size)
    return size

def parse_input(data):
    filesystem = {"/":{}}
    breadcrumbs = []
    for line in data:
        if line[0] == "$":
            parse_command(line[2:], filesystem, breadcrumbs)
        else:
            parse_output(line, filesystem, breadcrumbs)
    return filesystem["/"]

# Parse the command
def parse_command(cmd, filesystem, breadcrumbs):
    if cmd == "ls": return
    args = cmd.split(" ")[1]
    if args == "..":
        breadcrumbs.pop()
    else:
        if get_by_path(filesystem, breadcrumbs).get(args) == None:
            set_by_path(filesystem, breadcrumbs, args, {})
        breadcrumbs.append(args)

# Parse the output of whatever command was sent
def parse_output(data, filesystem, breadcrumbs):
    flags, filename = data.split(" ")
    if flags == "dir": return
    set_by_path(filesystem, breadcrumbs, filename, int(flags))

# get the nested value from a dictionary by passing a list of keys
def get_by_path(root, items):
    return reduce(lambda a,b: a.get(b,{}), items, root)

# Set a value to a key in a nested dictionary by passing a list of keys
def set_by_path(root, items, key, value):
    get_by_path(root, items[:-1])[items[-1]][key] = value
