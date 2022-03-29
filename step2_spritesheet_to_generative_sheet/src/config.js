"use strict";

const path = require("path");
const isLocal = typeof process.pkg === "undefined";
const basePath = isLocal ? process.cwd() : path.dirname(process.execPath);

const { totalSupply, layersOrder, description, baseUri } = require(path.join(
  basePath,
  "../global_config.json"
));

const layerConfigurations = [
  {
    growEditionSizeTo: totalSupply,
    layersOrder: layersOrder.map((layer) => {
      return {
        name: layer,
      };
    }),
  },
];

const shuffleLayerConfigurations = false;

const extraMetadata = {};

const rarityDelimiter = "#";

const uniqueDnaTorrance = 10000;

module.exports = {
  baseUri,
  description,
  uniqueDnaTorrance,
  layerConfigurations,
  rarityDelimiter,
  shuffleLayerConfigurations,
  extraMetadata,
};
