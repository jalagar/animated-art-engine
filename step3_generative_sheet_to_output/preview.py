from glob import glob
import os, sys

from pymongo import DESCENDING

# In order to import utils/file.py we need to add this path.append
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file import (
    get_png_file_name,
    setup_directory,
    sort_function,
    parse_global_config,
)
from build import crop_and_save, convert_pngs_to_output

import random


INPUT_DIRECTORY = "./step2_spritesheet_to_generative_sheet/output/images"
TEMP_DIRECTORY = "./step3_generative_sheet_to_output/temp"
BUILD_DIRECTORY = "./build/"

global_config = parse_global_config()
total_supply = global_config["totalSupply"]
height = global_config["height"]
width = global_config["width"]
fps = global_config["framesPerSecond"]
output_type = global_config["outputType"]

NUM_PREVIEW_OUTPUT = 4


class OrderEnum:
    RANDOM = "random"
    ASC = "ascending"
    DESC = "descending"


SORT_ORDER = OrderEnum.RANDOM


def main():
    # Reset temp directory
    setup_directory(TEMP_DIRECTORY)

    # subtract one because both numbers are included in randint
    sort_function = lambda _: random.randint(0, total_supply - 1)
    if SORT_ORDER == OrderEnum.ASC:
        sort_function = lambda file: int(get_png_file_name(file))
    elif SORT_ORDER == OrderEnum.DESC:
        sort_function = lambda file: -int(get_png_file_name(file))
    input_directory_files = sorted(os.listdir(INPUT_DIRECTORY), key=sort_function)[
        :NUM_PREVIEW_OUTPUT
    ]
    for i, filename in enumerate(input_directory_files):
        if filename.endswith(".png"):
            print(f"Including {filename} in preview {output_type}")
            # Save all files to the same folder
            crop_and_save(
                filename,
                i,
                width,
                height,
                temp_folder_name="preview",
            )

    convert_pngs_to_output(
        "preview",
        fps,
        BUILD_DIRECTORY,
        False,
        width,
        height,
    )


if __name__ == "__main__":
    main()
