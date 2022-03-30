from PIL import Image as PIL_Image
import os
from PIL.Image import Image
from typing import List, Tuple
import json
from file import get_png_file_name, setup_directory


layers_directory = "./layers"
output_directory = "./step1_layers_to_spritesheet/output"
json_config = "./global_config.json"


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


def sort_function(file: str) -> int:
    """
    Sorts based on the integer file name ex. 2.py.
    That way 2.py comes before 10.py. Returns
    0 for any invalid file name (there might be some hidden files)

    :param file: filename
    :returns: int
    """
    try:
        return int(get_png_file_name(file))
    except:
        return 0


def parse_global_config() -> dict:
    global_config_file = open(json_config, "r")
    global_config_json = json.load(global_config_file)
    global_config_file.close()
    return global_config_json


def parse_attributes_into_images(
    attribute_path: str, num_frames: int, is_debug: bool
) -> List[Image]:
    images = []

    rarity_percentage = None
    for filename in sorted(os.listdir(attribute_path), key=sort_function):
        file_path = os.path.join(attribute_path, filename)
        if filename.endswith(".png"):
            img = PIL_Image.open(file_path)
            images.append(img)

    if len(images) == 1:
        if is_debug:
            print(
                f"Only one image found for: {attribute_path}, duplicating images {num_frames} number of times"
            )
        images = images * num_frames
    return images


def main():
    print("********Starting step 1: Converting pngs to spritesheets********")
    global_config_json = parse_global_config()
    is_debug = global_config_json["debug"]

    for layer_folder in os.listdir(layers_directory):
        layer_path = os.path.join(layers_directory, layer_folder)
        output_path = os.path.join(output_directory, layer_folder)
        setup_directory(output_path)

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
                        os.path.join(output_path, f"{attribute_folder}.png")
                    )


if __name__ == "__main__":
    main()
