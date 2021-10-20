# Welcome to the _Generative GIF Engine v1.0.0_

## REQUIREMENTS
* The source png files must be a series of evenly spaced frames horizontally.
* sort your assets by folders on the 'layers' directory.
* This code requires [Node.js] installment.
* Before running the code, type the following comand on the terminal:

      npm install

## ADJUSTMENTS
Make sure to make the folowing adjustments before running the program.
[config.js]

   1) Change you nft description in _'description'_.
   2) Change the Uri in _'baseUri'_.
   3) Update your folders order in _'layersOrder'_.
   4) Adjust the size of the canvas on _'format'_ based on the size of your sprite sheet.
   5) Be sure to check _'editionSize'_, this option will determine the number of images generated.

## HOW TO USE
In order to everything work properly, the scripts must be runned in order.

When everything is ready you need to go to the terminal and run:

    node index.js

This will output your png sprite sheets on a new folder named 'build'.

After index.js was runned, in order to generate a gif file now you have to run:

    node script.js

Running script.js will prompt questions to input the gif format:

        1) _'Enter folder directory:'_
            Right click on your input folder ('build' folder) and select 'copy path', copy the path on this question and then press 'enter' to continue.

        2)_'Enter name (no extension). Leave blank to convert all:'_
            Enter a file name inside the build folder to specifically convert that file to .gif
            If the space is leaved blank, all the .png files inside the selected folder will be automatically converted to a .gif file.

        3)_'Enter frame frames per second:'_
            Enter the desired frame rate of the gif, the default value for this space is 30.

        4)_'Enter frame width. Leave blank for auto:'_
            Enter the desired frame width, if the space is leaved blank, the default frame width will be the same as the frame heigth.

        5)_'Enter transparent color in hex:'_
            Enter the desired backgroung color in hex format, leave blank for transparent color.

        6)_'Enter quality (1 = best; 20 = worst):'_
            Enter the desired quality output of your gif. The default value of this space is 10.

        7)_'Proceed with conversion?'_
            Type 'y' if you want to proceed with conversion, type 'n' to cancel the process.

After you proceed with the conversion, the converted .gif files will be located on the previously selected folder.

## IMPORTANT NOTES
* This current version does not support some features of the newest HashLips engine, this was build based on a very early version of hashlips art engine.
* Metadata.json is being created for the .png files instead of the .gif files.
* This version is not suited to create full gif nft collections.

Hopefully i can release new and more efficient versions of this code, so please stay tuned.

_Things to work on:_

    - Add a rarity system and more hashlips code features.
    - Improve efficiency by just needing to run one single .js file.
    - Create metadata for the gif files.
    - Improve performance.

Be sure to follow me for more updates on this project:

[MichaPipo Twitter](https://twitter.com/MichaPipo)

[MichaPipo GitHub](https://github.com/MichaPipo)

Also be sure to follow HashLips for a better understanding of this code and for a possible official release of his code with gif support:

[HashLips YouTube](https://www.youtube.com/channel/UC1LV4_VQGBJHTJjEWUmy8nA)

[HashLips Telegram](https://t.me/hashlipsnft)

[HashLips Twitter](https://twitter.com/hashlipsnft)

[HashLips Website](https://hashlips.online/HashLips)
