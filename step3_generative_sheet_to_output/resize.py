from build import main as step3_main
import sys
import os

# In order to import utils/file.py we need to add this path.append
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file import (
    parse_global_config,
)

DISPLAY_URI_DIRECTORY = "./build/tezos/displayUri/"
THUMBNAIL_URI_DIRECTORY = "./build/tezos/thumbnailUri/"

global_config = parse_global_config()
global_config_width = global_config["width"]
global_config_height = global_config["height"]

DISPLAY_URI_FRACTION = 0.75
THUMBNAIL_URI_FRACTION = 0.5


def main():
    step3_main(
        output_directory=DISPLAY_URI_DIRECTORY,
        is_resize=True,
        output_width=int(DISPLAY_URI_FRACTION * global_config_width),
        output_height=int(DISPLAY_URI_FRACTION * global_config_height),
    )
    step3_main(
        output_directory=THUMBNAIL_URI_DIRECTORY,
        is_resize=True,
        output_width=int(THUMBNAIL_URI_FRACTION * global_config_width),
        output_height=int(THUMBNAIL_URI_FRACTION * global_config_height),
    )


if __name__ == "__main__":
    main()
