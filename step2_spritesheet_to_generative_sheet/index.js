"use strict";

const path = require("path");
const isLocal = typeof process.pkg === "undefined";
const basePath = isLocal ? process.cwd() : path.dirname(process.execPath);

const fs = require("fs");
const { Command } = require("commander");
const program = new Command();
const chalk = require("chalk");

const { startCreating, buildSetup } = require(path.join(
  basePath,
  "/src/main.js"
));

program
  .name("generate")
  .option("--continue <dna>", "Continues generation using a _dna.json file")
  .option("--height <height>", "Override height")
  .option("--width <width>", "Override width")
  .action((options) => {
    options.continue
      ? console.log(
        chalk.bgCyanBright("\n continuing generation using _dna.json file \n")
      )
      : null;
    buildSetup();
    let dna = null;
    if (options.continue) {
      const storedGenomes = JSON.parse(fs.readFileSync(options.continue));
      dna = new Set(storedGenomes);
      console.log({ dna });
    }
    const args = program.args;
    if (args.length == 2) {
      startCreating(dna, parseInt(args[0]), parseInt(args[1]));
    } else {
      startCreating(dna, null, null);
    }

  });

program.parse(process.argv);