from step1_layers_to_spritesheet.build import main as step1_main
from step3_generative_sheet_to_output.build import main as step3_main
import subprocess
from utils.file import parse_global_config
import multiprocessing
import shutil
import os

global_config_json = parse_global_config()
num_total_frames = global_config_json["numberOfFrames"]
use_batching = global_config_json["useBatches"]
# if not using batching, default to num total frames
num_frames_per_batch = (
    global_config_json["numFramesPerBatch"] if use_batching else num_total_frames
)
total_supply = global_config_json["totalSupply"]
use_multiprocessing = global_config_json["useMultiprocessing"]
processor_count = global_config_json["processorCount"]
start_index = global_config_json["startIndex"]
height = global_config_json["height"]
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


def create_all_from_dna(num_frames_per_batch=num_frames_per_batch):
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
    if START_EDITION == start_index:
        print("********CREATING INITIAL JSON*******")
        # run step 1 with one pixel dimensions to speed up JSON processing and generate hashes
        step1_main(0, height=1, width=1)
        subprocess.run(
            f"cd step2_spritesheet_to_generative_sheet && npm run generate 1 1 && cd ..",
            shell=True,
        )

    print("********STARTING REGENERATION PROCESS*******")
    for i in range(num_total_frames // num_frames_per_batch):
        if use_batching:
            print(f"*******Starting Batch {i}*******")
        step1_main(i)

        # Remove step 2 folders to reset the editions if regenerating in parts
        shutil.rmtree("step2_spritesheet_to_generative_sheet/output/images")
        os.mkdir("step2_spritesheet_to_generative_sheet/output/images")
        create_all_from_dna()

        # Only generate animations if its the last batch
        step3_main(
            i,
            should_generate_output=i == (num_total_frames // num_frames_per_batch - 1),
        )

    # if odd number of frames
    if num_total_frames % num_frames_per_batch != 0:
        print(
            f"Odd number of frames, finishing final batch of length {num_total_frames % num_frames_per_batch}"
        )
        if use_batching:
            print(f"*******Starting Batch {i + 1}*******")
        step1_main(i + 1, num_total_frames % num_frames_per_batch)
        create_all_from_dna(num_total_frames % num_frames_per_batch)
        step3_main(i + 1, should_generate_output=True)


if __name__ == "__main__":
    main()
