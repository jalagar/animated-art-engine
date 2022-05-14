"use strict";
/**
 * Creates output image based on existing DNA metadata. Used in batching
 * to re-use the same DNA to create the subsequent batches.
 */

const isLocal = typeof process.pkg === "undefined";
const basePath = isLocal ? process.cwd() : path.dirname(process.execPath);
const fs = require("fs");
const path = require("path");
const { Command } = require("commander");
const program = new Command();
const { createCanvas } = require("canvas");

const chalk = require("chalk");

const imageDir = `${basePath}/output/images`;
const dnaFilePath = `${basePath}/../build/_dna.json`;

const {
  format,
  background,
  layerConfigurations,
  outputJPEG,
  startIndex,
  outputDir,
} = require(path.join(basePath, "/src/config.js"));

const {
  paintLayers,
  layersSetup,
  constructLayerToDna,
  loadLayerImg,
  sortZIndex,
} = require(path.join(basePath, "/src/main.js"));

const canvas = createCanvas(format.width, format.height);
const ctxMain = canvas.getContext("2d");

const getDNA = () => {
  return JSON.parse(fs.readFileSync(dnaFilePath));
  // .filter((item) => /^[0-9]{1,6}.json/g.test(item));
};

const createItem = (_id, layers) => {
  const existingDna = getDNA()[_id - startIndex];
  return { existingDna, layerImages: constructLayerToDna(existingDna, layers) };
};

const outputFiles = (_id) => {
  // Save the image
  fs.writeFileSync(
    `${imageDir}/${_id}${outputJPEG ? ".jpg" : ".png"}`,
    canvas.toBuffer(`${outputJPEG ? "image/jpeg" : "image/png"}`)
  );
};

const regenerateItem = (_id, options) => {
  // get the dna lists
  // FIgure out which layer config set it's from
  const layerEdition = layerConfigurations.reduce((acc, config) => {
    return [...acc, config.growEditionSizeTo];
  }, []);
  const layerConfigIndex = layerEdition.findIndex(
    (editionCount) => _id <= editionCount
  );

  const layers = layersSetup(layerConfigurations[layerConfigIndex].layersOrder);

  const { existingDna, layerImages } = createItem(_id, layers);
  if (!existingDna) {
    return;
  }
  options.debug ? console.log({ existingDna }) : null;

  // regenerate an image using main functions
  const allImages = layerImages.reduce((images, layer) => {
    return [...images, ...layer.selectedElements];
  }, []);

  const loadedElements = [];
  sortZIndex(allImages).forEach((layer) => {
    loadedElements.push(loadLayerImg(layer));
  });

  Promise.all(loadedElements).then((renderObjectArray) => {
    const layerData = {
      existingDna,
      layerConfigIndex,
      abstractedIndexes: [_id],
      _background: background,
    };
    // paint layers to global canvas context.. no return value
    paintLayers(ctxMain, renderObjectArray, layerData, []);
    outputFiles(_id, layerData, options);
  });
};

program
  .argument("<id>")
  .option("-d, --debug", "display some debugging")
  .action((id, options, command) => {
    options.debug
      ? console.log(chalk.greenBright.inverse(`Regenerating #${id}`))
      : null;

    regenerateItem(id, options);
  });

program.parse();
