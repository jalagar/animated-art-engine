from step1_layers_to_spritesheet.build import main as step1_main
from step3_generative_sheet_to_gif.build import main as step3_main
import subprocess
from utils.file import parse_global_config
import os.path
import sys

# In order to import utils/file.py we need to add this path.append
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file import setup_directory


global_config_json = parse_global_config()
num_total_frames = global_config_json["numberOfFrames"]
num_frames_per_batch = global_config_json["numFramesPerBatch"]
total_supply = global_config_json["totalSupply"]
use_batches = global_config_json["useBatches"]


def main():
    # Run step 1 to generate layers
    step1_main()
    setup_directory("build", delete_if_exists=False)
    setup_directory("build/json", delete_if_exists=False)

    # If metadata JSON and dna don't not exist, recreate metadata
    if not os.path.isfile("build/json/_metadata.json") and not os.path.isfile(
        "build/_dna.json"
    ):
        subprocess.run(
            f"cd step2_spritesheet_to_generative_sheet && npm run regenerate_metadata",
            shell=True,
        )

    # If DNA does not exist, recreate it, this depends on _metadata.json
    if not os.path.isfile("build/_dna.json"):
        subprocess.run(
            f"cd step2_spritesheet_to_generative_sheet && npm run regenerate_dna",
            shell=True,
        )

    # Then regenerate all the JSON files
    subprocess.run(
        f"cd step2_spritesheet_to_generative_sheet && npm run regenerate_metadata_from_dna",
        shell=True,
    )

    if use_batches:
        for i in range(num_total_frames // num_frames_per_batch):
            print(f"*******Starting Batch {i}*******")
            step1_main(i)
            for edition in range(total_supply):
                subprocess.run(
                    f"cd step2_spritesheet_to_generative_sheet && npm run create_from_dna {edition}",
                    shell=True,
                )
            # Only generate gif if its the last batch
            step3_main(
                i, generate_gifs=i == (num_total_frames // num_frames_per_batch - 1)
            )
    else:
        # Then recreate DNA from the editions
        for edition in range(total_supply):
            subprocess.run(
                f"cd step2_spritesheet_to_generative_sheet && npm run create_from_dna {edition}",
                shell=True,
            )

        # Finally output gifs
        step3_main()


if __name__ == "__main__":
    main()
