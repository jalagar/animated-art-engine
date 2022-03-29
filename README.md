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

Checkout this [Medium post]() for more information!

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

This should install python and node dependencies.

## How to run?

Load the png files into the `/layers` folder where each layer is a folder, and each folder contains
another attribute folder which contains the individual frames. They should be named `0.png` -> `X.png` and
there should be a `rarity.json` file with the rarity defined. See code or [step 1](# Step 1) for folder structure.

Update `global_config.json` with:

1.  **`'totalSupply'`** : total number of NFTs to generate.
2.  **`'height'`** : height of one frame. This should be equal to width.
3.  **`'width'`** : width of one frame. This should be equal to height.
4.  **`'layersOrder'`** : list of layers in order of background to foreground.
5.  **`'quality'`** : quality of images. See [PIL docs](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg) for more info. 0 - worst, 95 - best.
6.  **`'framesPerSecond'`** : number of frames per second. This will not be exact because PIL takes in milliseconds per frame (so 12fps = 83.3ms per
    frame), but PIL takes in an integer. This will not be recognizable by the human eye, but worth calling out.
7.  **`'numberOfFrames'`** : number of total frames. For example you could have 24 frames, but you want to render it 12fps.
8.  **`'description'`** : description to be put in the metadata.
9.  **`'baseUri'`** : baseUri to be put in the metadata.
10. **`'saveIndividualFrames'`** : this is if you want to save the individual final frames.

Run `make all`. Your output gifs and JSON metadata will appear in `build/gifs` and `build/json`. Try it yourself with the default settings
and layers!

## How does it work?

### Step 1

In order to get [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine), the input layers needs to be in [Sprite Sheet](https://gamedevelopment.tutsplus.com/tutorials/an-introduction-to-spritesheet-animation--gamedev-13099). However this is tedious and
unintuitive for many artists who use tools that export individual images.

Step 1 simply converts individual images to spritesheets. You provide the various layers in the
`/layers` folder. Each image should be numbered from 0 -> X, and only accepts `.png`. There should
also be a `rarity.json` in each layer folder which looks like:

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
│       │   rarity.json
│       │   0.png
│   └───pink
│       │   rarity.json
│       │   0.png
└───ball
│   └───red
│       │   rarity.json
│       │   0.png
│       │   1.png
│       │   2.png
│       │   3.png
│       │   4.png
│   └───blue
│       │   rarity.json
│       │   0.png
│       │   1.png
│       │   2.png
│       │   3.png
│       │   4.png
```

Example layers:
background:

grey:

0.png: <img src="./README_Assets/layers/background/grey/0.png" width="200">

pink:

0.png: <img src="./README_Assets/layers/background/pink/0.png" width="200">

ball:

red:

0.png: <img src="./README_Assets/layers/ball/red/0.png" width="200"> 1.png: <img src="./README_Assets/layers/ball/red/1.png" width="200"> 2.png: <img src="./README_Assets/layers/ball/red/2.png" width="200"> 3.png: <img src="./README_Assets/layers/ball/red/3.png" width="200"> 4.png: <img src="./README_Assets/layers/ball/red/4.png" width="200"> ...

blue:

0.png: <img src="./README_Assets/layers/ball/blue/0.png" width="200"> 1.png: <img src="./README_Assets/layers/ball/blue/1.png" width="200"> 2.png: <img src="./README_Assets/layers/ball/blue/2.png" width="200"> 3.png: <img src="./README_Assets/layers/ball/blue/3.png" width="200"> 4.png: <img src="./README_Assets/layers/ball/blue/4.png" width="200"> ...

I am using python here instead of javascript libraries because I have found that image processing using
[PIL](https://pillow.readthedocs.io/en/stable/) is much faster and without lossy quality than javascript.
These benefits are much clearer in step 3.

You can run only step1 by running:

        make step1

This will convert the pngs into spritesheets and the output will look something like this:

Output:

background:

grey:

grey#20.png: <img src="./README_Assets/step1/background/grey#20.png" width="1000">

pink:

pink#20.png: <img src="./README_Assets/step1/background/pink#20.png" width="1000">

ball:

blue:

blue#20.png: <img src="./README_Assets/step1/ball/blue#20.png" width="1000">

red:

red#20.png: <img src="./README_Assets/step1/ball/red#20.png" width="1000">

### Step 2

Step 2 takes the spritesheets from step 1 and generates all possible combinations based on rarity. This is where
all the magic happens! The output is a bunch of spritesheets with all the layers layered on top of each other.

Most of the code in this step is forked from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node). Please check out his [📺 Youtube](https://www.youtube.com/channel/UC1LV4_VQGBJHTJjEWUmy8nA) / [👄 Discord](https://discord.com/invite/qh6MWhMJDN) / [🐦 Twitter](https://twitter.com/hashlipsnft) / [ℹ️ Website](https://hashlips.online/HashLips)!

You can run only step 2 by running:

        make step2

Example output:

<img src="./README_Assets/step2/0.png" width="1000">
<img src="./README_Assets/step2/1.png" width="1000">
<img src="./README_Assets/step2/2.png" width="1000">
<img src="./README_Assets/step2/3.png" width="1000">

### Step 3

Step 3 takes the spritesheets from step 2 and creates gifs in `builds/gifs`. It also creates frame by frame in `builds/images` as well. This
is where Python and [PIL](https://pillow.readthedocs.io/en/stable/) really shine. In MichaPipo's original repo, they used javascript libraries to
create the gifs. These copied pixels by pixels, and the logic was a bit complicated. Creating just 15 gifs would take 4 minutes, and I noticed
some of the pixel hex colors were off. Also depending on CPU usage, the program would crash. I spent days debugging, when I just decided to
start from scratch in another language.

Now, generating 15 gifs takes < 30 seconds and renders with perfect pixel quality!

You can change the `quality` and `framesPerSecond` in `global_config.json` and you can run only step 3 by running:

        make step3

This allows you to not have to regenerate everything to play around with quality and fps.

Example output:

<img src="./README_Assets/step3/0.gif" width="500"><img src="./README_Assets/step3/1.gif" width="500"><img src="./README_Assets/step3/2.gif" width="500">
<img src="./README_Assets/step3/3.gif" width="500">

If you set `saveIndividualFrames` to `true` in `global_config.json`, it will also split the gifs into individual frames and save them in
`images`. This is useful if you want people to be able to choose a single frame for a profile picture.

### Rarity stats

You can check the rarity stats of your collection with:

        make rarity

### Update your metadata info

You can change the description and base Uri of your metadata even after running the code by updating `global_config.json` and running:

        make update_json

## IMPORTANT NOTES

All of the code in step1 and step3 was written by me, and most of the code in this step is forked from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node).

**_ Things to work on: _**

- [ ] Update step2 with latest features from [Hashlips art engine](https://github.com/HashLips/hashlips_art_engine).
- [ ] Add layer functionality to step2 from [nftchef art engine](https://github.com/nftchef/art-engine).
- [ ] Allow passing in gifs into step1 to split into spritesheets.

**FAQ**

Q: Why did you decide to use Python for step 1 and step 3?
A: I found that Python [PIL](https://pillow.readthedocs.io/en/stable/) works better and faster than JS libraries, and the code is simpler for me.
My philosphy is pick the right tool for the right job. If someone finds a better library for this specific job, then let me know!

Q: Why didn't you use Python for step 2?
A: The NFT dev community which writes the complicated logic for generative art mainly writes in javascript. I want to make it easy to update
my code and incorporate the best features of other repos as easily as possible, and porting everything to Python would be a pain.

Be sure to follow me for more updates on this project:

[Twitter](https://twitter.com/jalagar_eth)
[GitHub](https://github.com/jalagar/)
[Medium](https://jalagar-eth.medium.com/)
