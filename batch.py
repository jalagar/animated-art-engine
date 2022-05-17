from step1_layers_to_spritesheet.build import main as step1_main
from step3_generative_sheet_to_output.build import main as step3_main
import subprocess
from utils.file import parse_global_config
import multiprocessing

global_config_json = parse_global_config()
num_total_frames = global_config_json["numberOfFrames"]
num_frames_per_batch = global_config_json["numFramesPerBatch"]
total_supply = global_config_json["totalSupply"]
use_multiprocessing = global_config_json["useMultiprocessing"]
processor_count = global_config_json["processorCount"]
start_index = global_config_json["startIndex"]


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
    for i in range(num_total_frames // num_frames_per_batch):
        print(f"*******Starting Batch {i}*******")
        step1_main(i)
        # For first batch, run step2 normally to generate hashes
        if i == 0:
            subprocess.run(
                f"make step2",
                shell=True,
            )
        else:
            create_all_from_dna()
        # Only generate gif if its the last batch
        step3_main(
            i,
            should_generate_output=i == (num_total_frames // num_frames_per_batch - 1),
        )


if __name__ == "__main__":
    main()
