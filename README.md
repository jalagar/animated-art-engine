# Welcome to the **Generative GIF Engine v2.0.0** 🐤

[5 minute read]

This python and node app generates gifs based on layers to create NFT gif art! It is faster, simpler, and
more dynamic than any other open source gif generative tool out there! I plan to actively maintain this repo
and enhance it with various tools for months to come!

There are three steps:

1. [Python] Converts layers into spritesheets using [PIL](https://pillow.readthedocs.io/en/stable/). This step can be skipped if you already have the spritesheets, but
   is useful if you want to start with png files and makes the artist's life easier!
2. [Node] Create generative spritesheets from the layers from step 1.
   - Most of the code in this step is forked from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node). Please check out his [📺 Youtube](https://www.youtube.com/channel/UC1LV4_VQGBJHTJjEWUmy8nA) / [👄 Discord](https://discord.com/invite/qh6MWhMJDN) / [🐦 Twitter](https://twitter.com/hashlipsnft) / [ℹ️ Website](https://hashlips.online/HashLips)!
3. [Python] Convert spritesheets to gifs using [PIL](https://pillow.readthedocs.io/en/stable/).

Please checkout this [Medium post]() for more information!

## Requirements

Install an IDE of your preference. [Recomended](https://code.visualstudio.com/download)
Install the latest version of [Node.js](https://nodejs.org/en/download/)

- Run this command on your system terminal to check if node is installed:

        node -v


Install the latest version of [Python 3](https://www.python.org/downloads/). I am currently using 3.8.1 but anything above 3.6 should work.

- Run this command on your system terminal to check if node is installed:

        python3 --version

### Installation

- Download this repo and extract all the files.
- Run this command on your root folder using the terminal:

          make first_time_setup

  This should install python and node dependencies. You can use a virtual environment but I will not go into this here.

### Files

- All your assets must have attached a **"rarity weight"** on their file name. Example:

  > `File name` + `#` + `Number` = `File_name#10.png`

- Sort your layers assets into folders and add them to the `'Layer'` directory.
- All your layer assets must be a series of evenly spaced frames horizontally. The number and size of your frames must be consistent in order to work properly.
- This code only works with layers that are in [Sprite Sheet](https://gamedevelopment.tutsplus.com/tutorials/an-introduction-to-spritesheet-animation--gamedev-13099) format. Example:

  ![Sprite_Sheet example](https://github.com/MichaPipo/Generative_Gif_Engine/blob/main/README_Assets/SpriteSheet_test.png)

## How does it work?

# Step 1

In order to get [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine), the input layers needs to be in [Sprite Sheet](https://gamedevelopment.tutsplus.com/tutorials/an-introduction-to-spritesheet-animation--gamedev-13099). However this is tedious and
unintuitive for many artists who use tools that export individual images.

Step 1 simply converts individual images to spritesheets. You provide the various layers in the
`/layers` folder. Each image should be numbered from 0 -> X, and only accepts `.png`. There should
also be a `config.json` in each layer folder which looks like:

```
{
    "rarity": 10
}
```

which specifies the rarity of each layer.

Example layers folder structure:

```
layers
└───background
│   └───grey
│       │   config.json
│       │   0.png
│   └───pink
│       │   config.json
│       │   0.png
└───ball
│   └───red
│       │   config.json
│       │   0.png
│       │   1.png
│       │   2.png
│       │   3.png
│       │   4.png
│   └───blue
│       │   config.json
│       │   0.png
│       │   1.png
│       │   2.png
│       │   3.png
│       │   4.png
```

Example layers:
Background:
grey:
![0.png](https://github.com/MichaPipo/Generative_Gif_Engine/blob/main/README_Assets/layers/background/grey/0.png)
pink:
![0.png](https://github.com/MichaPipo/Generative_Gif_Engine/blob/main/README_Assets/layers/background/pink/0.png)

Ball:
red:
![0.png](https://github.com/MichaPipo/Generative_Gif_Engine/blob/main/README_Assets/layers/ball/red/0.png)
blue:
![0.png](https://github.com/MichaPipo/Generative_Gif_Engine/blob/main/README_Assets/layers/ball/blue/0.png)

I am using python here instead of javascript libraries because I have found that image processing using
[PIL](https://pillow.readthedocs.io/en/stable/) is much faster and without lossy quality than javascript. It
is also much simpler for me to work with.

You can run only step1 by running:

        make step1

## HOW TO USE

### Settings

Before running the code, go to `config.json` where you can make the next changes:

1.  **`'description'`** : the description of your nft that will be written in the metadata.
2.  **`'baseUri'`** : uri where the nft is going to be stored.
3.  **`'layerConfigurations'`** :
    - _'growEditionSizeTo'_ : the amount of images that will be generated.
    - _'layersOrder'_ : the order of generation of the layers, from back to front.
    - _'name'_ : the folder name of your layer.

```js
//Example: creates up to a 100 images with 3 kinds of layers
const layerConfigurations = [
  {
    growEditionSizeTo: 100,
    layersOrder: [
      { name: "Layer_folder_1" },
      { name: "Layer_folder_2" },
      { name: "Layer_folder_3" },
    ],
  },
];
```

4.  **`'shuffleLayerConfiguration'`** : shuffles the generation order of the output images.

5.  **`'debugLogs'`** : prints the debug logs on the terminal.

6.  **`'format`'** : determines the heigth and width of the generated images, make sure this values are the same as your input images.

7.  **`'extraMetadata'`** : add extra metadata to the .json file.

8.  **`'uniqueDnaTorrance'`** : determines the maximum amount of unique images that can be generated.

### Run the code

After everything is setup, you can proceed with the png generation with the next command:

    node index.js

This will create a new directory called `build` that will cointain 2 folders:

- `Json` : here you can find the .json files of each image generated.
- `Gifs` : here you can find the gifs generated by step 3.

When the image generation is finished, you can now proceed with the **png to gif** convertion using the following command:

    node script.js

Running this command will prompt some questions on the terminal where input regarding the gif format will be required:

| Question                              | Description                                                                                                                                             |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. 'Enter folder directory' :         | Select the input folder where png files will be extracted, leave this space blank and press enter for auto (build/images)                               |
| 2. 'Enter name' :                     | Enter a png file name inside the directory to specifically convert that file. Leave blank and press enter to convert everything.                        |
| 3. 'Enter storage folder directory' : | Select the output folder where gif files will be stored. Leave blank and press enter for auto (build/gifs).                                             |
| 4. 'Enter frames per second' :        | Type the desired frames per second value. Press enter for auto (30 fps).                                                                                |
| 5. 'Enter frame width' :              | If your sprite sheet frame width isnt the same as your frame heigth, you can change that value here. leave blank for auto (frame width = frame heigth). |
| 6. 'Enter transparent color' :        | change transparent color using a hex value. leave blank for auto.                                                                                       |
| 7. 'Enter quality' :                  | select the output gif quality (20 = best , 10 = worst). Default value is 10.                                                                            |
| 8. 'Proceed with conversion?' :       | type 'y' to proceed and 'n' to cancel the process.                                                                                                      |

## Utils

On the `utils` directory you can find some tools you can use after you generated your collection.

### Rarity stats

You can check the rarity stats of your collection with:

        node ./utils/rarity.js

### Update your metadata info

You can change the description and base Uri of your metadata even after running the code with:

        node ./utils/update.js

## IMPORTANT NOTES

Most of the code on this repo was originally created by HashLips, this is a modified version created for the nft community interested on gif nft generation.

This version is now suitable for a full collection creation, but there's always things to work on and improve.

Hopefully i can release new and more efficient versions of this code, so please stay tuned.

**_ Things to work on: _**

- [x] Add a rarity system and more hashlips code features.
- [x] Create metadata for .gif files.
- [ ] Improve efficiency by just needing to run one single .js file.

Be sure to follow me for more updates on this project:

[Twitter](https://twitter.com/jalagar_eth)
[GitHub](https://github.com/jalagar/)
[Medium](https://jalagar-eth.medium.com/)
