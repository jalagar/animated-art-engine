from PIL import Image as PIL_Image
import os
from PIL.Image import Image
from typing import List
import json
from file import get_png_file_name, setup_directory

layers_directory = "./layers"
output_directory = "./step1_png_to_spritesheet/output"

# TODO read this from a config
NUM_IMAGES = 12


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


def sort_function(file: str):
    """
    Sorts based on the integer file name ex. 2.py.
    That way 2.py comes before 10.py. Ignores
    other file names if it is not a valid integer.
    """
    try:
        return int(get_png_file_name(file))
    except:
        return file


def main():
    print("********Starting step 1: Converting pngs to spritesheets********")
    for layer_folder in sorted(os.listdir(layers_directory), key=sort_function):
        layer_path = os.path.join(layers_directory, layer_folder)
        output_path = os.path.join(output_directory, layer_folder)
        setup_directory(output_path)

        if os.path.isdir(layer_path):
            print(f"Parsing layer folder: {layer_folder}")
            for attribute_folder in os.listdir(layer_path):
                attribute_path = os.path.join(layer_path, attribute_folder)
                if os.path.isdir(attribute_path):
                    print(f"Parsing attributes in folder: {attribute_folder}")
                    images = []
                    # Default 100% rarity which would give them equal weight
                    rarity_percentage = 100
                    for filename in sorted(os.listdir(attribute_path)):
                        file_path = os.path.join(attribute_path, filename)
                        if filename == "config.json":
                            config_file = open(file_path, "r")
                            config_json = json.load(config_file)
                            rarity_percentage = config_json["rarity"]
                        if filename.endswith(".png"):
                            img = PIL_Image.open(file_path)
                            images.append(img)

                    if len(images) == 1:
                        images = images * NUM_IMAGES

                    dst = combine_images(images)
                    dst.save(
                        os.path.join(
                            output_path, f"{attribute_folder}#{rarity_percentage}.png"
                        )
                    )


if __name__ == "__main__":
    main()
