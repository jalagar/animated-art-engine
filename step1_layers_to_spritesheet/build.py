from PIL import Image as PIL_Image
from PIL.Image import Image
from typing import List, Tuple
import math

import os
import sys
import shutil
import multiprocessing

# In order to import utils/file.py we need to add this path.append
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file import setup_directory, sort_function, parse_global_config

global_config_json = parse_global_config()
is_debug = global_config_json["debug"]
num_total_frames = global_config_json["numberOfFrames"]
num_batch_frames = global_config_json["numFramesPerBatch"]
use_batches = global_config_json["useBatches"]
width = global_config_json["width"]
height = global_config_json["height"]
use_multiprocessing = global_config_json["useMultiprocessing"]
processor_count = global_config_json["processorCount"]

LAYERS_DIRECTORY = f"./{global_config_json['layersFolder']}"
TEMP_DIRECTORY = "./step1_layers_to_spritesheet/temp"
OUTPUT_DIRECTORY = "./step1_layers_to_spritesheet/output"


def combine_images(images: List[Image], batch_number: int) -> Image:
    """
    Combines images horizontally in a new image. This assumes
    all images are the same size.

    :param images: List of PIL Image classes
    :returns: PIL Image of all images combined horizontally
    :raises Exception: if no images are passed in
    """
    if len(images) == 0:
        raise Exception("No images passed in")

    # For batches, slice only batch number of frames
    if use_batches:
        images = images[
            batch_number * num_batch_frames : (batch_number + 1) * num_batch_frames
        ]

    dst = PIL_Image.new("RGBA", (len(images) * width, height), (0, 0, 0, 0))
    for i, img in enumerate(images):
        img_width, img_height = img.size
        # Only resize if the height/width are not the same
        if img_height != height or img_width != width:
            img = img.resize((height, width))
        dst.paste(img, (i * width, 0))
    return dst


def duplicate_images_number_of_frames_times(images: List[Image], num_total_frames: int):
    """
    Duplicates images number of layers times based on global_config.json
    or trims it if it is too long

    Ex. [0.png, 1.png]
    num_total_frames = 5
    output = [0.png, 1.png, 0.png, 1.png, 0.png]

    :param images: List of PIL Image classes
    :param num_total_frames: number of total frames in the list
    :returns: List of PIL Image classes
    """
    if len(images) == num_total_frames:
        return images

    num_time_multiple = math.ceil(num_total_frames / len(images))
    images = images * num_time_multiple
    if len(images) > num_total_frames:
        images = images[:num_total_frames]
    return images


def parse_attributes_into_images(
    attribute_folder: str, attribute_path: str, output_path: bool, batch_number: int
) -> Tuple[List[Image], bool]:
    """
    Mutual recursive function that parses the attributes
    in a folder into images.

    If it hits another folder, this function will call
    parse_attribute_folders which will call this method again

    :param attribute_folder: Folder name of attribute
    :param attribute_path: Path to folder of attribute
    :param output_path: output path to save images
    :returns: Tuple of list of images, and a boolean indicating if there contains a subfolder
    """
    images = []
    containsSubFolder = False

    for filename in sorted(os.listdir(attribute_path), key=sort_function):
        file_path = os.path.join(attribute_path, filename)
        if filename.endswith(".png"):
            img = PIL_Image.open(file_path)
            images.append(img)

        if os.path.isdir(file_path):
            containsSubFolder = True
            # Final output path needs to be output_layer_path/attribute_folder
            output_attribute_path = os.path.join(output_path, attribute_folder)
            setup_directory(output_attribute_path, delete_if_exists=False)
            parse_attribute_folders(
                filename, file_path, output_attribute_path, batch_number
            )

    if len(images) == 0:
        return [], containsSubFolder
    return (
        duplicate_images_number_of_frames_times(images, num_total_frames),
        containsSubFolder,
    )


