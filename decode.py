import os
import sys
import struct
import numpy
import cv2

import utils

input_file = "./input/input.mp4"
output_file = "./output/output.tar.gz"

# steps_list = []
# sequences = utils.generate_bit_combinations(bit_power)

if (not os.path.exists(input_file)):
    print(f"[FAIL] {input_file} does not exist!")
    sys.exit(1)

if (os.path.exists(output_file)):
    print(f"[FAIL] {output_file} already exists!")
    sys.exit(1)

print(f"[INFO] Decoding from {input_file} to {output_file}.")

video_read = cv2.VideoCapture(input_file)

while True:
    retval,frame = video_read.read()
    if (not frame):
        break
    # TODO