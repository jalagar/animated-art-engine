first_time_setup:
	python3 -m pip install --upgrade Pillow
	pip3 install -r requirements.txt
	cd step2_spritesheet_to_generative_sheet; npm i

step1:
	python3 step1_layers_to_spritesheet/build.py

step2:
	cd step2_spritesheet_to_generative_sheet; node index.js

step3:
	python3 step3_generative_sheet_to_gif/build.py

all:
	make step1
	make step2
	make step3

rarity:
	cd step2_spritesheet_to_generative_sheet; node utils/rarity.js

update_json:
	cd step2_spritesheet_to_generative_sheet; node utils/update.js
