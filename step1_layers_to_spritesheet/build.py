from PIL import Image as PIL_Image
import os
from PIL.Image import Image
from typing import List, Tuple
import json
import math

# In order to import utils/file.py we need to add this path.append
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file import setup_directory, sort_function, parse_global_config

layers_directory = "./layers"
output_directory = "./step1_layers_to_spritesheet/output"


def combine_images(images: List[Image]) -> Image:
    """
    Combines images horizontally in a new image. This assumes
    all images are the same size.

    :param images: List of PIL Image classes
    :returns: PIL Image of all images combined horizontally
    :raises Exception: if no images are passed in
    """
    if len(images) == 0:
        raise Exception("No images passed in")

    width, height = images[0].size
    dst = PIL_Image.new("RGBA", (len(images) * width, height), (0, 0, 0, 0))
    for i, img in enumerate(images):
        dst.paste(img, (i * width, 0))
    return dst

def duplicate_images_number_of_frames_times(images: List[Image], num_frames: int):
    """
    Duplicates images number of layers times based on global_config.json
    or trims it if it is too long

    Ex. [0.png, 1.png]
    num_frames = 5
    output = [0.png, 1.png, 0.png, 1.png, 0.png]

    :param images: List of PIL Image classes
    :param num_frames: number of total frames in the list
    :returns: List of PIL Image classes
    """
    if len(images) == num_frames:
        return images

    num_time_multiple = math.ceil(num_frames / len(images))
    images = images * num_time_multiple
    if len(images) > num_frames:
        images = images[:num_frames]
    return images


def parse_attributes_into_images(
    attribute_path: str, num_frames: int, is_debug: bool
) -> List[Image]:
    images = []

    for filename in sorted(os.listdir(attribute_path), key=sort_function):
        file_path = os.path.join(attribute_path, filename)
        if filename.endswith(".png"):
            img = PIL_Image.open(file_path)
            images.append(img)

    return duplicate_images_number_of_frames_times(images, num_frames)


def main():
    print("********Starting step 1: Converting pngs to spritesheets********")
    global_config_json = parse_global_config()
    is_debug = global_config_json["debug"]

    setup_directory(output_directory)
    for layer_folder in os.listdir(layers_directory):
        layer_path = os.path.join(layers_directory, layer_folder)

        output_layer_path = os.path.join(output_directory, layer_folder)
        # hidden files should be ignored
        if layer_folder.startswith("."):
            continue

        setup_directory(output_layer_path)

        if os.path.isdir(layer_path):
            print(f"Parsing layer folder: {layer_folder}")
            for attribute_folder in os.listdir(layer_path):
                attribute_path = os.path.join(layer_path, attribute_folder)
                if os.path.isdir(attribute_path):
                    print(f"Parsing attributes in folder: {attribute_folder}")

                    images = parse_attributes_into_images(
                        attribute_path,
                        num_frames=global_config_json["numberOfFrames"],
                        is_debug=is_debug,
                    )
                    spritesheet = combine_images(images)
                    spritesheet.save(
                        os.path.join(output_layer_path, f"{attribute_folder}.png")
                    )


if __name__ == "__main__":
    main()