def parse_attribute_folders(
    attribute_folder: str,
    attribute_path: str,
    output_path: str,
    batch_number: int,
) -> None:
    """
    Mutually recursive function that parses attribute folders by
    parsing all attributes into images and going into
    subfolders.

    Then it saves the images into the output path.

    :param attribute_folder: Folder name of attribute
    :param attribute_path: Path to folder of attribute
    :param output_path: output path to save images
    :returns: None
    """
    print(f"Parsing attributes in folder: {attribute_folder}")

    images, containsSubFolder = parse_attributes_into_images(
        attribute_folder,
        attribute_path,
        output_path=output_path,
        batch_number=batch_number,
    )
    if len(images) == 0:
        return

    spritesheet = combine_images(images, batch_number)
    # If it contains subfolder, that means there is if-then logic and we need to
    # place the file in the subfolder
    if containsSubFolder:
        output_folder = os.path.join(output_path, attribute_folder)
        if not os.path.exists(output_folder):
            setup_directory(output_folder)
        spritesheet.save(
            os.path.join(output_folder, f"{attribute_folder}.png"), quality=95
        )
    else:
        spritesheet.save(
            os.path.join(output_path, f"{attribute_folder}.png"), quality=95
        )


def search_folders_for_gifs(directory: str) -> bool:
    """
    Recursive function that searches folders for gifs
    :param directory: File path to directory
    :returns: bool - True or False if a gif exists
    """
    found_gif = False
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith("gif"):
            found_gif = True
        if os.path.isdir(file_path):
            found_gif = search_folders_for_gifs(file_path) or found_gif
    return found_gif


def parse_gifs_into_temp_directory(directory: str, output_directory: str) -> None:
    """
    Parses gifs in the layers folder and splits them into output directory
    :param directory - file path to layers directory
    :param output_directory - file path to output_directory
    :returns: None
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        output_path = os.path.join(output_directory, filename)
        if filename.endswith("gif"):
            pil_gif = PIL_Image.open(file_path)
            try:
                for i in range(num_total_frames):
                    pil_gif.seek(i)
                    pil_gif.save(os.path.join(output_directory, f"{i}.png"), quality=95)
            except EOFError:
                # Ran out of frames, not all gifs need to be the same length
                break

        if filename.endswith("png"):
            shutil.copyfile(file_path, output_path)
        if os.path.isdir(file_path):
            setup_directory(output_path, delete_if_exists=False)
            parse_gifs_into_temp_directory(file_path, output_path)


def process_layer_folder(layers_directory, layer_folder, batch_number):
    layer_path = os.path.join(layers_directory, layer_folder)
    # hidden files should be ignored
    if layer_folder.startswith("."):
        return
    output_layer_path = os.path.join(OUTPUT_DIRECTORY, layer_folder)

    setup_directory(output_layer_path)
    if os.path.isdir(layer_path):
        print(f"Parsing layer folder {layer_folder}")
        for attribute_folder in os.listdir(layer_path):
            attribute_path = os.path.join(layer_path, attribute_folder)
            if os.path.isdir(attribute_path):
                parse_attribute_folders(
                    attribute_folder,
                    attribute_path,
                    output_layer_path,
                    batch_number,
                )


def main(batch_number=0):
    print("********Starting step 1: Converting pngs to spritesheets********")

    setup_directory(OUTPUT_DIRECTORY)

    if use_batches:
        print(f"Creating layers for batch: {batch_number}")

    contains_gif_layer = search_folders_for_gifs(LAYERS_DIRECTORY)
    if contains_gif_layer:
        setup_directory(TEMP_DIRECTORY)
        parse_gifs_into_temp_directory(LAYERS_DIRECTORY, TEMP_DIRECTORY)
        layers_directory = TEMP_DIRECTORY
    else:
        layers_directory = LAYERS_DIRECTORY

    if use_multiprocessing:
        if processor_count > multiprocessing.cpu_count():
            raise Exception(
                f"You are trying to use too many processors, you passed in {processor_count} "
                f"but your computer can only handle {multiprocessing.cpu_count()}. Change this value and run make step1 again."
            )

        args = [
            (
                layers_directory,
                layer_folder,
                batch_number,
            )
            for layer_folder in os.listdir(layers_directory)
        ]
        with multiprocessing.Pool(processor_count) as pool:
            pool.starmap(
                process_layer_folder,
                args,
            )
    else:
        for layer_folder in os.listdir(layers_directory):
            process_layer_folder(layers_directory, layer_folder, batch_number)


if __name__ == "__main__":
    main()
