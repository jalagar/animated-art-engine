first_time_setup:
	python3 -m pip install --upgrade Pillow && pip3 install -r requirements.txt
	cd step2_spritesheet_to_generative_sheet && npm i && cd ..

step1:
	python3 step1_layers_to_spritesheet/build.py

step2:
	cd step2_spritesheet_to_generative_sheet && npm run generate && cd ..

step3:
	python3 step3_generative_sheet_to_output/build.py

all:
	make step1
	make step2
	make step3

solana:
	cd step2_spritesheet_to_generative_sheet && npm run generate:solana && cd ..

tezos:
	cd step2_spritesheet_to_generative_sheet && npm run generate:tezos && cd ..
	python3 step3_generative_sheet_to_output/resize.py

provenance:
	cd step2_spritesheet_to_generative_sheet && node utils/provenance.js && cd ..


rarity:
	cd step2_spritesheet_to_generative_sheet && node utils/rarityData.js && cd ..

update_json:
	cd step2_spritesheet_to_generative_sheet && node utils/updateInfo.js && cd ..

update_json_tezos:
	cd step2_spritesheet_to_generative_sheet && npm run update_info:tezos && cd ..

all_batch:
	python3 batch.py

replace:
	cd step2_spritesheet_to_generative_sheet && npm run replace ../ultraRares && cd ..

preview:
	python3 step3_generative_sheet_to_output/preview.py

regenerate:
	python3 regenerate.py
