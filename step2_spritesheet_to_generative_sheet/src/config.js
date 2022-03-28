"use strict";

const path = require("path");
const isLocal = typeof process.pkg === "undefined";
const basePath = isLocal ? process.cwd() : path.dirname(process.execPath);
const { MODE } = require(path.join(basePath, "src/blendMode.js"));
const description = "Your project description";
const baseUri = "ipfs://NewUriToReplace";
const numNFTs = 10;

const layerConfigurations = [
  {
    growEditionSizeTo: numNFTs,
    layersOrder: [{ name: "background" }, { name: "ball" }],
  },
];

const shuffleLayerConfigurations = false;

const debugLogs = false;

const format = {
  width: 12000,
  height: 1000,
};

const background = {
  generate: false,
  brightness: "80%",
};

const extraMetadata = {};

const rarityDelimiter = "#";

const uniqueDnaTorrance = 10000;

module.exports = {
  format,
  baseUri,
  description,
  background,
  uniqueDnaTorrance,
  layerConfigurations,
  rarityDelimiter,
  shuffleLayerConfigurations,
  debugLogs,
  extraMetadata,
};
