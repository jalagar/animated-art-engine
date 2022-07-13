# Welcome to the **Generative Animated Engine v3.1.0** 🐤

[8 minute read]

**This repo used to be called jalagar/Generative_Gif_Engine but because it now supports GIF, MP4, it was renamed to jalagar/animated-art-engine. v3.1.0 is the beginning of the animated era.**

**Check out this [Youtube Tutorial](https://www.youtube.com/watch?v=z3jMEx6PRUc) on how it works!**

This python and node app generates layered-based gifs/MP4 to create animated NFT art! It is faster, simpler, and
produces higher quality gifs/MP4s than any other open source animated generative tool out there. It also
contains many more features including but not limited to stacking layers, if-then, ETH/Solana/Tezos, preview images,
inserting legendaries, gifs/MP4, batching to support hundreds of layers, and multiprocessing.

Export your animation as a png image sequence,
organize your layer folders with rarity, and the code does the rest! I plan to actively maintain this repo
and enhance it with various tools for months to come so be sure to ask questions in the discussion and write issues.

There are three steps:

1. [Python] Converts layers into spritesheets using [PIL](https://pillow.readthedocs.io/en/stable/). This step can be skipped if you already have the spritesheets, but
   is useful if you want to start with png files and makes the artist's life easier!
2. [Node] Create generative spritesheets from the layers from step 1.
   - The original idea came from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) but now most of the code in this step is forked from [nftchef's Generative Engine](https://github.com/nftchef/art-engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node). Please check out Hashlip's [📺 Youtube](https://www.youtube.com/channel/UC1LV4_VQGBJHTJjEWUmy8nA) / [👄 Discord](https://discord.com/invite/qh6MWhMJDN) / [🐦 Twitter](https://twitter.com/hashlipsnft) / [ℹ️ Website](https://hashlips.online/HashLips) for a more in depth explanation on how the generative process works.
3. [Python + gifski/ffmpeg] Convert spritesheets to gifs/MP4 using Python and [gifski](https://github.com/ImageOptim/gifski) or [ffmpeg](https://ffmpeg.org/) for MP4.

Checkout this [Medium post](https://jalagar-eth.medium.com/how-to-create-generative-animated-nft-art-in-under-an-hour-e7dab1785c56) and [How does it work?](#how-does-it-work) for more information!

Here's an example final result (or you can download the code and run it and see more bouncing balls :)). It is also pushed to production
on [OpenSea](https://opensea.io/collection/genesis-bouncing-ball).

<img src="./README_Assets/0.gif" width="200"><img src="./README_Assets/1.gif" width="200"><img src="./README_Assets/2.gif" width="200"><img src="./README_Assets/3.gif" width="200">

**EDIT tool now supports z-index/stacking, grouping, if-then statements, and incompatibilities**. See [this section for more information](#nftchef-improvements-z-indexstacking-grouping-if-then-statements-and-incompatibilities). Here is an example of having one layer that is both in front and behind the ball.

<img src="./README_Assets/z-index/0.gif" width="200">

## Requirements

Install an IDE of your preference. [Recomended](https://code.visualstudio.com/download)

Install the latest version of [Node.js](https://nodejs.org/en/download/)

- Run this command on your system terminal to check if node is installed:

        node -v

Install the latest version of [Python 3](https://www.python.org/downloads/). I am currently using 3.8.1 but anything above 3.6 should work.

- Run this command on your system terminal to check if node is installed:

        python3 --version

If you want to output gifs then:

Install [gifski](https://gif.ski/). I recommend using brew `brew install gifski` if you're on Mac OSX. If you don't have brew you can install it using [brew](https://brew.sh/) on Mac OSX. Or if you're on Windows
you can install it using [Chocolatey](https://community.chocolatey.org/): `choco install gifski`.

If you're on Linux, some people were having issues with `gifski` so you can skip installing it. You will have to set
the `gifTool` config to `imageio` instead (see later instructions).

If none of those methods work, follow instructions on gifski [gifski Github](https://github.com/ImageOptim/gifski). Gifski is crucial for this tool because it provides the best gif generation
out of all the tools I checked out (PIL, imageio, ImageMagic, js libraries).

If you want to output MP4s then:

Install [ffmpeg](https://ffmpeg.org/). I recommend using brew `brew install ffmpeg` if you're on Mac OSX. If you don't have brew you can install it using [brew](https://brew.sh/) on Mac OSX. Or if you're on Windows
you can install it using [Chocolatey](https://community.chocolatey.org/): `choco install ffmpeg`.

If you plan on developing on this repository, run `pre-commit` to install pre-commit hooks.

If you're on Windows you can optionally install [Make](https://www.gnu.org/software/make/) by running `choco install make`. Make is already pre-installed on Mac.

### Installation

- Download this repo and extract all the files.
- Run this command on your root folder using the terminal:

        make first_time_setup

If you have any issues with this command, try running each separate command:

       python3 -m pip install --upgrade Pillow && pip3 install -r requirements.txt

       cd step2_spritesheet_to_generative_sheet && npm i

Each environment can be different, so try Google your issues. I'll add a few known issues below:

Known issues:

- [M1 Mac: Canvas prebuild isn't built for ARM computers](https://github.com/Automattic/node-canvas/issues/1825) so you need to install it [from their Github](https://github.com/Automattic/node-canvas/wiki#installation-guides)
- `cd` command might not work on Windows depending on what Terminal you are using. You may have to edit the `Makefile` to use `CHDIR` or the equivalent.
- If you're on Windows 10 you might get a 'make' is not recognized. Try `choco install make` or follow these [instructions](https://pakstech.com/blog/make-windows/#:~:text=make%20%3A%20The%20term%20'make',choose%20Path%20and%20click%20Edit). Otherwise you can copy and paste the instructions manually in `Makefile`.
- If you're on Windows you might get an error where 'python3' does not exist, try modify the `Makefile` and replace python3 with python. Thank you!
- If you don't have brew installed, look at [gifski](https://github.com/ImageOptim/gifski) docs for another way to install gifski or look at [ffmpeg](https://ffmpeg.org/) for MP4.

## How to run?

Load the png or gif files into the `/layers` folder where each layer is a folder, and each folder contains
another attribute folder which contains the individual frames and a rarity percentage. For example if you wanted
a background layer you would have `/layers/background/blue#20` and `/layers/background/red#20`.

In each attribute folder, the frames should be named `0.png` -> `X.png` or `0.gif`. See code or [step 1](#step-1) for folder structure. The code
will handle any number of layers, so you could have a layer with two frames, another layer with one frame, and another with 20 frames,
and as long as you pass `numberOfFrames` = 20, then the layers will be repeated until they hit 20.

**EDIT** You can leave the frame names whatever you want, and set `useFileNumbering` to `false`. This makes it easier if you have hundreds of frames and don't want to rename each one.

Update `global_config.json` with:

1.  **`'totalSupply'`** : total number of gifs/MP4 to generate.
2.  **`'height'`** : height of one frame. This should be equal to width. Default is 350 (see [https://docs.opensea.io/docs/metadata-standards#:~:text=We%20recommend%20using%20a%20350%20x%20350%20image](OpenSea recommendation))
3.  **`'width'`** : width of one frame. This should be equal to height. Default is 350 (see [https://docs.opensea.io/docs/metadata-standards#:~:text=We%20recommend%20using%20a%20350%20x%20350%20image](OpenSea recommendation))
4.  **`'framesPerSecond'`** : number of frames per second. This will not be exact because PIL takes in integer milliseconds per frame
    (so 12fps = 83.3ms per frame but rounded to an int = 83ms). This will not be recognizable by the human eye, but worth calling out.
5.  **`'numberOfFrames'`** : number of total frames. For example you could have 24 frames, but you want to render it 12fps.
6.  **`'description'`** : description to be put in the metadata.
7.  **`'baseUri'`** : baseUri to be put in the metadata.
8.  **`'saveIndividualFrames'`** : this is if you want to save the individual final frames, for example if you want to let people pick just one frame for a profile page.
9. **`'layersFolder'`**: this is the folder that you want to use for the layers. The default is `layers`, but this allows you to have multiple versions of layers and run them side by side. The current repo has four example folders, `layers`, `layers_grouping`, `layers_if_then`, `layers_z_index` which all demonstrate features from [nftchef's repo](https://generator.nftchef.dev/).
10. **`'quality'`**: quality of the output, 1-100.
11. **`'gifTool'`**: pick which gif generation method to use, `gifski` or `imageio`. Gifski is better overall, but some people were having issues with it on Linux. Also `imageio` will work for more pixel art, so if you don't want to download Gifski you can set this to `imageio`.
12. **`'MP4Tool'`**: pick which MP4 generation method to use. Only supports `ffmpeg` at the moment.
13. **`'outputType'`**: select `gif` or `mp4`.
14. **`'useBatches'`**: set to `true` if you want to take advantage of [batching](#batching). Otherwise does nothing.
15. **`'numFramesPerBatch'`**: number of frames for each batch. See [batching](#batching) for more information. Only does something if `useBatches` is set to `true`.
16. **`'loopGif'`**: `true` if you want to loop the gif, `false` if you don't want to loop it.
17. **`'useMultiprocessing'`**: `true` if you want to use multi-processing which will speed up step1 and step3. You can configure how many processors to use with `processorCount`. Use at your own discretion, I would recommend slowly increase `processorCount` and monitor CPU usage, this could crash your computer.
18. **`'processorCount'`**: Number of processors to use with multi-processing. The cap is `multiprocessing.cpu_count()`. Use at your own discretion.
19. **`'useFileNumbering'`**: Use 0.png -> X.png numbering or not. If you want to just use the render farm file names, set this to false.
20. **`'enableAudio'`**: BETA FEATURE. You can now add specific audio files per layer. See [Add Specific Audio Trait Section](#adding-specific-audio-per-trait) for more info.
21. **`'numLoopMP4'`**: Number of times to loop mp4.

Update `step2_spritesheet_to_generative_sheet/src/config.js` with your `layerConfigurations`. If you want the basic
configuration, just edit `layersOrder`, but if you want to take advantage of [nftchef's repo](https://generator.nftchef.dev/), then scroll through the file for some examples and modify `layerConfigurations` accordingly.

- To run the process end to end run:

        make all

Your output gifs will appear in `build/gif`, and your output MP4 will appear in `build/mp4`. The ETH JSON will appear in `build/json`. Try it yourself with the default settings
and layers!

If you want to switch between generating GIFs vs. MP4, you can change the `global_config.json` and just run `make step3`.

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
- grouping statements. You can now group traits into certain groups. So in the `layers_grouping` we have common balls and hats, and rare balls and hats, and the first `totalSupply - 1` balls are common, and the last one is rare. This will output in order, but you
can shuffle the layers by setting `shuffleLayerConfigurations` in `config.js` to `true`.
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

Step 3 takes the spritesheets from step 2 and creates gifs/MP4. Initially I used [PIL](https://pillow.readthedocs.io/en/stable/), but found some issues with pixel quality.

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

If you want to switch between generating gif vs. MP4, you need to change `outputType` to `mp4` and only run `make step3`.

### NFTChef improvements: z-index/stacking, grouping, if-then statements, and incompatibilities

Tool now supports z-index/stacking, grouping, if-then statements, and incompatibilities. See [nftchef's docs](https://generator.nftchef.dev/readme/) for more information.

TLDR if you don't want to read the doc:

- **z-index/stacking**: You can have the same layer appear in front and behind of another layer (see basketball above). You do this by specifying
a `z_,` in front of the name, for example `z1,` or `z2,`. See `layers_z_index` for an example, and try setting the `layersFolder` to `layers_z_index` to see this in action and checkout `layerConfigurationsZIndex` in the `config.js` for the configuration.
- **grouping**: You can group traits together into groups, like common/rare. Then you can specify how much supply you want of each. See `layers_grouping` folder and `layerConfigurationsGrouping` in the `config.js`.
- **if-then**: You can specify if this trait then have this other trait. For example, if ball is pink, then pick these two hats. See `layers_if_then` folder and `layerConfigurationsIfThen` in `config.js`.
- **incompatibilities**: You can specify if you want a layer to be incompatible with another layer. For example, if you don't want the flashing background to have a multicolor ball. NOTE, this only works if layer names are all unique or else this may lead to unintended behavior. See `layers_incompatible` and `const incompatible` in `config.js`. You can uncomment the line, and run the code with `layersFolder` set to `layers_incompatible` to see it working in action.

### Adding specific audio per trait

🧪 BETA FEATURE

You can now add specific audio per trait. For example if you want wind noises with a wind background,
and forest noises with a forest background.

Just put the audio file in the corresponding layer folder, and step3 will take that and put it on the mp4. You can see an example in the `layers_audio` folder. Try it out by setting `layersFolder` to `layers_audio` and `enableAudio` to `true`, then run `make all`. The mp4 will be the length of frames
and the audio will get truncated if it is too long.

The tool supports `mp3`, `wav`, and `m4a`.

### Extend existing collection into GIF/MP4

🧪 BETA FEATURE

[Video Walkthrough](https://www.youtube.com/watch?v=HvXOdGGspGo)

If you have existing metadata for an existing collection and want to either create a new collection with GIFs/MP4 or send GIF/MP4 version of the static image to holders,
this feature is for you! OR if you want to export as a spritesheet that can be imported into a pixel metaverse, this feature is for you!

There are a few configurations to you can use the tool:
1. If you already have a `_dna.json` generated by NFT Chef's repo, and a `_metadata.json` file which contains all the JSON files. Load the `_dna.json` into the `build` folder, and load the `_metadata.json` into the `build/json` folder. Setup your layers following the format above. Setup `global_config.json` and `config.js` and run `make regenerate`.
This is the most accurate and consistent way of generating GIFs based on existing layers and will work with NFT Chef's features.
2. If you generated using Hashlips' art engine, you won't have a `_dna.json`. You will only have `_metadata.json` which contains all the JSON files. Load this into the `build/json` folder, setup layers, setup `global_config.json`, `config.js` and run `make regenerate`. This under the hood attempts to regenerate
the DNA based on the JSON. This should work, but there may be features that are not backwards compatible so let me know if you come across such a case.
3. You don't have a `_metadata.json` file. Load all the individual `.json` files into `build/json`. Setup layers, setup `global_config.json`, `config.js` and run `make regenerate`. This is more annoying to do (if you have a ton of files), but will regenerate the `_metadata.json`, the `_dna.json`, and then regenerate the collection.

If you only want to regenerate spritesheets, you can set `SKIP_STEP_ONE` to `True` and `SKIP_STEP_THREE` to `True` in `regenerate.py`. Then instead
of putting your layers in the `layers` folder, you put them in `step1_layers_to_spritesheet/output` as an entire layer, and then
run `make regenerate`. The spritesheets will be in `step2_spritesheet_to_generative_sheet/output`.

If you need more than 32 frames at 1000x1000, follow the batches configuration and then run `make regenerate`. This will only work if you are doing
all the steps and not skipping any.

Please let me know if you have any issues or use cases I did not think of.


### Rarity stats

You can check the rarity stats of your collection with:

        make rarity


### Exclude a layer from DNA

If you want to have a layer _ignored_ in the DNA uniqueness check, you can set `bypassDNA: true` in the `options` object. This has the effect of making sure the rest of the traits are unique while not considering the `Background` Layers as traits, for example. The layers _are_ included in the final image.

```js
layersOrder: [
      { name: "Background" },
      { name: "Background" ,
        options: {
          bypassDNA: false;
        }
      },
```

### Provenance Hash Generation

If you need to generate a provenance hash (and, yes, you should, [read about it here](https://medium.com/coinmonks/the-elegance-of-the-nft-provenance-hash-solution-823b39f99473) ),

run the following util

```
make provenance
```

This will add a `imageHash` to each `.json` file and then concatenate them
and hash the file value into one string which is the `provenance` hash.

**The Provenance information is saved** to the build directory in `_provenance.json`. This file contains the final provenance hash as well as the (long) concatenated hash string.

\*Note, if you regenerate the gifs, **You will also need to regenerate this hash**.

### Remove trait

If you need to remove a trait from the generated attributes for ALL the generated metadata .json files, you can use the removeTrait util command.

`cd step2_spritesheet_to_generative_sheet && node utils/removeTrait.js "Trait Name"`

If you would like to print additional logging, use the -d flag

`cd step2_spritesheet_to_generative_sheet && node utils/removeTrait.js "Trait Name" -d`

### Update your metadata info

You can change the description and base Uri of your metadata even after running the code by updating `global_config.json` and running:

        make update_json

### Randomly Insert Rare items - Replace Util

If you would like to manually add 'hand drawn' or unique versions into the pool of generated items, this utility takes a source folder (of your new artwork) and inserts it into the `build` directory, assigning them to random id's.

#### Requirements

- Place gifs into ultraRares/gifs
- Put matching, sequential json files in the ultraRares/json folder

example:

```
├── ultraRares
│   ├── gifs
│   │   ├── 0.gif
│   │   └── 1.gif
│   └── json
│       ├── 0.json
│       └── 1.json
```

**You must have matching json files for each of your images.**

#### Setting up the JSON.

Because this script randomizes which tokens to replace/place, _it is important_ to update the metadata properly with the resulting tokenId #.

**_Everywhere_ you need the edition number in the metadata should use the `##` identifier.**

```json
  "edition": "##",
```

**Don't forget the image URI!**

```json
  "name": "## super rare sunburn ",
  "image": "ipfs://NewUriToReplace/##.png",
  "edition": "##",
```

#### Running

Run with `make replace`. If you need to replace the folder name, you may have to edit the `Makefile` directly with the folder.

**Note this will not update _dna.json because these new JSONs don't have DNA. This will modify _metadata.json though.**

### Solana metadata

🧪 BETA FEATURE

After running `make all` you can run generate the Solana metadata in two steps:
- Edit `step2_spritesheet_to_generative_sheet/Solana/solanaConfig.js`
- `make solana` to generate the Solana metadata. This will create an output folder `build/solana`with the gifs and the metadata.

Most of the code comes from [nftchef](https://github.com/nftchef/art-engine/blob/nested-folder-structure/utils/metaplex.js).

I have not tried this on any test net or production Solana chain, so please flag any issues or create a PR to fix them!

### Tezos metadata

🧪 BETA FEATURE

I have not tried this on any test net or production Tezos chain, so please flag any issues or create a PR to fix them!

See [Tezos README](step2_spritesheet_to_generative_sheet/documentation/other-blockchains/tezos.md) for more information.

### Batching

Do you want higher resolution, more frames, and larger gifs/MP4? Batching is for you! Currently step2 is limited by 32000 pixel files,
so in order to get around this we must batch the entire process into chunks and then combine them at the end.

Set `useBatches` in `global_config.json` to `true` and then set `numFramesPerBatch` to an even divisible of `numberOfFrames`.

Then run `make all_batch`. This under the hood first runs `make step1` + `make step2` to generate the initial metadata, then `python3 batch.py`
which creates the remaining images based on the initial metadata.


### Preview Gif/MP4

If you want a preview gif/MP4 of a subset of gifs (like Hashlips), run

`make preview`

This will output `preview.gif`/`preview.mp4` in the `build` folder. The default number of previews is 4 but you can change this in
`step3_generative_sheet_to_output/preview.py` at the top `NUM_PREVIEW_OUTPUT`. Currently it will randomly select the gifs/MP4,
if you want to output the first X, set `SORT_ORDER` to `OrderEnum.ASC` and if you want to output the last X,
set `SORT_ORDER` to `OrderEnum.DESC`.


## IMPORTANT NOTES

All of the code in step1 and step3 was written by me. The original idea for the repo came from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) but now most of the code in step 2 is forked from [nftchef's Generative Engine](https://github.com/nftchef/art-engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node).


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

Q: What file types do you support?

Input type: gif or png

Output type: gif or MP4

Q: What blockchains do you support?

Ethereum, Solana, Tezos.

Be sure to follow me for more updates on this project:

[Twitter](https://twitter.com/jalagar_eth)

[GitHub](https://github.com/jalagar/)

[Medium](https://jalagar-eth.medium.com/)

My ETH address is 0x4233EfcB109BF6618071759335a7b9ab84F2F4f3 if you feel like being generous :). I just quit my job to work on NFTs full time
so anything is appreciated.

If you want to see this code in action, we're using it for my fitness and mental health company Fitness Friends. Join the Discord if you need help with the animated art engine, you can get direct access to me in the #dev channel:

[Twitter](https://twitter.com/FitFriends_NFT)

[Website](https://www.fitnessfriends.io/)

[Discord](discord.gg/Nn36NUK9ba)
