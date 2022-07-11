const keccak256 = require("keccak256");
const fs = require("fs");
const chalk = require("chalk");
const path = require("path");
const isLocal = typeof process.pkg === "undefined";
const basePath = isLocal ? process.cwd() : path.dirname(process.execPath);

const { buildDir, outputType } = require(path.join(basePath, "/src/config.js"));

/**
 * Given some input, creates a sha256 hash.
 * @param {Object} input
 */
const hash = (input) => {
  const hashable = typeof input === Buffer ? input : JSON.stringify(input);
  return keccak256(hashable).toString("hex");
};

// Read files from the build folder defined in config.
const metadata = JSON.parse(
  fs.readFileSync(path.join(buildDir, `json/_metadata.json`), "utf-8")
);
// read json data
let rawdata = fs.readFileSync(`${basePath}/../build/json/_metadata.json`);

let data = JSON.parse(rawdata);

/**
 * loop over each loaded item, modify the data, and overwrite
 * the existing files.
 *
 * uses item.edition to ensure the proper number is used
 * insead of the loop index as images may have a different order.
 */
data.forEach((item, i) => {
  // Metadata options
  const savedFile = fs.readFileSync(
    `${buildDir}/${outputType}/${item.imageName}`
  );
  item.imageHash = hash(savedFile);

  fs.writeFileSync(
    `${basePath}/../build/json/${item.edition}.json`,
    JSON.stringify(item, null, 2)
  );
});

fs.writeFileSync(
  `${basePath}/../build/json/_metadata.json`,
  JSON.stringify(data, null, 2)
);

const accumulatedHashString = data.reduce((acc, item) => {
  return acc.concat(item.imageHash);
}, []);

const provenance = hash(accumulatedHashString.join(""));

fs.writeFileSync(
  `${buildDir}/_provenance.json`,
  JSON.stringify(
    { provenance, concatenatedHashString: accumulatedHashString.join("") },
    null,
    "\t"
  )
);

console.log(`\nProvenance Hash Save in !\n${buildDir}/../_provenance.json\n`);
console.log(chalk.greenBright.bold(`${provenance} \n`));
