# Tezos

🧪 BETA FEATURE

THIS FEATURE HAS NOT BEEN TESTED ON PRODUCTION CHAIN. USE WITH YOUR OWN DISCRETION.

Since tezos need some extra config information, in order to change config for tezos specific metadata you can look into `./Tezos/tezosConfig.js`.

### To set up your Tezos specific metadata.

Configure the `tezosConfig.js` file located in the `Tezos/` folder. Here, enter in all the necessary information for your collection.

First run `make all` then run

```
make tezos
```

This will run `utils/tezos.js` which generates the metadata and also runs `utils/resize.js` which
will output two more folders under `build/` directory. Now you can upload all these three folders to IPFS namely `build/tezos/displayUri/`, `build/tezos/thumbnailUri/` and `build/gif`. After that you can update the base IPFS uri for these three folders in `/Tezos/tezosConfig.js`

```js
const baseUriPrefix = "ipfs://BASE_ARTIFACT_URI";
const baseDisplayUri = "ipfs://BASE_DISPLAY_URI";
const baseThumbnailUri = "ipfs://BASE_THUMBNAIL_URI";
```

Then to update the generated metadata with these base uris run the following command.

```
make update_info_tezos
```

That's it you're ready for launch of your NFT project.
