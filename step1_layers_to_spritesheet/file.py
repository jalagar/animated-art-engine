import shutil
import os


def setup_directory(directory_path: str) -> None:
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)


def get_png_file_name(file_name: str) -> str:
    return file_name.split(".png")[0]
