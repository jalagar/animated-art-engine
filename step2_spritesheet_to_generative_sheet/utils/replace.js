"use strict";

/**
 * This utility tool is designed specifically for the scenario in which you
 * would like to replace one or many tokens with one off, non-generated items,
 * (or any gif/metadata combo that does NOT conflict with the generators permutation DNA checks)

 */

const isLocal = typeof process.pkg === "undefined";
const basePath = isLocal ? process.cwd() : path.dirname(process.execPath);
const fs = require("fs");
const path = require("path");
const { Command } = require("commander");
const program = new Command();
const chalk = require("chalk");
const keccak256 = require("keccak256");
const { start } = require("repl");
const { startIndex } = require(path.join(basePath, "/src/config.js"));

const builtGifsDir = `${basePath}/../build/gifs`;
const builtJsonDir = `${basePath}/../build/json`;

const getIndividualJsonFiles = (sourcePath) => {
  return fs
    .readdirSync(sourcePath)
    .filter((item) => /^[0-9]{1,6}.json/g.test(item));
};

const getIndividualgifFiles = (sourcePath) => {
  return fs.readdirSync(sourcePath);
};

/**
 * Given some input, creates a sha256 hash.
 * @param {Object} input
 */
const hash = (input) => {
  const hashable = typeof input === Buffer ? input : JSON.stringify(input);
  return keccak256(hashable).toString("hex");
};

/**
 * Resolve an objects nested path from string
 * @param {String} path string path to object
 * @param {Object} obj Optional to directly return the value
 * @returns
 */
function resolveNested(stringpath, obj) {
  return stringpath
    .split(".") // split string based on `.`
    .reduce(function (o, k) {
      return o && o[k]; // get inner property if `o` is defined else get `o` and return
    }, obj); // set initial value as object
}

/**
 * Randomly selects a number within the range of built gifs.
 * Since gifs and json files in the build folder are assumed to be identical,
 * we index of the length of the gifs directory.
 *
 * @param {String} gif incomong filename
 * @param {Number} randomID new index to replace existing gif/json files
 * @param {String} sourcePath path to source files
 * @param {Object} options command options object
 */
const replace = (gif, randomID, sourcePath, options) => {
  options.sneak
    ? console.log(chalk.cyan(`Randomly replacing ${gif} -> ${randomID} `))
    : null;
  // console.log({ gif, index, sourcePath });
  const gifNum = gif.substr(0, gif.lastIndexOf(".")) || gif;
  const gifExtension = gif.split(".").pop();

  // read the data, replace the numbers
  const currentGif = fs.readFileSync(path.join(sourcePath, "gifs", gif));
  try {
    const currentData = fs.readFileSync(
      path.join(sourcePath, "json", `${gifNum}.json`)
    );

    const newMetadata = JSON.parse(currentData);
    // hash the gif
    const gifHash = hash(currentGif);
    newMetadata.imageHash = gifHash;

    // replace all ## with proper edition number
    const symbol = options.replacementSymbol
      ? new RegExp(options.replacementSymbol, "gm")
      : /"##"|##/gm;

    options.debug ? console.log({ symbol }) : null;
    const updatedMetadata = JSON.stringify(newMetadata, null, 2).replace(
      symbol,
      randomID
    );

    options.debug
      ? console.log(`Generating hash from ${gif}`, gifHash)
      : null;

    const globalMetadata = JSON.parse(
      fs.readFileSync(path.join(builtJsonDir, "_metadata.json"))
    );

    // update the object in the globalFile,
    const updateIndex = globalMetadata.findIndex((item) => {
      const globalIndex = options.identifier
        ? resolveNested(options.identifier, item)
        : item.edition;
      return globalIndex === randomID;
    });
    if (updateIndex < 0) {
      throw new Error(
        `Could not find the identifier, "${options.identifier ? options.identifier : "edition"
        }" in _metadata.json. Check that it is correct and try again.`
      );
    }
    options.debug
      ? console.log(`updating _metadata.json index [${updateIndex}]`)
      : null;

    const updatedGlobalMetadata = globalMetadata;
    // set the new data in the _metadata.json
    updatedGlobalMetadata[updateIndex] = JSON.parse(updatedMetadata);
    // everything looks good to write files.
    // overwrite the build json file
    fs.writeFileSync(
      path.join(builtJsonDir, `${randomID}.json`),
      updatedMetadata
    );
    // overwrite the build gif file
    fs.writeFileSync(
      path.join(builtGifsDir, `${randomID}.${gifExtension}`),
      currentGif
    );

    // overwrite the build gif file
    fs.writeFileSync(
      path.join(builtJsonDir, "_metadata.json"),
      JSON.stringify(updatedGlobalMetadata, null, 2)
    );
  } catch (error) {
    console.error(error);
    throw new Error(`Gif ${gifNum} is missing a matching JSON file`);
  }
};

