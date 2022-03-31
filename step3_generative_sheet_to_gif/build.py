from PIL import Image
import os
import json
from file import get_png_file_name, setup_directory

output_gifs_directory = "./build/gifs"
output_images_directory = "./build/images"
input_directory = "./step2_spritesheet_to_generative_sheet/output/images"
temp_directory = "./step3_generative_sheet_to_gif/temp"
json_config = "./global_config.json"


def parse_global_config() -> dict:
    global_config_file = open(json_config, "r")
    global_config_json = json.load(global_config_file)
    global_config_file.close()
    return global_config_json


def crop_and_save(file_name: str, height: int, width: int) -> None:
    """
    Crops image into squares and saves them into temp folder

    :param file_name: name of file
    :param height: height of each frame
    :param width: width of each frame
    :returns: int - duration for each frame in milliseconds
    """
    file = os.path.join(input_directory, file_name)
    im = Image.open(file)
    k = 0
    imgwidth, imgheight = im.size
    temp_folder_path = os.path.join(temp_directory, get_png_file_name(file_name))

    if not os.path.exists(temp_folder_path):
        os.mkdir(temp_folder_path)

    for i in range(0, imgheight, height):
        for j in range(0, imgwidth, width):
            box = (j, i, j + width, i + height)
            a = im.crop(box)
            file_path = os.path.join(temp_folder_path, "%s.png" % k)
            a.save(file_path)
            k += 1


def convert_pngs_to_gif(file_name: str, quality: int, duration: int):
    frames = []
    global_config = parse_global_config()
    save_individual_frames = global_config["saveIndividualFrames"]

    images_directory = os.path.join(
        output_images_directory, get_png_file_name(file_name)
    )
    if save_individual_frames:
        setup_directory(images_directory)
    temp_img_folder = os.path.join(temp_directory, get_png_file_name(file_name))

    for filename in sorted(
        os.listdir(temp_img_folder), key=lambda img: int(get_png_file_name(img))
    ):
        if filename.endswith(".png"):
            temp_img_path = os.path.join(temp_img_folder, filename)
            new_frame = Image.open(temp_img_path)
            if save_individual_frames:
                new_frame.save(os.path.join(images_directory, filename))
            frames.append(new_frame)

    gif_name = get_png_file_name(file_name) + ".gif"
    frames[0].save(
        os.path.join(output_gifs_directory, gif_name),
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=0,
        quality=quality,
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


def main():
    print("Starting step 3: Converting sprite sheets to gifs")
    global_config = parse_global_config()
    quality = global_config["quality"]
    fps = global_config["framesPerSecond"]
    height = global_config["height"]
    width = global_config["width"]

    for folder in [output_gifs_directory, output_images_directory, temp_directory]:
        setup_directory(folder)

    for filename in sorted(os.listdir(input_directory), key=sort_function):
        if filename.endswith(".png"):
            print(f"Converting spritesheet to gif for {filename}")
            crop_and_save(
                filename,
                height,
                width,
            )
            convert_pngs_to_gif(filename, quality, fps_to_ms_duration(fps))


if __name__ == "__main__":
    main()
