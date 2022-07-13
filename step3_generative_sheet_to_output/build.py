import subprocess
import multiprocessing
from PIL import Image
import os, sys
import imageio
import json
from typing import Dict

# In order to import utils/file.py we need to add this path.append
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file import (
    get_png_file_name,
    setup_directory,
    sort_function,
    parse_global_config,
)

global_config_json = parse_global_config()
fps = global_config_json["framesPerSecond"]
height = global_config_json["height"]
width = global_config_json["width"]
height = global_config_json["height"]
quality = global_config_json["quality"]
gif_tool = global_config_json["gifTool"]
use_batches = global_config_json["useBatches"]
num_frames_per_batch = global_config_json["numFramesPerBatch"]
save_individual_frames = global_config_json["saveIndividualFrames"]
loop_gif = global_config_json["loopGif"]
use_multiprocessing = global_config_json["useMultiprocessing"]
processor_count = global_config_json["processorCount"]
start_index = global_config_json["startIndex"]
output_type = global_config_json["outputType"]
debug = global_config_json["debug"]
layers_folder = global_config_json["layersFolder"]
enable_audio = global_config_json["enableAudio"]
num_loop = global_config_json["numLoopMP4"]

OUTPUT_DIRECTORY = f"./build/{output_type}"
OUTPUT_IMAGES_DIRECTORY = "./build/images"
INPUT_DIRECTORY = "./step2_spritesheet_to_generative_sheet/output/images"
TEMP_DIRECTORY = "./step3_generative_sheet_to_output/temp"
JSON_DIRECTORY = f"./build/json"
LAYERS_DIRECTORY = f"./{layers_folder}"

VALID_AUDIO_FORMATS = ["mp3", "wav", "m4a"]


class GifTool:
    GIFSKI = "gifski"
    IMAGEIO = "imageio"


class OutputType:
    GIF = "gif"
    MP4 = "mp4"


def get_temp_directory(file_name: str):
    temp_directory = os.path.join(TEMP_DIRECTORY, get_png_file_name(file_name))
    setup_directory(temp_directory, delete_if_exists=False)
    return temp_directory


def get_metadata_json():
    f = open(os.path.join(JSON_DIRECTORY, "_metadata.json"), "r")
    metadata_list = json.load(f)
    f.close()
    return metadata_list


def crop_and_save(
    file_name: str,
    batch_number: int,
    width: int,
    height: int,
    temp_folder_name: str = None,
) -> None:
    """
    Crops image into squares and saves them into temp folder

    :param file_name: name of file
    :param height: height of each frame
    :param width: width of each frame
    :returns: int - duration for each frame in milliseconds
    """
    file = os.path.join(INPUT_DIRECTORY, file_name)
    im = Image.open(file)
    if use_batches:
        k = batch_number * num_frames_per_batch
    else:
        k = start_index

    imgwidth, imgheight = im.size
    temp_folder_path = get_temp_directory(temp_folder_name or file_name)

    for i in range(0, imgheight, height):
        for j in range(0, imgwidth, width):
            box = (j, i, j + width, i + height)
            a = im.crop(box)
            output_file_name = f"{k}.png"
            file_path = os.path.join(temp_folder_path, output_file_name)
            a.save(file_path, quality=95)
            k += 1


def get_audio_file_from_json(attribute_config: Dict[str, str]) -> str:
    """
    Loops through and finds if there are any audio files
    """
    trait_type, value = attribute_config["trait_type"], attribute_config["value"]
    audio_file_path = ""
    for layer in os.listdir(layers_folder):
        if layer == trait_type:
            value_folder = os.path.join(layers_folder, trait_type)
            for folder_value in os.listdir(value_folder):
                if folder_value.startswith(value):
                    file_folder = os.path.join(value_folder, folder_value)
                    for file in os.listdir(file_folder):
                        if any(
                            file.endswith(audio_ending)
                            for audio_ending in VALID_AUDIO_FORMATS
                        ):
                            audio_file_path = os.path.join(file_folder, file)
    return audio_file_path


