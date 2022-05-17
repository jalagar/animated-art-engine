import os, sys

import shutil

# In order to import utils/file.py we need to add this path.append
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file import (
    get_png_file_name,
    setup_directory,
    parse_global_config,
)
from build import crop_and_save, convert_pngs_to_output

import random


INPUT_DIRECTORY = "./step2_spritesheet_to_generative_sheet/output/images"
TEMP_DIRECTORY = "./step3_generative_sheet_to_output/temp"
BUILD_DIRECTORY = "./build/"
TEMP_PREVIEW_DIRECTORY = os.path.join(TEMP_DIRECTORY, "preview")

global_config = parse_global_config()
total_supply = global_config["totalSupply"]
height = global_config["height"]
width = global_config["width"]
fps = global_config["framesPerSecond"]
output_type = global_config["outputType"]
num_frames = global_config["numberOfFrames"]

NUM_PREVIEW_OUTPUT = 4


class OrderEnum:
    RANDOM = "random"
    ASC = "ascending"
    DESC = "descending"


SORT_ORDER = OrderEnum.RANDOM


def main():
    # subtract one because both numbers are included in randint
    sort_function = lambda _: random.randint(0, total_supply - 1)
    if SORT_ORDER == OrderEnum.ASC:
        sort_function = lambda file: int(get_png_file_name(file))
    elif SORT_ORDER == OrderEnum.DESC:
        sort_function = lambda file: -int(get_png_file_name(file))

    setup_directory(TEMP_PREVIEW_DIRECTORY)
    for i, folder in enumerate(
        sorted(os.listdir(TEMP_DIRECTORY), key=sort_function)[:NUM_PREVIEW_OUTPUT]
    ):
        print(f"Including {folder} in the preview {output_type}")
        folder_path = os.path.join(TEMP_DIRECTORY, folder)
        for image in os.listdir(folder_path):
            file_num = i * num_frames + int(get_png_file_name(image))
            shutil.copy2(
                os.path.join(folder_path, image),
                os.path.join(
                    TEMP_PREVIEW_DIRECTORY,
                    f"{file_num}.png",
                ),
            )

    print(f"Converting images to a {output_type}")
    convert_pngs_to_output(
        "preview",
        fps,
        BUILD_DIRECTORY,
        False,
        width,
        height,
        TEMP_PREVIEW_DIRECTORY,
        sort_function=lambda img: img,
    )


if __name__ == "__main__":
    main()
