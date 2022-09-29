import base64

import sys
import os

# In order to import utils/file.py we need to add this path.append
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file import (
    setup_directory,
    sort_function,
    parse_global_config,
    get_png_file_name,
)

global_config_json = parse_global_config()
output_type = global_config_json["outputType"]

OUTPUT_DIRECTORY = "./build/html"
ANIMATION_DIRECTORY = f"./build/{output_type}"
PFP_DIRECTORY = "./build/pfp"


def encode_binary_file_to_string(binary_file) -> str:
    base64_encoded_data = base64.b64encode(binary_file.read())
    return base64_encoded_data.decode("utf-8")


def main():
    """
    This function works by looping through all the PFPs in the pfp folder
    and uses template.html to insert the raw bytes of the PFP and the animated file
    and logo.
    """
    if not os.path.exists(ANIMATION_DIRECTORY) or not os.path.exists(PFP_DIRECTORY):
        raise Exception(
            "Missing animation directory or pfp directory, make sure to have generatePFP set to true"
        )

    with open("./generate_html/logo.png", "rb") as binary_file:
        encoded_logo = encode_binary_file_to_string(binary_file)

    setup_directory(OUTPUT_DIRECTORY)

    for file in os.listdir(PFP_DIRECTORY):
        edition = get_png_file_name(file)
        print(f"Generated {edition}.html")

        with open("./generate_html/template.html", "rt") as template_file:
            template_text = template_file.read()

        result_text = template_text.replace("logo_here", encoded_logo)

        animated_file_path = os.path.join(
            ANIMATION_DIRECTORY, f"{edition}.{output_type}"
        )

        with open(os.path.join(PFP_DIRECTORY, file), "rb") as binary_file:
            result_text = result_text.replace(
                "image_here", encode_binary_file_to_string(binary_file)
            )

        with open(animated_file_path, "rb") as binary_file:
            result_text = result_text.replace(
                "gif_here", encode_binary_file_to_string(binary_file)
            )

        with open(
            os.path.join(OUTPUT_DIRECTORY, f"{edition}.html"), "wt"
        ) as output_file:
            output_file.write(result_text)


if __name__ == "__main__":
    main()
