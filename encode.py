import os
import sys
import math
import numpy
import struct
import cv2

import utils

video_resolution = (1920,1080)
input_file = "./input/input.tar.gz"
output_file = "./output/output.mp4"
bit_power = 4

steps_list = []
sequences = utils.generate_bit_combinations(bit_power)

if (not os.path.exists(input_file)):
    print(f"[FAIL] {input_file} does not exist!")
    sys.exit(1)

if (os.path.exists(output_file)):
    print(f"[FAIL] {output_file} already exists!")
    sys.exit(1)

for step in range(2 ** bit_power):
    steps_list.append(numpy.uint8(255 / (2 ** bit_power - 1) * step))

print(f"[INFO] Encoding from {input_file} to {output_file}.")

video_write = cv2.VideoWriter(output_file,cv2.VideoWriter_fourcc(*"mp4v"),5,video_resolution,False)

data_frame = None
next_x = 0
next_y = 0
def write_sequence(sequence):
    global data_frame
    global next_x
    global next_y
    if (next_x >= video_resolution[0]):
        next_x = 0
        next_y = (next_y + 1)
    if ((next_y >= video_resolution[1]) or (not isinstance(data_frame,numpy.ndarray))):
        if (isinstance(data_frame,numpy.ndarray)):
            video_write.write(data_frame)
        data_frame = numpy.zeros(tuple(reversed(video_resolution)),numpy.uint8)
        next_x = 0
        next_y = 0
    
    sequence_index = 0
    for possible_sequence in sequences:
        if (possible_sequence == sequence):
            break
        sequence_index = (sequence_index + 1)
    
    data_frame[next_y,next_x] = steps_list[sequence_index]
    next_x = (next_x + 1)

def write_data(data):
    global next_x
    global next_y
    global data_frame

    debug_last = None
    debug_index = 0
    debug_len = len(data)
    for current_byte in data:
        debug_pos = (debug_index / debug_len)
        debug_index = (debug_index + 1)
        if ((not debug_last) or ((debug_pos - debug_last) >= 0.01)):
            print(f"[INFO] Progress: {str(round(debug_pos * 100))}%")
            debug_last = debug_pos

        byte_sequence = ""
        for bit_index in range(8):
            if ((current_byte >> (bit_index + 1)) & 0x01):
                byte_sequence = (byte_sequence + "1")
            else:
                byte_sequence = (byte_sequence + "0")
        for split_sequence in range(math.ceil(8 / bit_power)):
            current_sequence = byte_sequence[(bit_power * split_sequence):(bit_power * split_sequence + bit_power)]
            if (len(current_sequence) < bit_power):
                print("[FAIL] bit_power not valid.")
                raise Exception
            write_sequence(current_sequence)
    video_write.write(data_frame)
    next_x = 0
    next_y = 0
    data_frame = None

write_data(struct.pack("!Q",os.path.getsize(input_file)) + struct.pack("!b",bit_power))
with open(input_file,"rb") as open_input:
    read_data = open_input.read()
    write_data(read_data)

video_write.release()