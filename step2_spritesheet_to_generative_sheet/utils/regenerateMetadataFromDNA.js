"use strict";

const isLocal = typeof process.pkg === "undefined";
const basePath = isLocal ? process.cwd() : path.dirname(process.execPath);
const fs = require("fs");
const path = require("path");
const dnaFilePath = `${basePath}/../build/_dna.json`;
const rawDNAData = fs.readFileSync(dnaFilePath);
const DNAData = JSON.parse(rawDNAData);

const metadataFilePath = `${basePath}/../build/json/_metadata.json`;
const rawMetadata = fs.readFileSync(metadataFilePath);
const data = JSON.parse(rawMetadata);

const {
    saveMetaDataSingleFile,
    addMetadata,
    hash,
    writeMetaData,
} = require(path.join(basePath, "/src/main.js"));

const {
    startIndex,
} = require(path.join(basePath, "/src/config.js"));

const metadataList = [];

DNAData.forEach((dna, index) => {
    const tempMetadata = addMetadata(
        dna, index + startIndex, {
        _offset: 0,
        _prefix: "",
    }, []);
    const existingMetadata = data[index]
    tempMetadata.attributes = existingMetadata.attributes;
    tempMetadata.dna = hash(dna);
    metadataList.push(tempMetadata);
    saveMetaDataSingleFile(index + startIndex, tempMetadata);
})

writeMetaData(JSON.stringify(metadataList, null, 2));
