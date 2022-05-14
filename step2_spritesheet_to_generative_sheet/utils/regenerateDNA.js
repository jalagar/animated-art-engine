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
const { startIndex } = require("../src/config");
const program = new Command();

const {
    layerConfigurations,
} = require(path.join(basePath, "/src/config.js"));

const {
    layersSetup,
    DNA_DELIMITER,
    writeDnaLog,
} = require(path.join(basePath, "/src/main.js"));

let rawdata = fs.readFileSync(`${basePath}/../build/json/_metadata.json`);
let data = JSON.parse(rawdata);

const regenerateDNA = (options) => {
    console.log("Regenerating DNA Log")
    const dnaList = [];
    data.forEach((item, _id) => {
        // get the dna lists
        // Figure out which layer config set it's from
        const layerEdition = layerConfigurations.reduce((acc, config) => {
            return [...acc, config.growEditionSizeTo];
        }, []);
        const layerConfigIndex = layerEdition.findIndex(
            (editionCount) => _id <= editionCount
        );
        const dnaSequence = [];
        const layers = layersSetup(layerConfigurations[layerConfigIndex].layersOrder);

        // Loop through attributes, find the layer, and reconstruct the dna string
        item.attributes.forEach((attribute) => {
            const { trait_type: traitType, value } = attribute;
            const trait = layers.find((trait) => trait.name == traitType)

            const { id: parentId, elements } = trait;
            const layer = elements.find((element) => element.name == value);

            let dnaString;
            if (!layer) {
                console.log(`No corresponding layer for ${_id + startIndex}, skipping assuming this is a legendary`);
                dnaString = '';
            } else {
                dnaString = `${parentId}.${layer.id}:${layer.zindex}${layer.filename}`;
            }
            dnaSequence.push(dnaString)
        })
        dnaList.push(dnaSequence.join(DNA_DELIMITER));
    })
    writeDnaLog(JSON.stringify([...dnaList], null, 2));
}

program
    .option("-d, --debug", "display some debugging")
    .action((options, command) => {
        regenerateDNA(options);
    });

program.parse();
