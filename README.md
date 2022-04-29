# Welcome to the **Generative GIF Engine v2.0.4** 🐤

[8 minute read]

This python and node app generates layered-based gifs to create NFT gif art! It is faster, simpler, and
produces higher quality gifs than any other open source gif generative tool out there. Export your animation as a png image sequence,
organize your layer folders with rarity, and the code does the rest! I plan to actively maintain this repo
and enhance it with various tools for months to come so be sure to ask questions in the discussion and write issues.

There are three steps:

1. [Python] Converts layers into spritesheets using [PIL](https://pillow.readthedocs.io/en/stable/). This step can be skipped if you already have the spritesheets, but
   is useful if you want to start with png files and makes the artist's life easier!
2. [Node] Create generative spritesheets from the layers from step 1.
   - The original idea came from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) but now most of the code in this step is forked from [nftchef's Generative Engine](https://github.com/nftchef/art-engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node). Please check out Hashlip's [📺 Youtube](https://www.youtube.com/channel/UC1LV4_VQGBJHTJjEWUmy8nA) / [👄 Discord](https://discord.com/invite/qh6MWhMJDN) / [🐦 Twitter](https://twitter.com/hashlipsnft) / [ℹ️ Website](https://hashlips.online/HashLips) for a more in depth explanation on how the generative process works.
3. [Python + gifski] Convert spritesheets to gifs using Python and [gifski](https://github.com/ImageOptim/gifski).

Checkout this [Medium post](https://jalagar-eth.medium.com/how-to-create-generative-animated-nft-art-in-under-an-hour-e7dab1785c56) and [How does it work?](#how-does-it-work) for more information!

Here's an example final result (or you can download the code and run it and see more bouncing balls :)). It is also pushed to production
on [OpenSea](https://opensea.io/collection/genesis-bouncing-ball).

<img src="./README_Assets/0.gif" width="200"><img src="./README_Assets/1.gif" width="200"><img src="./README_Assets/2.gif" width="200"><img src="./README_Assets/3.gif" width="200">

**EDIT tool now supports z-index/stacking, grouping and if-then statements**. See [nftchef's docs](https://generator.nftchef.dev/readme/) for more information. Here is an example of having one layer that is both in front and behind the ball.

<img src="./README_Assets/z-index/0.gif" width="200">

## Requirements

Install an IDE of your preference. [Recomended](https://code.visualstudio.com/download)

Install the latest version of [Node.js](https://nodejs.org/en/download/)

- Run this command on your system terminal to check if node is installed:

        node -v

Install the latest version of [Python 3](https://www.python.org/downloads/). I am currently using 3.8.1 but anything above 3.6 should work.

- Run this command on your system terminal to check if node is installed:

        python3 --version

Install [gifski](https://gif.ski/). I recommend using brew `brew install gifski` if you're on Mac OSX. If you don't have brew you can install it using [brew](https://brew.sh/) on Mac OSX. Or if you're on Windows
you can install it using [Chocolatey](https://community.chocolatey.org/): `choco install gifski`.

If none of those methods work, follow instructions on gifski [gifski Github](https://github.com/ImageOptim/gifski). Gifski is crucial for this tool because it provides the best gif generation
out of all the tools I checked out (PIL, imageio, ImageMagic, js libraries).

If you plan on developing on this repository, run `pre-commit` to install pre-commit hooks.

### Installation

- Download this repo and extract all the files.
- Run this command on your root folder using the terminal:

        make first_time_setup

If you have any issues with this command, try running each separate command:

       python3 -m pip install --upgrade Pillow && pip3 install -r requirements.txt

       cd step2_spritesheet_to_generative_sheet; npm i

       brew install gifski

Each environment can be different, so try Google your issues. I'll add a few known issues below:

Known issues:

- [M1 Mac: Canvas prebuild isn't built for ARM computers](https://github.com/Automattic/node-canvas/issues/1825) so you need to install it [from their Github](https://github.com/Automattic/node-canvas/wiki#installation-guides)
- `cd` command might not work on Windows depending on what Terminal you are using. You may have to edit the `Makefile` to use `CHDIR` or the equivalent.
- If you're on Windows 10 you might get a 'make' is not recognized. Try follow these [instructions](https://pakstech.com/blog/make-windows/#:~:text=make%20%3A%20The%20term%20'make',choose%20Path%20and%20click%20Edit). Otherwise you can copy and paste the instructions manually in `Makefile`.
- If you're on Windows you might get an error where 'python3' does not exist, try modify the `Makefile` and replace python3 with python. Thank you!
- If you don't have brew installed, look at [gifski](https://github.com/ImageOptim/gifski) docs for another way to install gifski.

## How to run?

Load the png or gif files into the `/layers` folder where each layer is a folder, and each folder contains
another attribute folder which contains the individual frames and a rarity percentage. For example if you wanted
a background layer you would have `/layers/background/blue#20` and `/layers/background/red#20`.

In each attribute folder, the frames should be named `0.png` -> `X.png` or `0.gif`. See code or [step 1](#step-1) for folder structure. The code
will handle any number of layers, so you could have a layer with two frames, another layer with one frame, and another with 20 frames,
and as long as you pass `numberOfFrames` = 20, then the layers will be repeated until they hit 20.

Update `global_config.json` with:

1.  **`'totalSupply'`** : total number of gifs to generate.
2.  **`'height'`** : height of one frame. This should be equal to width.
3.  **`'width'`** : width of one frame. This should be equal to height.
4.  **`'framesPerSecond'`** : number of frames per second. This will not be exact because PIL takes in integer milliseconds per frame
    (so 12fps = 83.3ms per frame but rounded to an int = 83ms). This will not be recognizable by the human eye, but worth calling out.
5.  **`'numberOfFrames'`** : number of total frames. For example you could have 24 frames, but you want to render it 12fps.
6.  **`'description'`** : description to be put in the metadata.
7.  **`'baseUri'`** : baseUri to be put in the metadata.
8.  **`'saveIndividualFrames'`** : this is if you want to save the individual final frames, for example if you want to let people pick just one frame for a profile page.
9. **`'layersFolder'`**: this is the folder that you want to use for the layers. The default is `layers`, but this allows you to have multiple versions of layers and run them side by side. The current repo has four example folders, `layers`, `layers_grouping`, `layers_if_then`, `layers_z_index` which all demonstrate features from [nftchef's repo](https://generator.nftchef.dev/).
10. **`'quality'`**: quality of the gif, 1-100.
11. **`'gifTool'`**: pick which gif generation method to use, `gifski` or `imageio`. Gifski is better overall, but some people were having issues with it on Linux. Also `imageio` will work for more pixel art, so if you don't want to download Gifski you can set this to `imageio`.

Update `step2_spritesheet_to_generative_sheet/src/config.js` with your `layerConfigurations`. If you want the basic
configuration, just edit `layersOrder`, but if you want to take advantage of [nftchef's repo](https://generator.nftchef.dev/), then scroll through the file for some examples and modify `layerConfigurations` accordingly.

- To run the process end to end run:

        make all

Your output gifs and JSON metadata will appear in `build/gifs` and `build/json`. Try it yourself with the default settings
and layers!

## How does it work?

### Step 1

In order to get [nftchef's Generative Gif Engine](https://github.com/nftchef/art-engine) to work, the input
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

**EDIT tool now supports z-index/stacking, grouping and if-then statements**. See [nftchef's docs](https://generator.nftchef.dev/readme/) for more information. The layers in this step will have to match the format expected in step 2. See the example layer folders for some more info.

**EDIT tool now supports gif layers**. You can provide layers as gifs and the code will split the gif into
frames. See `layers_gif_example`. It will create a temp folder in step1_layers_to_spritesheet/temp with the
resulting separate frames, and then will parse through that folder to create the output. Make sure `numberOfFrames`
is set in global_config.json.

### Step 2

Step 2 takes the spritesheets from step 1 and generates all possible combinations based on rarity. This is where
all the magic happens! The output is a bunch of spritesheets with all the layers layered on top of each other.

The original idea came from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) but now most of the code in this step is forked from [nftchef's Generative Engine](https://github.com/nftchef/art-engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node). 
Please check out Hashlip's [📺 Youtube](https://www.youtube.com/channel/UC1LV4_VQGBJHTJjEWUmy8nA) / [👄 Discord](https://discord.com/invite/qh6MWhMJDN) / [🐦 Twitter](https://twitter.com/hashlipsnft) / [ℹ️ Website](https://hashlips.online/HashLips) for a more in depth explanation on how the generative process works.

I recently modified this section to use the code from [nftchef's Generative Engine](https://github.com/nftchef/art-engine) which adds the following features:
- if-then statements. You can have generative art code that says if this layer, then select these layers. There is an example layers under `layers_if_then` which has logic for if the ball is pink, wear a birthday or cowboy hat, or if the ball is purple, wear a mini ball hat. See [nftchef's docs](https://generator.nftchef.dev/readme/branching-if-then) for more information.
- grouping statements. You can now group traits into certain groups. So in the `layers_grouping` we have common balls and hats, and rare balls and hats, and the first `totalSupply - 1` balls are common, and the last one is rare.
- z-index otherwise known as stack order. You can now have multiple stacks for the same layer, for example a basketball hoop landscape which has art in front and behind the ball. See [nftchef's docs](https://generator.nftchef.dev/readme/z-index-layer-order) for more information.

You will need to update `global_config.json` and also update `layerConfigurations` in `step2_spritesheet_to_generative_sheet/src/config.js`.

You can run only step 2 by running:

        make step2

Example output with the `layers` folder (only first 4 displayed, but there are 16 total):

<img src="./README_Assets/step2/0.png" width="1000">
<img src="./README_Assets/step2/1.png" width="1000">
<img src="./README_Assets/step2/2.png" width="1000">
<img src="./README_Assets/step2/3.png" width="1000">

Example output with the `layers_z_index` folder:

<img src="./README_Assets/z-index/0.png" width="200">

### Step 3

Step 3 takes the spritesheets from step 2 and creates gifs in `builds/gifs`. This is where Python libraries really shine. Initially I used [PIL](https://pillow.readthedocs.io/en/stable/), but found some issues with pixel quality.

In MichaPipo's original repo, they used javascript libraries to
create the gifs. These copied pixel by pixel, and the logic was a bit complicated. Creating just 15 gifs would take 4 minutes, and I noticed
some of the pixel hex colors were off. Also depending on CPU usage, the program would crash. I spent days debugging, when I just decided to
start from scratch in another language.

I then tried imageio, and a few Python libraries, but they all had some issues
generating gifs. 

I spent weeks finding the best tool for this job, and came across [gifski](https://gif.ski/). This
creates incredibly clean gifs and worked the best.

Now, generating 15 gifs takes < 30 seconds and renders with perfect pixel quality!

You can change the `framesPerSecond` in `global_config.json` and you can run only step 3 by running:

        make step3

This allows you to not have to regenerate everything to play around with fps.

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

**NOTE**
`imageio` was by far the best Python library, so I added it as an option in case you don't want
to download `gifski`. `imageio` will work for most pixel art and I know some people had issues
with `gifski` on Linux (not Windows or Mac).

You can set which gif tool to use in `global_config.json` by setting `gifTool` to either `gifski` (default) or `imageio`.

### Rarity stats

You can check the rarity stats of your collection with:

        make rarity

### Provenance Hash Generation - IN PROGRESS

THIS SECTION IS STILL IN PROGRESS, IT DOES NOT GENERATE PROVENANCE HASH CORRECTLY

If you need to generate a provenance hash (and, yes, you should, [read about it here](https://medium.com/coinmonks/the-elegance-of-the-nft-provenance-hash-solution-823b39f99473) ), make sure the following in config.js is set to `true`

```js
// IF you need a provenance hash, turn this on
const hashImages = true;
```

Then…
After generating images and data, each metadata file will include an `imageHash` property, which is a Keccak256 hash of the output image.

### To generate the **Provenance Hash**

run the following util

```
make provenance
```

**The Provenance information is saved** to the build directory in `_prevenance.json`. This file contains the final hash as well as the (long) concatenated hash string.

\*Note, if you regenerate the images, **You will also need to regenerate this hash**.

### Update your metadata info

You can change the description and base Uri of your metadata even after running the code by updating `global_config.json` and running:

        make update_json

### Solana metadata

🧪 BETA FEATURE

After running `make all` you can run generate the Solana metadata in two steps:
- Edit `step2_spritesheet_to_generative_sheet/Solana/solana_config.js`
- `make solana` to generate the Solana metadata. This will create an output folder `build/solana`with the gifs and the metadata.

Most of the code comes from [nftchef](https://github.com/nftchef/art-engine/blob/nested-folder-structure/utils/metaplex.js).

I have not tried this on any test net or production Solana chain, so please flag any issues or create a PR to fix them!

## IMPORTANT NOTES

All of the code in step1 and step3 was written by me. The original idea for the repo came from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) but now most of the code in step 2 is forked from [nftchef's Generative Engine](https://github.com/nftchef/art-engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node).

**_ Things to work on: _**

- [X] Update step2 with latest features from [Hashlips art engine](https://github.com/HashLips/hashlips_art_engine).
- [X] Add layer functionality to step2 from [nftchef art engine](https://github.com/nftchef/art-engine).
- [X] Allow passing in gifs into step1 to split into spritesheets.

**FAQ**

Q: Why did you decide to use Python for step 1 and step 3?

A: I found that Python [PIL](https://pillow.readthedocs.io/en/stable/) work better and faster than JS libraries, and the code is simpler for me. Initially I tried PIL, imageio, and a few Python libraries, but they all had issues
generating gifs. I spent weeks finding the best tool for this job, and came across [gifski](https://gif.ski/). This
creates incredibly clean gifs and worked the best.

My philosophy is pick the right tool for the right job. If someone finds a better library for this specific job, then let me know!

Q: Why didn't you use Python for step 2?

A: The NFT dev community which writes the complicated logic for generative art mainly codes in javascript. I want to make it easy to update
my code and incorporate the best features of other repos as easily as possible, and porting everything to Python would be a pain. You can imagine
step 1 and step 3 are just helper tools in Python, and step 2 is where most of the business logic comes from.

Be sure to follow me for more updates on this project:

[Twitter](https://twitter.com/jalagar_eth)

[GitHub](https://github.com/jalagar/)

[Medium](https://jalagar-eth.medium.com/)

My ETH address is 0x4233EfcB109BF6618071759335a7b9ab84F2F4f3 if you feel like being generous :). I just quit my job to work on NFTs full time
so anything is appreciated.

If you want to see this code in action, we're using it for my fitness and mental health company Fitness Friends:

[Twitter](https://twitter.com/FitFriends_NFT)

[Website](https://www.fitnessfriends.io/)
