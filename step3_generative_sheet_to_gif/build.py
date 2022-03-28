from PIL import Image
import os

from file import get_png_file_name, setup_directory

output_directory = "./build/gifs"
input_directory = "./step2_spritesheet_to_generative_sheet/output/images"
temp_directory = "./step3_generative_sheet_to_gif/temp"


def crop(file_name, height, width, area=None):
    file = os.path.join(input_directory, file_name)
    if not area:
        area = height * width

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


def convert_pngs_to_gif(file_name: str):
    frames = []

    temp_img_folder = os.path.join(temp_directory, get_png_file_name(file_name))
    for filename in sorted(
        os.listdir(temp_img_folder), key=lambda img: int(get_png_file_name(img))
    ):
        if filename.endswith(".png"):
            temp_img_path = os.path.join(temp_img_folder, filename)
            new_frame = Image.open(temp_img_path)
            frames.append(new_frame)

    gif_name = get_png_file_name(file_name) + ".gif"
    frames[0].save(
        os.path.join(output_directory, gif_name),
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=125,
        loop=0,
        quality=95,
    )


def main():
    print("Starting step 3: Converting sprite sheets to gifs")
    for folder in [output_directory, temp_directory]:
        setup_directory(folder)

    for filename in sorted(
        os.listdir(input_directory), key=lambda file: int(get_png_file_name(file))
    ):
        print(f"Converting spritesheet to gif for {filename}")
        if filename.endswith(".png"):
            crop(
                filename,
                1000,
                1000,
            )
            convert_pngs_to_gif(filename)


if __name__ == "__main__":
    main()
