"use strict";

const path = require("path");
const isLocal = typeof process.pkg === "undefined";
const basePath = isLocal ? process.cwd() : path.dirname(process.execPath);
const fs = require("fs");

const { baseUri, description } = require(path.join(
  basePath,
  "../global_config.json"
));

// read json data
let rawdata = fs.readFileSync(`${basePath}/../build/json/_metadata.json`);
let data = JSON.parse(rawdata);

data.forEach((item) => {
  item.description = description;
  item.image = `${baseUri}/${item.edition}.gif`;
  fs.writeFileSync(
    `${basePath}/../build/json/${item.edition}`,
    JSON.stringify(item, null, 2)
  );
});

fs.writeFileSync(
  `${basePath}/../build/json/_metadata.json`,
  JSON.stringify(data, null, 2)
);

console.log(`Updated baseUri for images to ===> ${baseUri}`);
console.log(`Updated description for images to ===> ${description}`);