program
  .argument("<source>")
  .option("-d, --debug", "display additional logging")
  .option("-s, --sneak", "output the random ID's that are being replaced")
  .option(
    "-r, --replacementSymbol <symbol>",
    "The character used as a placeholder for edition numbers"
  )
  .option(
    "-i, --identifier <identifier>",
    'Change the default object identifier/location for the edition/id number. defaults to "edition"'
  )
  .action((source, options, command) => {
    // get source to replace from
    // replaceFrom source/ -> destination

    // get source to replace to, gif + json
    const gifSource = path.join(basePath, source, `/gifs`);
    const dataSource = path.join(basePath, source, `/json`);
    const gifFiles = getIndividualgifFiles(gifSource);
    const dataFiles = getIndividualJsonFiles(dataSource);
    // global variable to keep track of which ID's have been used.
    const randomIDs = new Set();

    console.log(
      chalk.greenBright.inverse(`\nPulling gif and data from ${source}`)
    );
    options.debug
      ? console.log(
        `\tFound ${gifFiles.length} gifs in "${gifSource}"
        and
        ${dataFiles.length} in ${dataSource}`
      )
      : null;

    // Main functions in trycatch block for cleaner error logging if throwing errors.
    // try {
    if (gifFiles.length !== dataFiles.length) {
      throw new Error(
        "Number of gifs and number of metadata JSON files do not match. \n Are you Missing one?"
      );
    }
    // get the length of gifs in the build folder
    const totalCount = fs.readdirSync(builtGifsDir).length;
    while (randomIDs.size < gifFiles.length) {
      randomIDs.add(Math.floor(Math.random() * (totalCount + startIndex - 1)));
    }
    const randomIDArray = Array.from(randomIDs);

    // randomly choose a number
    gifFiles.forEach((gif, index) =>
      replace(gif, randomIDArray[index], path.join(basePath, source), options)
    );
    // if gif is missing accompanying json, throw error.
    console.log(
      chalk.green(
        `\nSuccessfully inserted ${chalk.bgGreenBright.black(
          gifFiles.length
        )} gifs and Data Files into the build directories\n`
      )
    );
    // } catch (error) {
    //   console.error(chalk.bgRedBright.black(error));
    // }

    // side effects?
    // does it affect rarity data util?
    // provenance hash?

    // jsonFiles.forEach((filename) => {
    //   // read the contents
    //   options.debug ? console.log(`removing ${trait} from ${filename}`) : null;
    //   const contents = JSON.parse(fs.readFileSync(`${jsonDir}/${filename}`));

    //   const hasTrait = contents.attributes.some(
    //     (attr) => attr.trait_type === trait
    //   );

    //   if (!hasTrait) {
    //     console.log(chalk.yellow(`"${trait}" not found in ${filename}`));
    //   }
    //   // remove the trait from attributes

    //   contents.attributes = contents.attributes.filter(
    //     (traits) => traits.trait_type !== trait
    //   );

    //   // write the file
    //   fs.writeFileSync(
    //     `${jsonDir}/${filename}`,
    //     JSON.stringify(contents, null, 2)
    //   );

    //   options.debug
    //     ? console.log(
    //         hasTrait ? chalk.greenBright("Removed \n") : "…skipped \n"
    //       )
    //     : null;
    // });
  });

program.parse();
