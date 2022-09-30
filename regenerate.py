from step1_layers_to_spritesheet.build import main as step1_main
from step3_generative_sheet_to_output.build import main as step3_main
import subprocess
from utils.file import parse_global_config
import os.path
import sys
import shutil

# In order to import utils/file.py we need to add this path.append
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file import setup_directory
import multiprocessing

SKIP_STEP_ONE = False
SKIP_STEP_THREE = False

global_config_json = parse_global_config()
num_total_frames = global_config_json["numberOfFrames"]
use_batching = global_config_json["useBatches"]
# if not using batching, default to num total frames
num_frames_per_batch = (
    global_config_json["numFramesPerBatch"] if use_batching else num_total_frames
)
total_supply = global_config_json["totalSupply"]
use_batches = global_config_json["useBatches"]
start_index = global_config_json["startIndex"]
use_multiprocessing = global_config_json["useMultiprocessing"]
processor_count = global_config_json["processorCount"]
width = global_config_json["width"]

"""
Override START_EDITION and END_EDITION if you want to run in batches.
Default values:
START_EDITION = start_index
END_EDITION = start_index + total_supply

Ex. You have a 10k collection but it takes too long to render the entire collection. You would first do
START_EDITION = start_index
END_EDITION = 1000 (exclusive)

This would generate all 10k JSON files, but only generate the NFTs for the first 1K.

Then you can move these NFTs to another folder, and then change:
START_EDITION = 1000
END_EDITION = 2000
etc...

NOTE END_EDITION is exclusive, so if start_index is 0 and you have 10k collection, END_EDITION would be 10001
"""
START_EDITION = start_index
END_EDITION = start_index + total_supply


def create_from_dna(edition, num_frames_per_batch=num_frames_per_batch):
    override_width = num_frames_per_batch * width
    subprocess.run(
        f"cd step2_spritesheet_to_generative_sheet && npm run create_from_dna {edition} {override_width}",
        shell=True,
    )


def create_all_from_dna():
    if use_multiprocessing:
        if processor_count > multiprocessing.cpu_count():
            raise Exception(
                f"You are trying to use too many processors, you passed in {processor_count} "
                f"but your computer can only handle {multiprocessing.cpu_count()}. Change this value and run make step3 again."
            )

        args = [
            (edition, num_frames_per_batch)
            for edition in range(START_EDITION, END_EDITION)
        ]
        with multiprocessing.Pool(processor_count) as pool:
            pool.starmap(
                create_from_dna,
                args,
            )
    else:
        # Then recreate DNA from the editions
        for edition in range(START_EDITION, END_EDITION):
            create_from_dna(edition, num_frames_per_batch)


def main():
    # Run step 1 to generate layers
    if not SKIP_STEP_ONE:
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
    setup_directory("step2_spritesheet_to_generative_sheet/output/images")

    if use_batches:
        for i in range(num_total_frames // num_frames_per_batch):
            print(f"*******Starting Batch {i}*******")
            step1_main(i)
            # Remove step 2 folders to reset the editions if regenerating in parts
            shutil.rmtree("step2_spritesheet_to_generative_sheet/output/images")
            os.mkdir("step2_spritesheet_to_generative_sheet/output/images")
            create_all_from_dna()
            # Only generate gif if its the last batch
            if not SKIP_STEP_THREE:
                step3_main(
                    i,
                    should_generate_output=i
                    == (num_total_frames // num_frames_per_batch - 1),
                )
    else:
        create_all_from_dna()
        # Finally output gifs
        if not SKIP_STEP_THREE:
            step3_main()


if __name__ == "__main__":
    main()
