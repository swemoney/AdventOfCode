# Day 6

START_OF_PACKET = 4
START_OF_MESSAGE = 14

def find_packet_in_buffer(data, packet_length):
    idx = 0
    while idx < len(data) - packet_length:
        testing = data[idx:idx+packet_length]
        if len(set(testing)) == len(testing):
            break
        idx += 1
    return idx + packet_length

def run_part_1(data):
    return find_packet_in_buffer(data, START_OF_PACKET)

def run_part_2(data):
    return find_packet_in_buffer(data, START_OF_MESSAGE)

def parse_input(data):
    return data[0]
