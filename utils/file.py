import shutil
import os

import json

json_config = "./global_config.json"


def parse_global_config() -> dict:
    global_config_file = open(json_config, "r")
    global_config_json = json.load(global_config_file)
    global_config_file.close()
    return global_config_json


global_config_json = parse_global_config()
is_debug = global_config_json["debug"]
use_file_numbering = global_config_json["useFileNumbering"]


def setup_directory(directory_path: str, delete_if_exists: bool = True) -> None:
    is_debug and print(f"Setting up directory {directory_path}")
    if os.path.exists(directory_path) and delete_if_exists:
        is_debug and print(f"Directory {directory_path} exists, deleting directory")
        shutil.rmtree(directory_path)

    if not os.path.exists(directory_path):
        is_debug and print(f"Creating directory {directory_path}")
        os.makedirs(directory_path)


def get_png_file_name(file_name: str) -> str:
    return file_name.split(".png")[0]


def sort_function(file: str) -> int:
    """
    Sorts based on the integer file name ex. 2.py.
    That way 2.py comes before 10.py. Returns
    0 for any invalid file name (there might be some hidden files)

    :param file: filename
    :returns: int
    """
    try:
        if use_file_numbering:
            return int(get_png_file_name(file))
        return get_png_file_name(file)
    except:
        return 0
