from step1_layers_to_spritesheet.build import main as step1_main
from step3_generative_sheet_to_output.build import main as step3_main
import subprocess
from utils.file import parse_global_config

global_config_json = parse_global_config()
num_total_frames = global_config_json["numberOfFrames"]
num_frames_per_batch = global_config_json["numFramesPerBatch"]
total_supply = global_config_json["totalSupply"]


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
            for edition in range(total_supply):
                subprocess.run(
                    f"cd step2_spritesheet_to_generative_sheet && npm run create_from_dna {edition}",
                    shell=True,
                )
        # Only generate gif if its the last batch
        step3_main(
            i,
            should_generate_output=i == (num_total_frames // num_frames_per_batch - 1),
        )


if __name__ == "__main__":
    main()
