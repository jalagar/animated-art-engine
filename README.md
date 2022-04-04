# Welcome to the **Generative GIF Engine v2.0.0** 🐤

[8 minute read]

This python and node app generates layered-based gifs to create NFT gif art! It is faster, simpler, and
produces higher quality gifs than any other open source gif generative tool out there. Export your animation as a png image sequence,
organize your layer folders with rarity, and the code does the rest! I plan to actively maintain this repo
and enhance it with various tools for months to come so be sure to ask questions in the discussion and write issues.

There are three steps:

1. [Python] Converts layers into spritesheets using [PIL](https://pillow.readthedocs.io/en/stable/). This step can be skipped if you already have the spritesheets, but
   is useful if you want to start with png files and makes the artist's life easier!
2. [Node] Create generative spritesheets from the layers from step 1.
   - Most of the code in this step is forked from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node). Please check out his [📺 Youtube](https://www.youtube.com/channel/UC1LV4_VQGBJHTJjEWUmy8nA) / [👄 Discord](https://discord.com/invite/qh6MWhMJDN) / [🐦 Twitter](https://twitter.com/hashlipsnft) / [ℹ️ Website](https://hashlips.online/HashLips) for a more in depth explanation on how the generative process works.
3. [Python] Convert spritesheets to gifs using [PIL](https://pillow.readthedocs.io/en/stable/).

Checkout this [Medium post](https://jalagar-eth.medium.com/how-to-create-generative-animated-nft-art-in-under-an-hour-e7dab1785c56) and [How does it work?](#how-does-it-work) for more information!

Here's an example final result (or you can download the code and run it and see more bouncing balls :)). It is also pushed to production
on [OpenSea](https://opensea.io/collection/genesis-bouncing-ball).

<img src="./README_Assets/0.gif" width="200"><img src="./README_Assets/1.gif" width="200"><img src="./README_Assets/2.gif" width="200"><img src="./README_Assets/3.gif" width="200">

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

If you have any issues with this command, try running each separate command:

       python3 -m pip install --upgrade Pillow && pip3 install -r requirements.txt

       cd step2_spritesheet_to_generative_sheet; npm i

Each environment can be different, so try Google your issues. I'll add a few known issues below:

Known issues:

- [Canvas prebuild isn't built for ARM computers](https://github.com/Automattic/node-canvas/issues/1825) so you need to install it [from their Github](https://github.com/Automattic/node-canvas/wiki#installation-guides)
- `cd` command might not work on Windows depending on what Terminal you are using. You may have to edit the `Makefile` to use `CHDIR` or the equivalent.


## How to run?

Load the png files into the `/layers` folder where each layer is a folder, and each folder contains
another attribute folder which contains the individual frames and a rarity percentage. For example if you wanted
a background layer you would have `/layers/background/blue#20` and `/layers/background/red#20`.

In each attribute folder, the frames should be named `0.png` -> `X.png`. See code or [step 1](#step-1) for folder structure. The code
will handle any number of layers, so you could have a layer with two frames, another layer with one frame, and another with 20 frames,
and as long as you pass `numberOfFrames` = 20, then the layers will be repeated until they hit 20.

Update `global_config.json` with:

1.  **`'totalSupply'`** : total number of gifs to generate.
2.  **`'height'`** : height of one frame. This should be equal to width.
3.  **`'width'`** : width of one frame. This should be equal to height.
4.  **`'layersOrder'`** : list of layers in order of background to foreground.
5.  **`'quality'`** : quality of images. See [PIL docs](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg) for more info. 0 - worst, 95 - best.
6.  **`'framesPerSecond'`** : number of frames per second. This will not be exact because PIL takes in integer milliseconds per frame
    (so 12fps = 83.3ms per frame but rounded to an int = 83ms). This will not be recognizable by the human eye, but worth calling out.
7.  **`'numberOfFrames'`** : number of total frames. For example you could have 24 frames, but you want to render it 12fps.
8.  **`'description'`** : description to be put in the metadata.
9.  **`'baseUri'`** : baseUri to be put in the metadata.
10. **`'saveIndividualFrames'`** : this is if you want to save the individual final frames, for example if you want to let people pick
    just one frame for a profile page

- To run the process end to end run:

          make all

Your output gifs and JSON metadata will appear in `build/gifs` and `build/json`. Try it yourself with the default settings
and layers!

## How does it work?

### Step 1

In order to get [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) to work, the input
layers needs to be in [Sprite Sheet](https://gamedevelopment.tutsplus.com/tutorials/an-introduction-to-spritesheet-animation--gamedev-13099).
However this is tedious and unintuitive for many artists who use tools that export individual images.

Step 1 simply converts individual images to spritesheets with the rarity percentage. You provide the various layers in the
`/layers` folder with the rarity in the folder name. Each image should be numbered from 0 -> X, and only accepts `.png`.

**If you do not include the rarity weight in the attribute folder name, that attribute will be ignored**

You can provide any number of frames in each layer folder, the code will repeat them up until it hits `numberOfFrames`.
It will also trim any that have too many frames.

Example layers folder structure with four layers
and two traits each layer:

```
layers
└───Background
│   └───Grey#50
│       │   0.png
│   └───Pink#50
│       │   0.png
└───Ball
│   └───Blue#50
│       │   0.png
│       │   1.png
│       │   2.png
│       │   ...
│   └───Green#50
│       │   0.png
│       │   1.png
│       │   2.png
│       │   ...
└───Hat
│   └───Birthday#50
│       │   0.png
│       │   1.png
│       │   2.png
│       │   ...
│   └───Cowboy#50
│       │   0.png
│       │   1.png
│       │   2.png
│       │   ...
└───Landscape
│   └───Cupcake#50
│       │   0.png
│   └───Green Tower#50
│       │   0.png
```

**Example layer**:

**Background**:

Grey:

<img src="./README_Assets/layers/Background/Grey/0.png" width="200">

Pink:

<img src="./README_Assets/layers/Background/Pink/0.png" width="200">

**Ball**:

Blue:

<img src="./README_Assets/layers/Ball/Blue/0.png" width="150"><img src="./README_Assets/layers/Ball/Blue/1.png" width="150"><img src="./README_Assets/layers/Ball/Blue/2.png" width="150"><img src="./README_Assets/layers/Ball/Blue/3.png" width="150"><img src="./README_Assets/layers/Ball/Blue/4.png" width="150">...

Green:

<img src="./README_Assets/layers/Ball/Green/0.png" width="150"><img src="./README_Assets/layers/Ball/Green/1.png" width="150"><img src="./README_Assets/layers/Ball/Green/2.png" width="150"><img src="./README_Assets/layers/Ball/Green/3.png" width="150"><img src="./README_Assets/layers/Ball/Green/4.png" width="150">...

**Hat**:

Birthday:

<img src="./README_Assets/layers/Hat/Birthday/0.png" width="150"><img src="./README_Assets/layers/Hat/Birthday/1.png" width="150"><img src="./README_Assets/layers/Hat/Birthday/2.png" width="150"><img src="./README_Assets/layers/Hat/Birthday/3.png" width="150"><img src="./README_Assets/layers/Hat/Birthday/4.png" width="150">...

Cowboy:

<img src="./README_Assets/layers/Hat/Cowboy/0.png" width="150"><img src="./README_Assets/layers/Hat/Cowboy/1.png" width="150"><img src="./README_Assets/layers/Hat/Cowboy/2.png" width="150"><img src="./README_Assets/layers/Hat/Cowboy/3.png" width="150"><img src="./README_Assets/layers/Hat/Cowboy/4.png" width="150">...

**Landscape**:

Cupcake:

<img src="./README_Assets/layers/Landscape/Cupcake/0.png" width="150">

Green Tower:

<img src="./README_Assets/layers/Landscape/Green Tower/0.png" width="150">

I am using python here instead of javascript libraries because I have found that image processing using
[PIL](https://pillow.readthedocs.io/en/stable/) is much faster and without lossy quality than javascript.
These benefits are much clearer in step 3.

You can run only step1 by running:

        make step1

This will convert the pngs into spritesheets and the output will look something like this:

Output:

**Background**:

Grey#50.png:

<img src="./README_Assets/step1/Background/Grey.png" width="1000">

Pink#50.png:

<img src="./README_Assets/step1/Background/Pink.png" width="1000">

**Ball**:

Blue#50.png:

<img src="./README_Assets/step1/Ball/Blue.png" width="1000">

Green#50.png:

<img src="./README_Assets/step1/Ball/Green.png" width="1000">

**Hat**:

Birthday#50.png:

<img src="./README_Assets/step1/Hat/Birthday.png" width="1000">

Cowboy#50.png:

<img src="./README_Assets/step1/Hat/Cowboy.png" width="1000">

**Landscape**:

Cupcake#50.png:

<img src="./README_Assets/step1/Landscape/Cupcake.png" width="1000">

Green Tower#50.png:

<img src="./README_Assets/step1/Landscape/Green Tower.png" width="1000">

### Step 2

Step 2 takes the spritesheets from step 1 and generates all possible combinations based on rarity. This is where
all the magic happens! The output is a bunch of spritesheets with all the layers layered on top of each other.

Most of the code in this step is forked from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node). Please check out his [📺 Youtube](https://www.youtube.com/channel/UC1LV4_VQGBJHTJjEWUmy8nA) / [👄 Discord](https://discord.com/invite/qh6MWhMJDN) / [🐦 Twitter](https://twitter.com/hashlipsnft) / [ℹ️ Website](https://hashlips.online/HashLips) for a more in depth explanation on how the generative process works.

There shouldn't be any extra configurations needed outside of `global_config.json`, but you can check out `step2_spritesheet_to_generative_sheet/src/config.js` for more configurations.

You can run only step 2 by running:

        make step2

Example output (only first 4 displayed, but there are 16 total):

<img src="./README_Assets/step2/0.png" width="1000">
<img src="./README_Assets/step2/1.png" width="1000">
<img src="./README_Assets/step2/2.png" width="1000">
<img src="./README_Assets/step2/3.png" width="1000">

### Step 3

Step 3 takes the spritesheets from step 2 and creates gifs in `builds/gifs`. This is where Python and [PIL](https://pillow.readthedocs.io/en/stable/) really shine. In MichaPipo's original repo, they used javascript libraries to
create the gifs. These copied pixel by pixel, and the logic was a bit complicated. Creating just 15 gifs would take 4 minutes, and I noticed
some of the pixel hex colors were off. Also depending on CPU usage, the program would crash. I spent days debugging, when I just decided to
start from scratch in another language.

Now, generating 15 gifs takes < 30 seconds and renders with perfect pixel quality!

You can change the `quality` and `framesPerSecond` in `global_config.json` and you can run only step 3 by running:

        make step3

This allows you to not have to regenerate everything to play around with quality and fps.

Example output with all 16 permutations (click on each gif for the 1000x1000 version):

<img src="./README_Assets/step3/0.gif" width="150"><img src="./README_Assets/step3/1.gif" width="150"><img src="./README_Assets/step3/2.gif" width="150"><img src="./README_Assets/step3/3.gif" width="150"><img src="./README_Assets/step3/4.gif" width="150"><img src="./README_Assets/step3/5.gif" width="150"><img src="./README_Assets/step3/6.gif" width="150"><img src="./README_Assets/step3/7.gif" width="150"><img src="./README_Assets/step3/8.gif" width="150"><img src="./README_Assets/step3/9.gif" width="150"><img src="./README_Assets/step3/10.gif" width="150"><img src="./README_Assets/step3/11.gif" width="150"><img src="./README_Assets/step3/12.gif" width="150"><img src="./README_Assets/step3/13.gif" width="150"><img src="./README_Assets/step3/14.gif" width="150"><img src="./README_Assets/step3/15.gif" width="150">

If you set `saveIndividualFrames` to `true` in `global_config.json`, it will also split the gifs into individual frames and save them in
`images`. This is useful if you want people to be able to choose a single frame for a profile picture.

Some metrics:

MichaPipo's Generative Gif Engine:

- 15 NFT - 5 minutes with sometimes incorrect pixels.
- 100 NFT - one hour (with the computer being almost unusable).

New Generative Gif Engine:

- 15 NFT - 30 seconds with no pixel issues.
- 100 NFT - 3 minutes and 17 seconds with no pixel issues.
- 1000 NFT - 45 minutes with no pixel issues and no CPU issues.

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
My philosophy is pick the right tool for the right job. If someone finds a better library for this specific job, then let me know!

Q: Why didn't you use Python for step 2?

A: The NFT dev community which writes the complicated logic for generative art mainly codes in javascript. I want to make it easy to update
my code and incorporate the best features of other repos as easily as possible, and porting everything to Python would be a pain. You can imagine
step 1 and step 3 are just helper tools in Python, and step 2 is where most of the business logic comes from.

Be sure to follow me for more updates on this project:

[Twitter](https://twitter.com/jalagar_eth)

[GitHub](https://github.com/jalagar/)

[Medium](https://jalagar-eth.medium.com/)