def convert_pngs_to_output(
    file_name: str,
    fps: int,
    output_directory: str,
    is_resize: bool,
    width: int,
    height: int,
    temp_img_folder: str,
    sort_function=None,
):
    """
    Loop through temp_img_folder using the sort_function and save individual frames
    and then using either IMAGEIO or GIFSKI save the gif
    """
    if not sort_function:
        sort_function = lambda img: int(get_png_file_name(img))

    images_directory = os.path.join(
        OUTPUT_IMAGES_DIRECTORY, get_png_file_name(file_name)
    )
    if save_individual_frames and not is_resize:
        setup_directory(images_directory)

    for filename in sorted(os.listdir(temp_img_folder), key=sort_function):
        if filename.endswith(".png"):
            temp_img_path = os.path.join(temp_img_folder, filename)
            if save_individual_frames and not is_resize:
                new_frame = Image.open(temp_img_path)
                new_frame.save(os.path.join(images_directory, filename), quality=95)

    kwargs = {}
    if not debug:
        kwargs = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}

    if output_type == OutputType.MP4:
        # ffmpeg uses quality 0 - 50, where 0 is the best, 50 is the worst.
        # so 50 - quality / 2 gives you the correct scale. Ex. quality = 100 will be 50 - 100 / 2 = 50
        # however I was having issues with 0 lossless, so pad 3 quality
        index = get_png_file_name(file_name)
        mp4_name = index + ".mp4"
        mp4_quality = int(50 - quality / 2) + 3

        ffmpeg_string = ""
        if enable_audio:
            metadata_json = get_metadata_json()
            metadata = metadata_json[int(index) - start_index]
            attributes = metadata["attributes"]
            audio_file_paths = []
            for attribute_config in attributes:
                audio_file_path = get_audio_file_from_json(attribute_config)
                if audio_file_path:
                    audio_file_paths.append(audio_file_path)

            if len(audio_file_paths) > 1:
                raise Exception(
                    f"Multiple audio files for attribute {audio_file_paths}"
                )

            audio_file_path = ""
            if len(audio_file_paths) == 1:
                audio_file_path = audio_file_paths[0]

            if audio_file_path:
                ffmpeg_string = f"-i '{audio_file_path}' -bitexact "

        subprocess.run(
            f"ffmpeg -stream_loop {num_loop} -y -r {fps} -f image2 -s {width}x{height} -i {temp_img_folder}/%d.png "
            + ffmpeg_string
            + f"-shortest -vcodec libx264 "
            f"-crf {mp4_quality} -pix_fmt yuv420p {os.path.join(output_directory, mp4_name)}",
            shell=True,
            **kwargs,
        )
    elif output_type == OutputType.GIF:
        gif_name = get_png_file_name(file_name) + ".gif"
        if gif_tool == GifTool.IMAGEIO:
            images = []
            for filename in sorted(os.listdir(temp_img_folder), key=sort_function):
                if filename.endswith(".png"):
                    temp_img_path = os.path.join(temp_img_folder, filename)
                    images.append(imageio.imread(temp_img_path))

            with imageio.get_writer(
                os.path.join(output_directory, gif_name),
                fps=fps,
                mode="I",
                quantizer=0,
                palettesize=256,
                loop=0 if loop_gif else 1,
            ) as writer:
                for image in images:
                    writer.append_data(image)
        elif gif_tool == GifTool.GIFSKI:
            subprocess.run(
                f"gifski -o {os.path.join(output_directory, gif_name)} "
                f"{temp_img_folder}/*.png "
                f"--fps={fps} "
                f"--quality={quality} "
                f"-W={width} "
                f"-H={height} "
                f"--repeat={0 if loop_gif else -1}",
                shell=True,
                **kwargs,
            )
        else:
            raise Exception(
                f"Passed in invalid gif_tool {gif_tool}, only options are gifski and imageio"
            )
    else:
        raise Exception(
            f"Passed in invalid output type {output_type}, only options are gif and mp4"
        )


def fps_to_ms_duration(fps: int) -> int:
    """
    Converts frames per second to millisecond duration.
    PIL library takes in millisecond duration per frame
    which is unintuitive from an animation perspective.

    NOTE - this will not always be exact given the library
    takes in an integer for number of milliseconds.
    Ex. 12fps = 83.33ms per frame, but the code will convert
    it to 83. Not noticeable by the human eye but still
    worth calling out.

    :param file: fps - frames per second
    :returns: int - duration for each frame in milliseconds
    """
    return int(1000 / fps)


def generate_output(
    filename: str,
    batch_number: int,
    should_generate_output: bool,
    output_directory: str,
    is_resize: bool,
    output_width: int,
    output_height: int,
    temp_img_folder: str,
):
    # Use global_config here from step2, not the override width/height
    crop_and_save(filename, batch_number, width, height)
    if not use_batches or should_generate_output:
        print(f"Converting spritesheet to {output_type} for {filename}")
        convert_pngs_to_output(
            filename,
            fps,
            output_directory,
            is_resize,
            output_width,
            output_height,
            temp_img_folder,
        )


def main(
    batch_number: int = 0,
    should_generate_output: bool = True,  # Flag to determine if we should generate the final output or not
    output_directory=None,
    is_resize=False,
    output_width=None,
    output_height=None,
):
    print(f"Starting step 3: Converting sprite sheets to {output_type}")

    if not output_directory:
        output_directory = OUTPUT_DIRECTORY

    if not output_width:
        output_width = width

    if not output_height:
        output_height = height

    if use_batches:
        print(
            f"Starting {batch_number} with should_generate_output flag {should_generate_output}"
        )

    # Only set up folders if its the first batch
    if not use_batches or batch_number == 0:
        for folder in [output_directory, OUTPUT_IMAGES_DIRECTORY, TEMP_DIRECTORY]:
            setup_directory(folder)

    if use_multiprocessing:
        if processor_count > multiprocessing.cpu_count():
            raise Exception(
                f"You are trying to use too many processors, you passed in {processor_count} "
                f"but your computer can only handle {multiprocessing.cpu_count()}. Change this value and run make step3 again."
            )

        args = [
            (
                filename,
                batch_number,
                should_generate_output,
                output_directory,
                is_resize,
                output_width,
                output_height,
                get_temp_directory(filename),
            )
            for filename in sorted(os.listdir(INPUT_DIRECTORY), key=sort_function)
            if filename.endswith(".png")
        ]
        with multiprocessing.Pool(processor_count) as pool:
            pool.starmap(
                generate_output,
                args,
            )
    else:
        for filename in sorted(os.listdir(INPUT_DIRECTORY), key=sort_function):
            if filename.endswith(".png"):
                generate_output(
                    filename,
                    batch_number,
                    should_generate_output,
                    output_directory,
                    is_resize,
                    output_width,
                    output_height,
                    get_temp_directory(filename),
                )


if __name__ == "__main__":
    main()
