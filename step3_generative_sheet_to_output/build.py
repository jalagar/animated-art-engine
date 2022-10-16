import subprocess
import multiprocessing
from PIL import Image
import os, sys
import json
from typing import Dict, List
import numpy

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
loop_gif = global_config_json["loopGif"]
use_multiprocessing = global_config_json["useMultiprocessing"]
processor_count = global_config_json["processorCount"]
start_index = global_config_json["startIndex"]
output_type = global_config_json["outputType"]
debug = global_config_json["debug"]
layers_folder = global_config_json["layersFolder"]
enable_audio = global_config_json["enableAudio"]
num_loop = global_config_json["numLoopMP4"]
generate_thumbnail = global_config_json["generateThumbnail"]
thumbnail_output_type = global_config_json["thumbnailOutputType"]
generate_pfp = global_config_json["generatePFP"]
pfp_frame_number = global_config_json["pfpFrameNumber"]
thumbnail_height = global_config_json["thumbnailHeight"]
thumbnail_width = global_config_json["thumbnailWidth"]

OUTPUT_DIRECTORY = f"./build/{output_type}"
THUMBNAIL_DIRECTORY = f"./build/thumbnail"
PFP_DIRECTORY = f"./build/pfp"
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


def get_audio_file_from_json(attribute_config: Dict[str, str]) -> List[str]:
    """
    Loops through and finds if there are any audio files
    """
    trait_type, value = attribute_config["trait_type"], attribute_config["value"]
    audio_file_paths = []
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
                            audio_file_paths.append(os.path.join(file_folder, file))
    return audio_file_paths

def generate_ffmpeg(mp4_quality, mp4_width, mp4_height, temp_img_folder, ffmpeg_string, output_directory, mp4_name, kwargs):
    subprocess.run(
        f"ffmpeg -stream_loop {num_loop} -y -r {fps} -f image2 -s {mp4_width}x{mp4_height} -i {temp_img_folder}/%d.png "
        + ffmpeg_string
        + f" -bitexact -shortest -vcodec libx264 "
        f"-crf {mp4_quality} -pix_fmt yuv420p {os.path.join(output_directory, mp4_name)}",
        shell=True,
        **kwargs,
    )

def generate_gif_imageio(output_directory, temp_img_folder, gif_name, gif_width, gif_height):
    # Moved import down here as people were having issues
    import imageio

    images = []
    for filename in sorted(os.listdir(temp_img_folder), key=sort_function):
        if filename.endswith(".png"):
            temp_img_path = os.path.join(temp_img_folder, filename)
            image = imageio.imread(temp_img_path)
            image = Image.fromarray(image).resize((gif_width, gif_height))
            images.append(numpy.array(image))

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

def generate_gif_gifski(output_directory, temp_img_folder, gif_name, gif_width, gif_height, kwargs):
    subprocess.run(
        f"gifski -o {os.path.join(output_directory, gif_name)} "
        f"{temp_img_folder}/*.png "
        f"--fps={fps} "
        f"--quality={quality} "
        f"-W={gif_width} "
        f"-H={gif_height} "
        f"--repeat={0 if loop_gif else -1}",
        shell=True,
        **kwargs,
    )

