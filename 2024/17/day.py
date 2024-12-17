from collections import deque

# Day 17

def run_part_1(data):
    a, b, c, program = data
    a, b, c, outs = execute_program(program, a, b, c)
    return ",".join(map(str,outs))

def run_part_2(data):
    _, b, c, program = data
    return find_repeating(program, b, c)

def find_repeating(program, b, c):
    queue = deque()
    queue.append((0, 1))

    while queue:
        a, n = queue.popleft()
        if n > len(program): return a

        for i in range(8):
            shift_a = (a << 3) | i
            _, _, _, out = execute_program(program, shift_a, b, c)
            target = program[-n:]

            if out == target:
                queue.append((shift_a, n + 1))
    
    return False

def execute_program(program, a, b, c):
    ptr, outs = 0, []
    while ptr < len(program):

        opcode, operand = program[ptr:ptr+2]
        val = combo_operand(operand, a, b, c) if opcode in [0,2,5,6,7] else operand
        match opcode:
            case 0: # adv, combo: A / 2**op -> A
                a = a // (2**val)

            case 1: # bxl, literal: B xor op -> B
                b = b ^ val

            case 2: # bst, combo: op % 8 -> B
                b = val % 8
            
            case 3: # jnz, literal: jump to ptr + op if A != 0
                ptr = ptr + 2 if a == 0 else val

            case 4: # bxc, literal: B xor C -> B
                b = b ^ c

            case 5: # out, combo: op % 8 -> out
                outs.append(val % 8)

            case 6: # bdv, combo: A / 2^op -> B
                b = a // (2**val)

            case 7: # cbv, combo: A / 2^op -> C
                c = a // (2**val)

        if opcode != 3: ptr += 2

    return a, b, c, outs

def combo_operand(operand, a, b, c):
    if operand in [0,1,2,3]: return operand
    if operand == 4: return a
    if operand == 5: return b
    if operand == 6: return c

def parse_input(data) -> tuple[int, int, int, list[int]]: # register A, register B, register C, program
    return (
        int(data[0].split(": ")[1]),
        int(data[1].split(": ")[1]),
        int(data[2].split(": ")[1]),
        list(map(int, data[4].split(": ")[1].split(",")))
    )
