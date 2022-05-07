first_time_setup:
	python3 -m pip install --upgrade Pillow && pip3 install -r requirements.txt
	cd step2_spritesheet_to_generative_sheet && npm i

step1:
	python3 step1_layers_to_spritesheet/build.py

step2:
	cd step2_spritesheet_to_generative_sheet && npm run generate

solana:
	cd step2_spritesheet_to_generative_sheet
	npm run generate:solana

tezos:
	cd step2_spritesheet_to_generative_sheet && npm run generate:tezos
	python3 step3_generative_sheet_to_gif/resize.py

provenance:
	cd step2_spritesheet_to_generative_sheet && node utils/provenance.js

step3:
	python3 step3_generative_sheet_to_gif/build.py

all:
	make step1
	make step2
	make step3

rarity:
	cd step2_spritesheet_to_generative_sheet &&node utils/rarityData.js

update_json:
	cd step2_spritesheet_to_generative_sheet && node utils/updateInfo.js

update_json_tezos:
	cd step2_spritesheet_to_generative_sheet && npm run update_info:tezos

all_batch:
	make step1
	make step2
	python3 batch.py

replace:
	cd step2_spritesheet_to_generative_sheet && npm run replace ../ultraRares


preview:
	python3 step3_generative_sheet_to_gif/preview.py
