from step1_layers_to_spritesheet.build import main as step1_main
from step3_generative_sheet_to_output.build import main as step3_main
import subprocess
from utils.file import parse_global_config
import os.path
import sys

# In order to import utils/file.py we need to add this path.append
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file import setup_directory
import multiprocessing

SKIP_STEP_ONE = False
SKIP_STEP_THREE = False

global_config_json = parse_global_config()
num_total_frames = global_config_json["numberOfFrames"]
num_frames_per_batch = global_config_json["numFramesPerBatch"]
total_supply = global_config_json["totalSupply"]
use_batches = global_config_json["useBatches"]
start_index = global_config_json["startIndex"]
use_multiprocessing = global_config_json["useMultiprocessing"]
processor_count = global_config_json["processorCount"]


def create_from_dna(edition):
    subprocess.run(
        f"cd step2_spritesheet_to_generative_sheet && npm run create_from_dna {edition}",
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
            (edition,) for edition in range(start_index, start_index + total_supply)
        ]
        with multiprocessing.Pool(processor_count) as pool:
            pool.starmap(
                create_from_dna,
                args,
            )
    else:
        # Then recreate DNA from the editions
        for edition in range(start_index, start_index + total_supply):
            create_from_dna(edition)


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