def convert_pngs_to_output(
    file_name: str,
    output_directory: str,
    thumbnail_directory: str,
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

    index = get_png_file_name(file_name)

    i = 0
    for filename in sorted(os.listdir(temp_img_folder), key=sort_function):
        if filename.endswith(".png"):
            temp_img_path = os.path.join(temp_img_folder, filename)
            if generate_pfp and i == pfp_frame_number:
                new_frame = Image.open(temp_img_path)
                new_frame.save(os.path.join(PFP_DIRECTORY, f"{index}.png"), quality=95)
            i += 1

    kwargs = {}
    if not debug:
        kwargs = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}

    mp4_name = index + ".mp4"
    gif_name = get_png_file_name(file_name) + ".gif"

    # ffmpeg uses quality 0 - 50, where 0 is the best, 50 is the worst.
    # so 50 - quality / 2 gives you the correct scale. Ex. quality = 100 will be 50 - 100 / 2 = 50
    # however I was having issues with 0 lossless, so pad 3 quality
    mp4_quality = int(50 - quality / 2) + 3
    ffmpeg_string = ""
    if enable_audio:
        metadata_json = get_metadata_json()
        metadata = metadata_json[int(index) - start_index]
        attributes = metadata["attributes"]
        audio_file_paths = []
        for attribute_config in attributes:
            audio_file_paths.extend(get_audio_file_from_json(attribute_config))

        if audio_file_paths:
            multi_audio_string = "".join(
                f"-i {audio_file_path} " for audio_file_path in audio_file_paths
            )
            subprocess.run(
                f"ffmpeg {multi_audio_string} -filter_complex amix=inputs={len(audio_file_paths)}:duration=longest"
                f" {os.path.join(get_temp_directory(file_name), 'output.mp3')}",
                shell=True,
                **kwargs,
            )
            ffmpeg_string = (
                f"-i {os.path.join(get_temp_directory(file_name), 'output.mp3')}"
            )

    if output_type == OutputType.MP4:
        generate_ffmpeg(mp4_quality, width, height, temp_img_folder, ffmpeg_string, output_directory, mp4_name, kwargs)
    elif output_type == OutputType.GIF:
        if gif_tool == GifTool.IMAGEIO:
            generate_gif_imageio(output_directory, temp_img_folder, gif_name, width, height)
        elif gif_tool == GifTool.GIFSKI:
            generate_gif_gifski(output_directory, temp_img_folder, gif_name, width, height, kwargs)
        else:
            raise Exception(
                f"Passed in invalid gif_tool {gif_tool}, only options are gifski and imageio"
            )
    else:
        raise Exception(
            f"Passed in invalid output type {output_type}, only options are gif and mp4"
        )
    
    if generate_thumbnail:
        print(f"Generating thumbnail {gif_name}")
        if thumbnail_output_type == OutputType.MP4:
            generate_ffmpeg(mp4_quality, thumbnail_width, thumbnail_height, temp_img_folder, ffmpeg_string, thumbnail_directory, mp4_name, kwargs)
        elif thumbnail_output_type == OutputType.GIF:
            if gif_tool == GifTool.IMAGEIO:
                generate_gif_imageio(thumbnail_directory, temp_img_folder, gif_name, thumbnail_width, thumbnail_height)
            elif gif_tool == GifTool.GIFSKI:
                generate_gif_gifski(thumbnail_directory, temp_img_folder, gif_name, thumbnail_width, thumbnail_height, kwargs)
            else:
                raise Exception(
                    f"Passed in invalid gif_tool {gif_tool}, only options are gifski and imageio"
                )
        else:
            raise Exception(
                f"Passed in invalid thumbnail output type {thumbnail_output_type}, only options are gif and mp4"
            )


def generate_output(
    filename: str,
    batch_number: int,
    should_generate_output: bool,
    output_directory: str,
    thumbnail_directory: str,
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
            output_directory,
            thumbnail_directory,
            output_width,
            output_height,
            temp_img_folder,
        )


def main(
    batch_number: int = 0,
    should_generate_output: bool = True,  # Flag to determine if we should generate the final output or not
    output_directory=None,
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
        for folder in [output_directory, TEMP_DIRECTORY]:
            setup_directory(folder)

        if generate_thumbnail:
            setup_directory(THUMBNAIL_DIRECTORY)

        if generate_pfp:
            setup_directory(PFP_DIRECTORY)

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
                THUMBNAIL_DIRECTORY,
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
                    THUMBNAIL_DIRECTORY,
                    output_width,
                    output_height,
                    get_temp_directory(filename),
                )


if __name__ == "__main__":
    main()
