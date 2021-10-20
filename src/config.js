const description =
  "This is the description of your NFT project, remember to replace this";
const baseUri = "https://Change_this";

const layersOrder = [
  { name: "Background" },
  { name: "Ball" },
];

const format = {
  width: 2560,
  height: 640,
};

const background = {
  generate: true,
  brightness: "80%",
};

const uniqueDnaTorrance = 10000;

const editionSize = 4;

module.exports = {
  layersOrder,
  format,
  editionSize,
  baseUri,
  description,
  background,
  uniqueDnaTorrance,
};